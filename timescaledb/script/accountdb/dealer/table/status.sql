DROP TABLE IF EXISTS accountdb.dealer.status;
CREATE TABLE accountdb.dealer.status(
    strategy INT,
    security_type char(1), -- S, F
    code varchar(10),
    cost double precision,
    qty INT,
    in_date date,
    out_date date,
    --status varchar(10),
    CONSTRAINT fk_strategy FOREIGN KEY(strategy) REFERENCES dealer.strategy(id)
);