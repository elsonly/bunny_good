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
        "dividend_policy",
        [
            ("code", "VARCHAR(10) NOT NULL", "", "stock code"),
            ("year", "INT NOT NULL", "股利政策表", "年度"),
            ("distribution_frequency", "smallint", "股利政策表", "配發次數"),
            ("ex_rights_date", "date", "股利政策表", "除權日"),
            ("ex_rights_last_compensation_date", "date", "股利政策表", "除權最後回補日"),
            ("ex_dividend_date", "date", "股利政策表", "除息日"),
            ("ex_dividend_last_compensation_date", "date", "股利政策表", "除息最後回補日"),
            ("ex_rights_allotment_reference_date", "date", "股利政策表", "除權分派基準日"),
            ("ex_dividend_allotment_reference_date", "date", "股利政策表", "除息分派基準日"),
            ("share_receipt_date", "date", "股利政策表", "領股日期"),
            ("dividend_receipt_date", "date", "股利政策表", "領息日期"),
            ("earnings_stock_dividend", "double precision", "股利政策表", "盈餘配股(元)"),
            ("surplus_stock_dividend", "double precision", "股利政策表", "公積配股(元)"),
            ("total_stock_dividend", "double precision", "股利政策表", "股票股利合計(元)"),
            ("earnings_cash_dividend", "double precision", "股利政策表", "盈餘配息(元)"),
            ("surplus_cash_dividend", "double precision", "股利政策表", "公積配息(元)"),
            ("total_cash_dividend", "double precision", "股利政策表", "現金股利合計(元)"),
            ("total_dividend", "double precision", "股利政策表", "股利合計(元)"),
            ("stock_dividend_payout_ratio", "double precision", "股利政策表", "股票股利發放率(%)"),
            ("cash_dividend_payout_ratio", "double precision", "股利政策表", "現金股利發放率(%)"),
            ("dividend_payout_ratio", "double precision", "股利政策表", "股利發放率(%)"),
            ("ex_rights_opening_reference_price", "double precision", "股利政策表", "除權開盤競價基準"),
            ("ex_dividend_opening_reference_price", "double precision", "股利政策表", "除息開盤競價基準"),
            ("ex_rights_reference_price", "double precision", "股利政策表", "除權參考價"),
            ("ex_dividend_reference_price", "double precision", "股利政策表", "除息參考價"),
            ("pre_ex_rights_stock_price", "double precision", "股利政策表", "除權前股價"),
            ("pre_ex_dividend_stock_price", "double precision", "股利政策表", "除息前股價"),
            ("pre_ex_rights_share_capital", "double precision", "股利政策表", "除權前股本(百萬)"),
            ("post_ex_rights_share_capital", "double precision", "股利政策表", "除權後股本(百萬)"),
            ("pre_ex_rights_market_value_ratio", "double precision", "股利政策表", "除權前市值比重(%)"),
            ("pre_ex_dividend_market_value_ratio", "double precision", "股利政策表", "除息前市值比重(%)"),
            ("cash_dividend_yield", "double precision", "股利政策表", "現金股利殖利率(%)"),
            ("total_shareholders_stock_dividend_allotment_shares", "INT", "股利政策表", "股東股票股利總配股數(張)"),
            ("total_shareholders_cash_dividend_amount", "INT", "股利政策表", "股東現金紅利總金額(千)"),
            ("employee_compensation_stock_allotment_shares", "INT", "股利政策表", "員工酬勞配股(張)"),
            ("employee_stock_allotment_amount", "INT", "股利政策表", "員工配股金額(千)"),
            ("employee_bonus_stock_allotment_ratio_to_earnings_stock_dividend", "double precision", "股利政策表", "員工紅利配股佔盈餘配股比例(%)"),
            ("employee_cash_compensation", "INT", "股利政策表", "員工酬勞現金(千)"),
            ("directors_and_supervisors_compensation", "INT", "股利政策表", "董監酬勞(千)"),
            ("compensation_difference", "INT", "股利政策表", "酬勞差異數(千)"),
            ("eps_after_deducting_dividends_and_directors_compensation", "double precision", "股利政策表", "扣除紅利及董監酬勞後之EPS"),
            ("board_remarks", "text", "股利政策表", "董事會備註"),
            ("shareholders_meeting_remarks", "text", "股利政策表", "股東會備註"),
            ("dividend_distribution_date_approved_by_the_board_of_directors", "date", "股利政策表", "董事會決議通過股利分派日"),
            ("shareholders_meeting_date", "date", "股利政策表", "股東會日期"),
            ("announcement_date", "date", "股利政策表", "公告日期"),
            ("ex_rights_announcement_date", "date", "股利政策表", "除權公告日期"),
            ("ex_dividend_announcement_date", "date", "股利政策表", "除息公告日期"),
            ("rights_offering_date_for_capital_increase", "date", "股利政策表", "現增除權日"),
            ("type_of_capital_increase", "varchar(20)", "股利政策表", "現增類別"),
            ("subscription_price_for_capital_increase", "double precision", "股利政策表", "現增認購價"),
            ("stock_allotment_for_capital_increase_shares", "double precision", "股利政策表", "現增配股(股)"),
            ("total_amount_for_capital_increase", "INT", "股利政策表", "現增總額(百萬)"),
            ("year_of_directors_and_supervisors_resignation_and_election", "INT", "股利政策表", "董監改選年度"),
        ],
        create_index=[["code"], ["year", "code"]],
        #create_hypertable=False,
        #time_column="tdate",
        #partitioning_column="code",
    )
