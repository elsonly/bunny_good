DROP TABLE IF EXISTS accountdb.dealer.exit_signals;
CREATE TABLE accountdb.dealer.exit_signals(
    id char(16),
    sdate date,
    stime time,
    strategy_id INT,
    security_type varchar(7), -- S, F
    code varchar(10),
    order_type varchar(3), -- ROD, IOC, FOK
    action char(1), -- B, S
    quantity int,
    price double precision,
    exit_type name,
    CONSTRAINT fk_strategy_id
        FOREIGN KEY(strategy_id)
        REFERENCES dealer.strategy(id),
    CONSTRAINT pk_exit_signals PRIMARY KEY(id, sdate)
);