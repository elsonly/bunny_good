DROP TABLE IF EXISTS tsdb.cmoney.institute_dealer;

CREATE TABLE
    tsdb.cmoney.institute_dealer(
        tdate date NOT NULL,
        code varchar(10) NOT NULL,
        buy double precision,
        sell double precision,
        net double precision,
        buy_self double precision,
        sell_self double precision,
        net_self double precision,
        buy_hedge double precision,
        sell_hedge double precision,
        net_hedge double precision,
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

SELECT
    create_hypertable(
        'tsdb.cmoney.institute_dealer',
        'tdate',
        partitioning_column => 'code',
        number_partitions => 1,
        chunk_time_interval => INTERVAL '30 day'
    );

ALTER TABLE
    tsdb.cmoney.institute_dealer
SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'code'
    );

SELECT
    add_compression_policy(
        'tsdb.cmoney.institute_dealer',
        INTERVAL '7 days'
    );

comment
    on column tsdb.cmoney.institute_dealer.tdate is 'trading date';

comment on column tsdb.cmoney.institute_dealer.code is 'stock code';

comment on column tsdb.cmoney.institute_dealer.buy is '自營商買張';

comment on column tsdb.cmoney.institute_dealer.sell is '自營商賣張';

comment on column tsdb.cmoney.institute_dealer.net is '自營商買賣超';

comment
    on column tsdb.cmoney.institute_dealer.buy_self is '自營商買張(自行買賣)';

comment
    on column tsdb.cmoney.institute_dealer.sell_self is '自營商賣張(自行買賣)';

comment
    on column tsdb.cmoney.institute_dealer.net_self is '自營商買賣超(自行買賣)';

comment
    on column tsdb.cmoney.institute_dealer.buy_hedge is '自營商買張(避險)';

comment
    on column tsdb.cmoney.institute_dealer.sell_hedge is '自營商賣張(避險)';

comment
    on column tsdb.cmoney.institute_dealer.net_hedge is '自營商買賣超(避險)';

comment on column tsdb.cmoney.institute_dealer.position is '自營商庫存';

comment
    on column tsdb.cmoney.institute_dealer.buy_amt is '自營商買金額(千)';

comment
    on column tsdb.cmoney.institute_dealer.sell_amt is '自營商賣金額(千)';

comment
    on column tsdb.cmoney.institute_dealer.net_amt is '自營商買賣超金額(千)';

comment
    on column tsdb.cmoney.institute_dealer.buy_avg_prc is '自營商買均價';

comment
    on column tsdb.cmoney.institute_dealer.sell_avg_prc is '自營商賣均價';

comment
    on column tsdb.cmoney.institute_dealer.holding_ratio is '自營商持股比率(%)';

comment
    on column tsdb.cmoney.institute_dealer.holding_mkt_value is '自營商持股市值(百萬)';

comment
    on column tsdb.cmoney.institute_dealer.holding_avg_prc is '自營商持股成本';


-- select * from tsdb.cmoney.institute_dealer;