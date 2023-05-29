DROP TABLE IF EXISTS accountdb.dealer.sf31_orders;
CREATE TABLE accountdb.dealer.sf31_orders(
    id BIGSERIAL PRIMARY KEY,
    signal_id char(3),
    sfdate date,
    sftime time,
    strategy_id INT,
    code varchar(10),
    security_type varchar(7),  -- Stock
    order_type varchar(3), -- ROD, IOC, FOK
    price_type char(3), -- LMT, MKT, MOP
    action char(1), -- B, S
    quantity int,
    price double precision,
    order_id varchar(10),
    CONSTRAINT fk_strategy_id
        FOREIGN KEY(strategy_id)
        REFERENCES dealer.strategy(id)
);
