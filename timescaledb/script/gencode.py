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
        "institute_dealer",
        [
            ("dvd_year", "date NOT NULL", "", "年度"),
            ("dvd_num", "varchar(10) NOT NULL", "", "配發次數"),
            ("ex_date", "double precision", "日自營商進出排行", "除權日"),
            ("sell", "double precision", "日自營商進出排行", "除權最後回補日"),
            ("net", "double precision", "日自營商進出排行", "除息日"),
            ("buy_self", "double precision", "日自營商進出排行", "除息最後回補日"),
            ("sell_self", "double precision", "日自營商進出排行", "除權分派基準日"),
            ("net_self", "double precision", "日自營商進出排行", "除息分派基準日"),
            ("buy_hedge", "double precision", "日自營商進出排行", "領股日期"),
            ("sell_hedge", "double precision", "日自營商進出排行", "領息日期"),
            ("net_hedge", "double precision", "日自營商進出排行", "盈餘配股(元)"),
            ("position", "double precision", "日自營商進出排行", "公積配股(元)"),
            ("buy_amt", "double precision", "日自營商進出排行", "股票股利合計(元)"),
            ("sell_amt", "double precision", "日自營商進出排行", "盈餘配息(元)"),
            ("net_amt", "double precision", "日自營商進出排行", "公積配息(元)"),
            ("buy_avg_prc", "double precision", "日自營商進出排行", "現金股利合計(元)"),
            ("sell_avg_prc", "double precision", "日自營商進出排行", "股利合計(元)"),
            ("holding_ratio", "double precision", "日自營商進出排行", "股票股利發放率(%)"),
            ("holding_mkt_value", "double precision", "日自營商進出排行", "現金股利發放率(%)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "股利發放率(%)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除權開盤競價基準"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除息開盤競價基準"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除權參考價"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除息參考價"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除權前股價"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除息前股價"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除權前股本(百萬)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除權後股本(百萬)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除權前市值比重(%)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除息前市值比重(%)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "現金股利殖利率(%)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "股東股票股利總配股數(張)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "股東現金紅利總金額(千)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "員工酬勞配股(張)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "員工配股金額(千)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "員工紅利配股佔盈餘配股比例(%)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "員工酬勞現金(千)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "董監酬勞(千)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "酬勞差異數(千)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "扣除紅利及董監酬勞後之EPS"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "董事會備註"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "股東會備註"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "董事會決議通過股利分派日"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "股東會日期"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "公告日期"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除權公告日期"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "除息公告日期"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "現增除權日"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "現增類別"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "現增認購價"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "現增配股(股)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "現增總額(百萬)"),
            ("holding_avg_prc", "double precision", "日自營商進出排行", "董監改選年度"),
        ],
        create_index=[],
        create_hypertable=True,
        time_column="tdate",
        partitioning_column="code",
    )
