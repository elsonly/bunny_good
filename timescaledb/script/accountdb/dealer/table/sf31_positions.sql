DROP TABLE IF EXISTS accountdb.dealer.sf31_positions;
CREATE TABLE accountdb.dealer.sf31_positions(
    trader_id varchar(10),
    ptime time,
    security_type char(1),
    code varchar(10) primary key,
    action char(1),
    shares INT,
    avg_price double precision,
    closed_pnl double precision,
    open_pnl double precision,
    pnl_chg double precision,
    cum_return double precision
);
