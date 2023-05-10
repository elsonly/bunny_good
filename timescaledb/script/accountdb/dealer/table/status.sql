DROP TABLE IF EXISTS accountdb.dealer.orders;
CREATE TABLE accountdb.dealer.status(
    strategy INT,
    security_type char(1), -- S, F
    code varchar(10),
    action char(1), -- B, S
    in_date date,
    out_date date,
    status varchar(10),
    CONSTRAINT fk_strategy FOREIGN KEY(strategy) REFERENCES dealer.strategy(id)
);