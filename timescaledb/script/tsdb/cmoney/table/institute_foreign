DROP TABLE IF EXISTS tsdb.cmoney.institute_foreign;
CREATE TABLE tsdb.cmoney.institute_foreign(
    tdate date NOT NULL,
    code varchar(10) NOT NULL,
    buy double precision,
    sell double precision,
    net double precision,
    holding_chg double precision,
    holding_chg_shares double precision,
    buy_ex_dealer double precision,
    sell_ex_dealer double precision,
    net_ex_dealer double precision,
    buy_dealer double precision,
    sell_dealer double precision,
    net_dealer double precision,
    buy_amt double precision,
    sell_amt double precision,
    net_amt double precision,
    buy_avg_prc double precision,
    sell_avg_prc double precision,
    holding_ratio double precision,
    holding_mkt_value double precision,
    holding_avg_prc double precision,
    avalible_shares double precision,
    avalible_ratio double precision,
    avalible_limit double precision,
    avalible_limit_cn double precision,
    reason_for_chg text
);
SELECT create_hypertable(
        'tsdb.cmoney.institute_foreign',
        'tdate',
        partitioning_column => 'code',
        number_partitions => 1,
        chunk_time_interval => INTERVAL '30 day'
    );
ALTER TABLE tsdb.cmoney.institute_foreign
SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'code'
    );
SELECT add_compression_policy('tsdb.cmoney.institute_foreign', INTERVAL '7 days');


comment on column cmoney.institute_foreign.tdate is 'trading date';
comment on column cmoney.institute_foreign.code is 'stock code';
comment on column cmoney.institute_foreign.buy is '外資買張';
comment on column cmoney.institute_foreign.sell is '外資賣張';
comment on column cmoney.institute_foreign.net is '外資買賣超';
comment on column cmoney.institute_foreign.holding_chg is '外資持股異動';
comment on column cmoney.institute_foreign.holding_chg_shares is '外資持股張數';
comment on column cmoney.institute_foreign.buy_ex_dealer is '外資及陸資(不含外資自營商)買張';
comment on column cmoney.institute_foreign.sell_ex_dealer is '外資及陸資(不含外資自營商)賣張';
comment on column cmoney.institute_foreign.net_ex_dealer is '外資及陸資(不含外資自營商)買賣超';
comment on column cmoney.institute_foreign.buy_dealer is '外資自營商買張';
comment on column cmoney.institute_foreign.sell_dealer is '外資自營商賣張';
comment on column cmoney.institute_foreign.net_dealer is '外資自營商買賣超';
comment on column cmoney.institute_foreign.buy_amt is '外資買金額(千)';
comment on column cmoney.institute_foreign.sell_amt is '外資賣金額(千)';
comment on column cmoney.institute_foreign.net_amt is '外資買賣超金額(千)';
comment on column cmoney.institute_foreign.buy_avg_prc is '外資買均價';
comment on column cmoney.institute_foreign.sell_avg_prc is '外資賣均價';
comment on column cmoney.institute_foreign.holding_ratio is '外資持股比率(%)';
comment on column cmoney.institute_foreign.holding_mkt_value is '外資持股市值(百萬)';
comment on column cmoney.institute_foreign.holding_avg_prc is '外資持股成本';
comment on column cmoney.institute_foreign.avalible_shares is '外資尚可投資張數';
comment on column cmoney.institute_foreign.avalible_ratio is '外資尚可投資比率(%)';
comment on column cmoney.institute_foreign.avalible_limit is '外資投資上限比率(%)';
comment on column cmoney.institute_foreign.avalible_limit_cn is '陸資投資上限比率(%)';
comment on column cmoney.institute_foreign.reason_for_chg is '與前日異動原因';


-- select * from cmoney.institute_foreign where code = '1102' order by tdate desc;
-- select * from ft_get_table_description('institute_foreign');

