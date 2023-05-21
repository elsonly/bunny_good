from typing import List, Tuple
import json


def gensql(
    db: str,
    schema: str,
    table: str,
    columns: List[Tuple[str, str, str, str]],
    create_index: List[List[str]] = [],
    create_hypertable: bool = False,
    time_column: str = "",
    partitioning_column: str = "",
):
    """
    colume: (column_name, data_type, original_table_name, original_column_name)
    ex: ('code', 'varchar', '日外資持股與排行', '股票代號')
    """
    sql = f"DROP TABLE IF EXISTS {db}.{schema}.{table};\n"
    sql += f"CREATE TABLE  {db}.{schema}.{table}("
    for col in columns:
        sql += f"{col[0]} {col[1]},"
    sql = sql[:-1]
    sql += ");\n"

    if create_index:
        for indexes in create_index:
            if len(indexes) == 1:
                sql += f"CREATE INDEX idx_{table}_{indexes[0]} ON {db}.{schema}.{table}({indexes[0]});\n"
            elif len(indexes) == 2:
                sql += f"CREATE INDEX idx_{table}_{indexes[0]}_{indexes[1]} ON {db}.{schema}.{table}({indexes[0]}, {indexes[1]});\n"

    if create_hypertable:
        sql += f"""SELECT create_hypertable(
            '{db}.{schema}.{table}', 
            '{time_column}', 
            partitioning_column => '{partitioning_column}', 
            number_partitions => 1,
            chunk_time_interval => INTERVAL '30 day'
        );
        ALTER TABLE {db}.{schema}.{table}
        SET (
                timescaledb.compress,
                timescaledb.compress_segmentby = '{partitioning_column}'
            );
        SELECT add_compression_policy('{db}.{schema}.{table}', INTERVAL '7 days');\n"""

    for col in columns:
        sql += f"comment on column {db}.{schema}.{table}.{col[0]} is '{col[-1]}';\n"

    return sql


def genitems(
    columns: List[Tuple[str, str, str, str]],
) -> dict:
    """
    colume: (column_name, data_type, original_table_name, original_column_name)
    ex: ('code', 'varchar', '日外資持股與排行', '股票代號')
    """
    d = {}
    for col in columns:
        if col[-1] == "":
            continue
        d[col[-1]] = col[-2]
    return d


def gencolumn_mapping(
    columns: List[Tuple[str, str, str, str]],
) -> dict:
    """
    colume: (column_name, data_type, original_table_name, original_column_name)
    ex: ('code', 'varchar', '日外資持股與排行', '股票代號')
    """
    d = {}
    for col in columns:
        if col[-1] == "":
            continue
        d[col[-1]] = col[0]
    return d


def gencode(
    db: str,
    schema: str,
    table: str,
    columns: List[Tuple[str, str, str, str]],
    create_index: List[List[str]] = [],
    create_hypertable: bool = False,
    time_column: str = "",
    partitioning_column: str = "",
    output_path: str = "./timescaledb/script/build",
):
    """
    colume: (column_name, data_type, original_table_name, original_column_name)
    ex: ('code', 'varchar', '日外資持股與排行', '股票代號')
    """
    sql = gensql(
        db,
        schema,
        table,
        columns,
        create_index,
        create_hypertable,
        time_column,
        partitioning_column,
    )
    d_items = genitems(columns)
    d_col_mapping = gencolumn_mapping(columns)

    with open(f"{output_path}/gen.sql", "w") as f:
        f.buffer.write(sql.encode("utf-8"))

    with open(f"{output_path}/gen.py", "w") as f:
        f.buffer.write(
            json.dumps(d_items, indent=4, ensure_ascii=False).encode("utf-8")
        )
        f.buffer.write(
            json.dumps(d_col_mapping, indent=4, ensure_ascii=False).encode("utf-8")
        )


