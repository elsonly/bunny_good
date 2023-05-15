DROP TABLE IF EXISTS tsdb.cmoney.daily_price;
CREATE TABLE tsdb.cmoney.daily_price(
    tdate date NOT NULL,
    code varchar(10) NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume bigint,
    cnt bigint, 
    amt bigint, -- in thousands
    amt_ratio double precision,
    shares bigint, -- in million
    market_value double precision, -- in 1000 m
    pe double precision,
    pb double precision,
    pe_4q double precision,
    turnover double precision,
    up_down_limit smallint
);
SELECT create_hypertable(
        'tsdb.cmoney.daily_price',
        'tdate',
        partitioning_column => 'code',
        number_partitions => 1,
        chunk_time_interval => INTERVAL '30 day'
    );
ALTER TABLE tsdb.cmoney.daily_price
SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'code'
    );
SELECT add_compression_policy('tsdb.cmoney.daily_price', INTERVAL '7 days');

-- select * from tsdb.cmoney.daily_price where code = '2330' order by tdate desc;
-- delete from tsdb.cmoney.daily_price where tdate > '2023-01-01';