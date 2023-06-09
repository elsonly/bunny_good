DROP TABLE IF EXISTS accountdb.dealer.trades;
CREATE TABLE accountdb.dealer.trades(
    id BIGSERIAL PRIMARY KEY,
    trader_id varchar(10),
    broker_id varchar(7),
    account_id varchar(7),
    strategy INT,
    order_id varchar(10),
    order_type varchar(3),
    seqno varchar(20),
    security_type char(1), -- S, F
    trade_date date,
    trade_time time,
    code varchar(10),
    action char(1), -- B, S
    price double precision,
    qty int,
    CONSTRAINT fk_strategy FOREIGN KEY(strategy) REFERENCES dealer.strategy(id)
);
CREATE INDEX idx_trades_date ON accountdb.dealer.trades(trade_date);
CREATE INDEX idx_trades_date_strategy ON accountdb.dealer.trades(trade_date, strategy);
CREATE INDEX idx_trades_date_code ON accountdb.dealer.trades(trade_date, code);