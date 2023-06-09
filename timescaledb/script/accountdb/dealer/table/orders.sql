DROP TABLE IF EXISTS accountdb.dealer.orders;
CREATE TABLE accountdb.dealer.orders(
    id BIGSERIAL PRIMARY KEY,
    trader_id varchar(10),
    broker_id varchar(7),
    account_id varchar(7),
    strategy INT,
    order_id varchar(10),
    security_type char(1), -- S, F
    order_date date,
    order_time time,
    code varchar(10),
    action char(1), -- B, S
    order_price double precision,
    order_qty int,
    order_type varchar(3), -- ROD, IOC, FOK
    price_type varchar(3), -- LMT, MKT, MOP
    status varchar(10),
    msg text,
    CONSTRAINT fk_strategy_id
        FOREIGN KEY(strategy)
        REFERENCES dealer.strategy(id)
);
CREATE INDEX idx_orders_date ON accountdb.dealer.orders(order_date);
CREATE INDEX idx_orders_date_strategy ON accountdb.dealer.orders(order_date, strategy);
CREATE INDEX idx_orders_date_code ON accountdb.dealer.orders(order_date, code);