if __name__ == "__main__":
    gencode(
        "tsdb",
        "cmoney",
        "margin_short",
        [
            ("code", "VARCHAR(10) NOT NULL", "日融資券排行", "stock code"),
            ("tdate", "date NOT NULL", "日融資券排行", "trading date"),
            ("margin_buy", "INT", "日融資券排行", "資買"),
            ("margin_sell", "INT", "日融資券排行", "資賣"),
            ("margin_redemption", "INT", "日融資券排行", "資現償"),
            ("margin_balance", "INT", "日融資券排行", "資餘"),
            ("margin_balance_change", "INT", "日融資券排行", "資增減"),
            ("margin_limit", "INT", "日融資券排行", "資限"),
            ("short_buy", "INT", "日融資券排行", "券買"),
            ("short_sell", "INT", "日融資券排行", "券賣"),
            ("short_sell_amount", "INT", "日融資券排行", "券賣金額(千)"),
            ("short_sell_redemption", "INT", "日融資券排行", "券現償"),
            ("short_balance", "INT", "日融資券排行", "券餘"),
            ("short_balance_change", "INT", "日融資券排行", "券增減"),
            ("margin_short_offset", "INT", "日融資券排行", "資券相抵"),
            ("short_margin_ratio", "double precision", "日融資券排行", "券資比"),
            ("margin_utilization_rate", "double precision", "日融資券排行", "資使用率"),
            ("short_utilization_rate", "double precision", "日融資券排行", "券使用率"),
            ("day_trading_ratio", "double precision", "日融資券排行", "當沖比率"),
            ("margin_short_remarks", "varchar(10)", "日融資券排行", "資券註"),
            ("sb_short_sell", "INT", "日融資券排行", "借券賣出"),
            ("sb_short_sell_amount", "INT", "日融資券排行", "借券賣出金額(千)"),
            ("sb_short_sell_return", "INT", "日融資券排行", "借券賣出還券"),
            ("sb_short_sell_adjustment", "INT", "日融資券排行", "借券賣出調整"),
            ("sb_short_sell_inventory_change", "INT", "日融資券排行", "借券賣出庫存異動"),
            ("sb_short_sell_balance", "INT", "日融資券排行", "借券賣出餘額"),
            ("sb_short_sell_available_limit", "INT", "日融資券排行", "借券可使用額度"),
            ("sb_system_daily_borrowing", "INT", "日融資券排行", "借券系統當日借券"),
            ("sb_system_daily_return", "INT", "日融資券排行", "借券系統當日還券"),
            ("sb_system_balance_change", "INT", "日融資券排行", "借券系統借券餘額異動"),
            ("sb_system_balance", "INT", "日融資券排行", "借券系統借券餘額"),
            ("sb_system_balance_market_value", "INT", "日融資券排行", "借券系統借券餘額市值"),
            ("sb_broker_daily_borrowing", "INT", "日融資券排行", "證商營業處所當日借券"),
            ("sb_broker_daily_return", "INT", "日融資券排行", "證商營業處所當日還券"),
            ("sb_broker_balance_change", "INT", "日融資券排行", "證商營業處所借券餘額異動"),
            ("sb_broker_balance", "INT", "日融資券排行", "證商營業處所借券餘額"),
            ("sb_broker_balance_market_value", "INT", "日融資券排行", "證商營業處所借券餘額市值"),
            ("sb_margin_account_daily_borrowing", "INT", "日融資券排行", "借貸專戶當日借券"),
            ("sb_margin_account_daily_return", "INT", "日融資券排行", "借貸專戶當日還券"),
            ("sb_margin_account_balance_change", "INT", "日融資券排行", "借貸專戶借券餘額異動"),
            ("sb_margin_account_balance", "INT", "日融資券排行", "借貸專戶借券餘額"),
            ("sb_margin_account_balance_market_value", "INT", "日融資券排行", "借貸專戶借券餘額市值"),
            ("estimated_margin_cost", "double precision", "日融資券排行", "融資成本(推估)"),
            ("estimated_short_sell_cost", "double precision", "日融資券排行", "融券成本(推估)"),
            ("margin_maintenance_rate", "double precision", "日融資券排行", "融資維持率(%)"),
            ("short_sell_maintenance_rate", "double precision", "日融資券排行", "融券維持率(%)"),
            ("overall_maintenance_rate", "double precision", "日融資券排行", "整體維持率(%)"),
        ],
        # create_index=[["code"]],
        create_hypertable=True,
        time_column="tdate",
        partitioning_column="code",
    )
