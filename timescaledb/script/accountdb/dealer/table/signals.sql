DROP TABLE IF EXISTS accountdb.dealer.signals;
CREATE TABLE accountdb.dealer.signals(
    id char(3),
    source name,
    sdate date,
    stime time,
    strategy_id INT,
    security_type char(1), -- S, F
    code varchar(10),
    order_type char(3), -- ROD, IOC, FOK
    price_type char(3), -- LMT, MKT, MOP
    action char(1), -- B, S
    quantity int,
    price double precision,
    exit_type name,
    rm_validated boolean,
    rm_reject_reason name,
    CONSTRAINT fk_strategy_id
        FOREIGN KEY(strategy_id)
        REFERENCES dealer.strategy(id),
    CONSTRAINT pk_signals PRIMARY KEY(id, sdate)
);