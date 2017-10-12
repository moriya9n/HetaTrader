import sqlite3
import datetime
import sys
import os.path
prog_base = os.path.dirname(sys.argv[0])
if prog_base == '':
    prog_base = './'
sys.path.append(prog_base)
import pan
import statistics

def update_variance(conn, code, period):
    cur = conn.cursor()
    cur.execute('SELECT * FROM fixed_stock_price WHERE code = ? ORDER BY date desc', (code,))
    last_regist = datetime.datetime.strptime(cur.fetchone()[1], '%Y-%m-%d').date() # date  
    cur.execute('SELECT * FROM fixed_stock_price WHERE code = ? and date < ? ORDER BY date desc LIMIT ?', (code, last_regist, period))
    d = [c[5] for c in cur]
    if len(d) < 2:
        return
    mean = statistics.mean(d)
    stdev = statistics.stdev(d)
    if mean == 0.0 or stdev == 0.0:
        return
    cur.execute('INSERT OR REPLACE INTO stock_signal_variance VALUES(?, ?, ?, ?)', (code, last_regist, mean, stdev))

def update_year_hl(conn, code):
    cur = conn.cursor()
    cur.execute('SELECT * FROM fixed_stock_price WHERE code = ? ORDER BY date desc', (code,))
    last_regist = datetime.datetime.strptime(cur.fetchone()[1], '%Y-%m-%d').date() # date  
    year_ago = last_regist - datetime.timedelta(weeks=52) # 52weeks ago
    cur.execute('SELECT MAX(high), MIN(low) from fixed_stock_price WHERE code = ? and date >= ? and date < ?', (code, year_ago, last_regist))
    hl = cur.fetchone()
    cur.execute('INSERT OR REPLACE INTO stock_signal_yearhl VALUES(?, ?, ?, ?)', (code, last_regist, hl[0], hl[1]))

def update_sma(conn, code, period):
    cur = conn.cursor()
    cur.execute('SELECT * FROM fixed_stock_price WHERE code = ? ORDER BY date desc', (code,))
    last_regist = datetime.datetime.strptime(cur.fetchone()[1], '%Y-%m-%d').date() # date  
    cur.execute('SELECT * FROM fixed_stock_price WHERE code = ? and date < ? ORDER BY date desc LIMIT ?', (code, last_regist, period))
    sma = 0.0
    cnt = 0
    for r in cur:
        sma += r[5] # close price
        cnt += 1
    if cnt == 0:
        return
    sma = sma / cnt
    cur.execute('INSERT OR REPLACE INTO stock_signal_sma VALUES(?, ?, ?)', (code, last_regist, sma))

def update_multiplier(conn, code):
    cur = conn.cursor()
    cur.execute('UPDATE stock_price SET multiplier = 1.0 WHERE code = ?', (code,))
    cur.execute('SELECT date, exrights FROM stock_price WHERE code = ? AND exrights != 1.0 ORDER BY date DESC', (code,))
    for r in cur.fetchall():
        cur.execute('UPDATE stock_price SET multiplier = multiplier * ? WHERE code = ? AND date < ?', (r[1], code, r[0]))
    cur.execute('SELECT date, exrights, multiplier FROM stock_price WHERE code = ?', (code,))

def fix_zero(conn, code):
    cur = conn.cursor()
    cur.execute('SELECT * FROM stock_price WHERE code = ? ORDER BY date', (code,))
    sv_open = 0.0
    sv_high = 0.0
    sv_low = 0.0
    sv_close = 0.0
    prices = cur.fetchall()
    for price in prices:
        (cd, dt, op, hi, lo, cl, vl, oi, er, ml) = price
        if vl > 0.0:
            (sv_open, sv_high, sv_low, sv_close) = (op, hi, lo, cl)
            continue
        cur.execute('UPDATE stock_price SET open=?, high=?, low=?, close=? WHERE code = ? and date = ?', (sv_open, sv_high, sv_low, sv_close, cd, dt))

def am_import(conn, am, code):
    cur = conn.cursor()
    try:
        am.prices.read(code)
        for pos in range(am.prices.end(), am.prices.begin() - 1, -1):
            if am.prices.isclosed(pos):
                continue
            dt = am.calendar.Date(pos)
            d = datetime.date(dt.year, dt.month, dt.day)
            cur.execute('INSERT INTO stock_price VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (code, d, am.prices.open(pos), am.prices.high(pos), am.prices.low(pos), am.prices.close(pos), am.prices.volume(pos), am.prices.openinterest(pos), am.prices.exrights(pos), 1.0))
    except Exception as e:
        print(e)
        pass

def createdb():
    am = pan.ActiveMarket()

    dbfile = os.path.join(prog_base, 'kabudb.sqlite3')
    initsql = None
    if not os.path.exists(dbfile):
        initsql = open(os.path.join(prog_base, 'kabudb.sql'), 'r').read()

    conn = sqlite3.connect(os.path.join(prog_base, 'kabudb.sqlite3'))
    if initsql:
        conn.executescript(initsql)

    names = am.names.AllNames(1)
    stocks = dict(zip(names[0], names[1]))

    codes = sorted(stocks.keys())

    for code in codes:
        print('[%s]' % code, end="", flush=True)
        am_import(conn, am, code)
        fix_zero(conn, code)
        update_multiplier(conn, code)
        update_year_hl(conn, code)
        update_sma(conn, code, 20)
        update_variance(conn, code, 21)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    createdb()

