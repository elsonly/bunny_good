DROP TABLE IF EXISTS accountdb.dealer.strategy;
CREATE TABLE accountdb.dealer.strategy(
    id SERIAL PRIMARY KEY,
    name varchar not null,
    factor name,
    add_date date not null DEFAULT CURRENT_DATE,
    status boolean not null DEFAULT false,
    enable_raise boolean not null DEFAULT false,
    enable_dividend boolean not null DEFAULT false,
    leverage_ratio double precision,
    expected_mdd double precision,
    expected_daily_return double precision,
    holding_period int,
    order_low_ratio double precision,
    exit_stop_loss double precision,
    exit_take_profit double precision,
    exit_dp_days int,
    exit_dp_profit_limit double precision,
);
