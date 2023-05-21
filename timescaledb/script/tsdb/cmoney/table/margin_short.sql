DROP TABLE IF EXISTS tsdb.cmoney.margin_short;
CREATE TABLE tsdb.cmoney.margin_short(
    code VARCHAR(10) NOT NULL,
    tdate date NOT NULL,
    margin_buy INT,
    margin_sell INT,
    margin_redemption INT,
    margin_balance INT,
    margin_balance_change INT,
    margin_limit INT,
    short_buy INT,
    short_sell INT,
    short_sell_amount INT,
    short_sell_redemption INT,
    short_balance INT,
    short_balance_change INT,
    margin_short_offset INT,
    short_margin_ratio double precision,
    margin_utilization_rate double precision,
    short_utilization_rate double precision,
    day_trading_ratio double precision,
    margin_short_remarks varchar(10),
    sb_short_sell INT,
    sb_short_sell_amount INT,
    sb_short_sell_return INT,
    sb_short_sell_adjustment INT,
    sb_short_sell_inventory_change INT,
    sb_short_sell_balance INT,
    sb_short_sell_available_limit INT,
    sb_system_daily_borrowing INT,
    sb_system_daily_return INT,
    sb_system_balance_change INT,
    sb_system_balance INT,
    sb_system_balance_market_value INT,
    sb_broker_daily_borrowing INT,
    sb_broker_daily_return INT,
    sb_broker_balance_change INT,
    sb_broker_balance INT,
    sb_broker_balance_market_value INT,
    sb_margin_account_daily_borrowing INT,
    sb_margin_account_daily_return INT,
    sb_margin_account_balance_change INT,
    sb_margin_account_balance INT,
    sb_margin_account_balance_market_value INT,
    estimated_margin_cost double precision,
    estimated_short_sell_cost double precision,
    margin_maintenance_rate double precision,
    short_sell_maintenance_rate double precision,
    overall_maintenance_rate double precision
);
SELECT create_hypertable(
        'tsdb.cmoney.margin_short',
        'tdate',
        partitioning_column => 'code',
        number_partitions => 1,
        chunk_time_interval => INTERVAL '30 day'
    );
ALTER TABLE tsdb.cmoney.margin_short
SET (
        timescaledb.compress,
        timescaledb.compress_segmentby = 'code'
    );
SELECT add_compression_policy('tsdb.cmoney.margin_short', INTERVAL '7 days');
comment on column tsdb.cmoney.margin_short.code is 'stock code';
comment on column tsdb.cmoney.margin_short.tdate is 'trading date';
comment on column tsdb.cmoney.margin_short.margin_buy is '資買';
comment on column tsdb.cmoney.margin_short.margin_sell is '資賣';
comment on column tsdb.cmoney.margin_short.margin_redemption is '資現償';
comment on column tsdb.cmoney.margin_short.margin_balance is '資餘';
comment on column tsdb.cmoney.margin_short.margin_balance_change is '資增減';
comment on column tsdb.cmoney.margin_short.margin_limit is '資限';
comment on column tsdb.cmoney.margin_short.short_buy is '券買';
comment on column tsdb.cmoney.margin_short.short_sell is '券賣';
comment on column tsdb.cmoney.margin_short.short_sell_amount is '券賣金額(千)';
comment on column tsdb.cmoney.margin_short.short_sell_redemption is '券現償';
comment on column tsdb.cmoney.margin_short.short_balance is '券餘';
comment on column tsdb.cmoney.margin_short.short_balance_change is '券增減';
comment on column tsdb.cmoney.margin_short.margin_short_offset is '資券相抵';
comment on column tsdb.cmoney.margin_short.short_margin_ratio is '券資比';
comment on column tsdb.cmoney.margin_short.margin_utilization_rate is '資使用率';
comment on column tsdb.cmoney.margin_short.short_utilization_rate is '券使用率';
comment on column tsdb.cmoney.margin_short.day_trading_ratio is '當沖比率';
comment on column tsdb.cmoney.margin_short.margin_short_remarks is '資券註';
comment on column tsdb.cmoney.margin_short.sb_short_sell is '借券賣出';
comment on column tsdb.cmoney.margin_short.sb_short_sell_amount is '借券賣出金額(千)';
comment on column tsdb.cmoney.margin_short.sb_short_sell_return is '借券賣出還券';
comment on column tsdb.cmoney.margin_short.sb_short_sell_adjustment is '借券賣出調整';
comment on column tsdb.cmoney.margin_short.sb_short_sell_inventory_change is '借券賣出庫存異動';
comment on column tsdb.cmoney.margin_short.sb_short_sell_balance is '借券賣出餘額';
comment on column tsdb.cmoney.margin_short.sb_short_sell_available_limit is '借券可使用額度';
comment on column tsdb.cmoney.margin_short.sb_system_daily_borrowing is '借券系統當日借券';
comment on column tsdb.cmoney.margin_short.sb_system_daily_return is '借券系統當日還券';
comment on column tsdb.cmoney.margin_short.sb_system_balance_change is '借券系統借券餘額異動';
comment on column tsdb.cmoney.margin_short.sb_system_balance is '借券系統借券餘額';
comment on column tsdb.cmoney.margin_short.sb_system_balance_market_value is '借券系統借券餘額市值';
comment on column tsdb.cmoney.margin_short.sb_broker_daily_borrowing is '證商營業處所當日借券';
comment on column tsdb.cmoney.margin_short.sb_broker_daily_return is '證商營業處所當日還券';
comment on column tsdb.cmoney.margin_short.sb_broker_balance_change is '證商營業處所借券餘額異動';
comment on column tsdb.cmoney.margin_short.sb_broker_balance is '證商營業處所借券餘額';
comment on column tsdb.cmoney.margin_short.sb_broker_balance_market_value is '證商營業處所借券餘額市值';
comment on column tsdb.cmoney.margin_short.sb_margin_account_daily_borrowing is '借貸專戶當日借券';
comment on column tsdb.cmoney.margin_short.sb_margin_account_daily_return is '借貸專戶當日還券';
comment on column tsdb.cmoney.margin_short.sb_margin_account_balance_change is '借貸專戶借券餘額異動';
comment on column tsdb.cmoney.margin_short.sb_margin_account_balance is '借貸專戶借券餘額';
comment on column tsdb.cmoney.margin_short.sb_margin_account_balance_market_value is '借貸專戶借券餘額市值';
comment on column tsdb.cmoney.margin_short.estimated_margin_cost is '融資成本(推估)';
comment on column tsdb.cmoney.margin_short.estimated_short_sell_cost is '融券成本(推估)';
comment on column tsdb.cmoney.margin_short.margin_maintenance_rate is '融資維持率(%)';
comment on column tsdb.cmoney.margin_short.short_sell_maintenance_rate is '融券維持率(%)';
comment on column tsdb.cmoney.margin_short.overall_maintenance_rate is '整體維持率(%)';