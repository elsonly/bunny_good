DROP TABLE IF EXISTS accountdb.dealer.xq_signals;
CREATE TABLE accountdb.dealer.xq_signals(
    id char(3),
    sdate date,
    stime time,
    strategy_id INT,
    security_type varchar(7), -- S, F
    code varchar(10),
    order_type varchar(3), -- ROD, IOC, FOK
    action char(1), -- B, S
    quantity int,
    price double precision,
    CONSTRAINT fk_strategy_id
        FOREIGN KEY(strategy_id)
        REFERENCES dealer.strategy(id)
    --CONSTRAINT pk_xq_signals PRIMARY KEY(signal_date, signal_time, code)
);