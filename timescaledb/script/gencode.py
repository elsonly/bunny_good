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
        "holidays",
        [
            ("country_code", "name NOT NULL", "金融市場假日表", "country code"),
            ("hdate", "date", "金融市場假日表", "日期"),
            ("name", "name", "金融市場假日表", "假日名稱"),
            ("week", "smallint", "金融市場假日表", "星期"),
            ("is_dayoff", "smallint", "金融市場假日表", "是否放假"),
            ("country", "name", "金融市場假日表", "國家"),
        ],
        # create_index=[["code"]],
        create_hypertable=False,
        #time_column="tdate",
        #partitioning_column="code",
    )
