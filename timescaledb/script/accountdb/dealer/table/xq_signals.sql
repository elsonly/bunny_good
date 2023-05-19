DROP TABLE IF EXISTS accountdb.dealer.xq_signals;
CREATE TABLE accountdb.dealer.xq_signals(
    id BIGSERIAL PRIMARY KEY,
    signal_date date,
    signal_time time,
    strategy_id INT,
    code varchar(10),
    order_type varchar(3), -- ROD, IOC, FOK
    action char(1), -- B, S
    order_qty int,
    order_price double precision,
    CONSTRAINT fk_strategy_id
        FOREIGN KEY(strategy_id)
        REFERENCES dealer.strategy(id)
);
CREATE INDEX idx_xq_signals_date ON accountdb.dealer.xq_signals(signal_date);
CREATE INDEX idx_xq_signals_date_strategy_id ON accountdb.dealer.xq_signals(signal_date, strategy_id);
CREATE INDEX idx_xq_signals_date_code ON accountdb.dealer.xq_signals(signal_date, code);