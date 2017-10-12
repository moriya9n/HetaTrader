import sqlite3
import datetime
import sys
import os.path
prog_base = os.path.dirname(sys.argv[0])
if prog_base == '':
    prog_base = './'

def get_last_registered(conn):
    cur = conn.cursor()
    cur.execute('SELECT date FROM fixed_stock_price WHERE code = "1001" ORDER BY date DESC limit 1')
    return datetime.datetime.strptime(cur.fetchone()[0], '%Y-%m-%d').date()

def search_52week_high(conn):
    print('52week high')
    cur = conn.cursor()
    last_registered = get_last_registered(conn)
    print(last_registered)
    cur.execute('SELECT * FROM fixed_stock_price AS a LEFT JOIN stock_signal_yearhl AS b USING(code, date) WHERE date = ? AND a.close > b.high', (last_registered,))
    for r in cur:
        print(r)
    
def search_break_sigma(conn):
    print('break sigma')
    cur = conn.cursor()
    last_registered = get_last_registered(conn)
    print(last_registered)
    cur.execute('SELECT * FROM fixed_stock_price AS a LEFT JOIN stock_signal_variance AS b USING(code, date) WHERE date = ? AND a.close > b.mu + b.sigma', (last_registered,))
    for r in cur:
        print(r)
    
def kabubot(conn):
    search_52week_high(conn)
    search_break_sigma(conn)

if __name__ == '__main__':
    conn = sqlite3.connect(os.path.join(prog_base, 'kabudb.sqlite3'))
    kabubot(conn)
