CREATE TABLE stock_price(code TEXT, date DATE, open DOUBLE, high DOUBLE, low DOUBLE, close DOUBLE, volume DOUBLE, openinterest DOUBLE, exrights DOUBLE, multiplier DOUBLE, PRIMARY KEY (code, date));
CREATE INDEX index_stock_price_date ON stock_price(date);
CREATE VIEW fixed_stock_price AS SELECT code, date, open * multiplier AS open, high * multiplier AS high, low * multiplier AS low, close * multiplier AS close, volume * multiplier AS volume FROM stock_price;

CREATE TABLE stock_signal_yearhl(code TEXT, date DATE, high DOUBLE, low DOUBLE, PRIMARY KEY (code, date));
CREATE INDEX index_stock_signal_yearhl ON stock_signal_yearhl(date);

CREATE TABLE stock_signal_sma(code TEXT, date DATE, sma DOUBLE, PRIMARY KEY (code, date));
CREATE INDEX index_stock_signal_sma ON stock_signal_sma(date);

CREATE TABLE stock_signal_variance(code TEXT, date DATE, mu DOUBLE, sigma DOUBLE);
CREATE INDEX index_stock_signal_variance ON stock_signal_variance(date);
