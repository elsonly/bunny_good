DROP TABLE IF EXISTS tsdb.sino.contracts;
CREATE TABLE tsdb.sino.contracts(
    security_type name,
    exchange name,
    code name NOT NULL PRIMARY KEY,
    symbol name,
    name name,
    category name,
    currency name,
    delivery_month varchar(10),
    delivery_date date,
    strike_price double precision,
    option_right  name,
    underlying_kind name,
    underlying_code name,
    unit INTEGER,
    multiplier INTEGER,
    limit_up double precision,
    limit_down double precision,
    reference double precision,
    update_date date,
    margin_trading_balance INTEGER,
    short_selling_balance INTEGER,
    day_trade name,
    target_code name
);

-- select * from tsdb.sino.contracts limit 10;
