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
        "institute_fund",
        [
            ("code", "VARCHAR(10) NOT NULL", "", "stock code"),
            ("tdate", "date NOT NULL", "日投信明細與排行", "trading date"),
            ("buy", "double precision", "日投信明細與排行", "投信買張"),
            ("sell", "double precision", "日投信明細與排行", "投信賣張"),
            ("net", "double precision", "日投信明細與排行", "投信買賣超"),
            ("position", "double precision", "日投信明細與排行", "投信庫存"),
            ("buy_amt", "double precision", "日投信明細與排行", "投信買金額(千)"),
            ("sell_amt", "double precision", "日投信明細與排行", "投信賣金額(千)"),
            ("net_amt", "double precision", "日投信明細與排行", "投信買賣超金額(千)"),
            ("buy_avg_prc", "double precision", "日投信明細與排行", "投信買均價"),
            ("sell_avg_prc", "double precision", "日投信明細與排行", "投信賣均價"),
            ("holding_ratio", "double precision", "日投信明細與排行", "投信持股比率(%)"),
            ("holding_mkt_value", "double precision", "日投信明細與排行", "投信持股市值(百萬)"),
            ("holding_avg_prc", "double precision", "日投信明細與排行", "投信持股成本"),
        ],
        #create_index=[["code"]],
        create_hypertable=True,
        time_column="tdate",
        partitioning_column="code",
    )
