DROP TABLE IF EXISTS tsdb.twse.stock_info;
CREATE TABLE tsdb.twse.stock_info(
    code varchar(20) not null primary key,
    name name not null,
    sec_type name,
    listed_type varchar(10),
    isin varchar(12),
    ind name,
    ipo_date date,
    cfic varchar(10),
    memo text,
    upd_date date not null
);

-- select * from tsdb.twse.stock_info limit 10;
