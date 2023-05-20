DROP TABLE IF EXISTS tsdb.cmoney.institute_fund;
CREATE TABLE tsdb.cmoney.institute_fund(
    code VARCHAR(10) NOT NULL,
    tdate date NOT NULL,
    buy double precision,
    sell double precision,
    net double precision,
    position double precision,
    buy_amt double precision,
    sell_amt double precision,
    net_amt double precision,
    buy_avg_prc double precision,
    sell_avg_prc double precision,
    holding_ratio double precision,
    holding_mkt_value double precision,
    holding_avg_prc double precision
);
SELECT create_hypertable(
        'tsdb.cmoney.institute_fund',
        'tdate',
        partitioning_column => 'code',
        number_partitions => 1,
        chunk_time_interval => INTERVAL '30 day'
    );
ALTER TABLE tsdb.cmoney.institute_fund
SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'code'
    );
SELECT add_compression_policy('tsdb.cmoney.institute_fund', INTERVAL '7 days');
comment on column tsdb.cmoney.institute_fund.code is 'stock code';
comment on column tsdb.cmoney.institute_fund.tdate is 'trading date';
comment on column tsdb.cmoney.institute_fund.buy is '投信買張';
comment on column tsdb.cmoney.institute_fund.sell is '投信賣張';
comment on column tsdb.cmoney.institute_fund.net is '投信買賣超';
comment on column tsdb.cmoney.institute_fund.position is '投信庫存';
comment on column tsdb.cmoney.institute_fund.buy_amt is '投信買金額(千)';
comment on column tsdb.cmoney.institute_fund.sell_amt is '投信賣金額(千)';
comment on column tsdb.cmoney.institute_fund.net_amt is '投信買賣超金額(千)';
comment on column tsdb.cmoney.institute_fund.buy_avg_prc is '投信買均價';
comment on column tsdb.cmoney.institute_fund.sell_avg_prc is '投信賣均價';
comment on column tsdb.cmoney.institute_fund.holding_ratio is '投信持股比率(%)';
comment on column tsdb.cmoney.institute_fund.holding_mkt_value is '投信持股市值(百萬)';
comment on column tsdb.cmoney.institute_fund.holding_avg_prc is '投信持股成本';