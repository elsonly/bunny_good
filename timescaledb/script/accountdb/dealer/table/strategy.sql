DROP TABLE IF EXISTS accountdb.dealer.strategy;
CREATE TABLE accountdb.dealer.strategy(
    id SERIAL PRIMARY KEY,
    name varchar,
    add_date date DEFAULT CURRENT_DATE,
    status boolean,
    leverage_ratio double precision,
    expected_mdd double precision,
    expected_daily_return double precision,
    holding_period int,
    order_low_ratio double precision
);