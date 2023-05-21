from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
import xlwings as xw
import pandas as pd
from typing import Dict, List
from pathlib import Path

from bunny_good.database.data_manager import DataManager
from bunny_good.services.prefect_agent.utils import flow_error_handle


def get_workbook_path() -> Path:
    try:
        name = Path(__file__).absolute().name.replace(".py", "")
        wb_path = Path(__file__).parent.joinpath(f"docs/{name}.xlsm")
    except:
        wb_path = (
            Path()
            .absolute()
            .joinpath(
                "bunny_good/services/prefect_agent/cmoney/docs/dividend_policy.xlsm"
            )
        )
    return wb_path


@task(name="task-dividend_policy-update_workbook", retries=3, retry_delay_seconds=3)
def update_workbook(
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
    periods: List[pd.Timestamp] = [],
    validate_date: bool = False,
):
    logger = get_run_logger()
    items = {
        "年度": "股利政策表",
        "配發次數": "股利政策表",
        "除權日": "股利政策表",
        "除權最後回補日": "股利政策表",
        "除息日": "股利政策表",
        "除息最後回補日": "股利政策表",
        "除權分派基準日": "股利政策表",
        "除息分派基準日": "股利政策表",
        "領股日期": "股利政策表",
        "領息日期": "股利政策表",
        "盈餘配股(元)": "股利政策表",
        "公積配股(元)": "股利政策表",
        "股票股利合計(元)": "股利政策表",
        "盈餘配息(元)": "股利政策表",
        "公積配息(元)": "股利政策表",
        "現金股利合計(元)": "股利政策表",
        "股利合計(元)": "股利政策表",
        "股票股利發放率(%)": "股利政策表",
        "現金股利發放率(%)": "股利政策表",
        "股利發放率(%)": "股利政策表",
        "除權開盤競價基準": "股利政策表",
        "除息開盤競價基準": "股利政策表",
        "除權參考價": "股利政策表",
        "除息參考價": "股利政策表",
        "除權前股價": "股利政策表",
        "除息前股價": "股利政策表",
        "除權前股本(百萬)": "股利政策表",
        "除權後股本(百萬)": "股利政策表",
        "除權前市值比重(%)": "股利政策表",
        "除息前市值比重(%)": "股利政策表",
        "現金股利殖利率(%)": "股利政策表",
        "股東股票股利總配股數(張)": "股利政策表",
        "股東現金紅利總金額(千)": "股利政策表",
        "員工酬勞配股(張)": "股利政策表",
        "員工配股金額(千)": "股利政策表",
        "員工紅利配股佔盈餘配股比例(%)": "股利政策表",
        "員工酬勞現金(千)": "股利政策表",
        "董監酬勞(千)": "股利政策表",
        "酬勞差異數(千)": "股利政策表",
        "扣除紅利及董監酬勞後之EPS": "股利政策表",
        "董事會備註": "股利政策表",
        "股東會備註": "股利政策表",
        "董事會決議通過股利分派日": "股利政策表",
        "股東會日期": "股利政策表",
        "公告日期": "股利政策表",
        "除權公告日期": "股利政策表",
        "除息公告日期": "股利政策表",
        "現增除權日": "股利政策表",
        "現增類別": "股利政策表",
        "現增認購價": "股利政策表",
        "現增配股(股)": "股利政策表",
        "現增總額(百萬)": "股利政策表",
        "董監改選年度": "股利政策表",
    }
    wb_path = get_workbook_path()
    logger.info(wb_path)

    with xw.App() as app:
        wb = xw.Book(wb_path)
        sh = wb.sheets("工作表1")

        logger.info("clear contents...")
        rng = sh.range("A3:CNZ10000")
        rng.delete()

        logger.info("update request items...")
        idx = 3
        for item, table in items.items():
            req_date = start_date
            while req_date and req_date <= end_date:
                sh.range(f"A{idx}").value = f"{table}.{item}"
                sh.range(f"B{idx}").value = req_date.strftime("%Y")
                req_date = req_date + pd.offsets.YearBegin()

                idx += 1

        logger.info("update data...")
        wb.macro("工作表1.CM_Renew")()

        logger.info("save and close workbook")
        wb.save()
        wb.close()


@task(name="task-dividend_policy-process_data")
def process_data() -> Dict[str, pd.DataFrame]:
    collection = {}
    wb_path = get_workbook_path()
    df = pd.read_excel(wb_path, 0, dtype=str)
    indexes = df.iloc[1:, 1].unique()
    indexes.sort()
    df.set_index("基準日:最近一日", inplace=True)

    col_map = {
        "年度": "year",
        "配發次數": "distribution_frequency",
        "除權日": "ex_rights_date",
        "除權最後回補日": "ex_rights_last_compensation_date",
        "除息日": "ex_dividend_date",
        "除息最後回補日": "ex_dividend_last_compensation_date",
        "除權分派基準日": "ex_rights_allotment_reference_date",
        "除息分派基準日": "ex_dividend_allotment_reference_date",
        "領股日期": "share_receipt_date",
        "領息日期": "dividend_receipt_date",
        "盈餘配股(元)": "earnings_stock_dividend",
        "公積配股(元)": "surplus_stock_dividend",
        "股票股利合計(元)": "total_stock_dividend",
        "盈餘配息(元)": "earnings_cash_dividend",
        "公積配息(元)": "surplus_cash_dividend",
        "現金股利合計(元)": "total_cash_dividend",
        "股利合計(元)": "total_dividend",
        "股票股利發放率(%)": "stock_dividend_payout_ratio",
        "現金股利發放率(%)": "cash_dividend_payout_ratio",
        "股利發放率(%)": "dividend_payout_ratio",
        "除權開盤競價基準": "ex_rights_opening_reference_price",
        "除息開盤競價基準": "ex_dividend_opening_reference_price",
        "除權參考價": "ex_rights_reference_price",
        "除息參考價": "ex_dividend_reference_price",
        "除權前股價": "pre_ex_rights_stock_price",
        "除息前股價": "pre_ex_dividend_stock_price",
        "除權前股本(百萬)": "pre_ex_rights_share_capital",
        "除權後股本(百萬)": "post_ex_rights_share_capital",
        "除權前市值比重(%)": "pre_ex_rights_market_value_ratio",
        "除息前市值比重(%)": "pre_ex_dividend_market_value_ratio",
        "現金股利殖利率(%)": "cash_dividend_yield",
        "股東股票股利總配股數(張)": "total_shareholders_stock_dividend_allotment_shares",
        "股東現金紅利總金額(千)": "total_shareholders_cash_dividend_amount",
        "員工酬勞配股(張)": "employee_compensation_stock_allotment_shares",
        "員工配股金額(千)": "employee_stock_allotment_amount",
        "員工紅利配股佔盈餘配股比例(%)": "employee_bonus_stock_allotment_ratio_to_earnings_stock_dividend",
        "員工酬勞現金(千)": "employee_cash_compensation",
        "董監酬勞(千)": "directors_and_supervisors_compensation",
        "酬勞差異數(千)": "compensation_difference",
        "扣除紅利及董監酬勞後之EPS": "eps_after_deducting_dividends_and_directors_compensation",
        "董事會備註": "board_remarks",
        "股東會備註": "shareholders_meeting_remarks",
        "董事會決議通過股利分派日": "dividend_distribution_date_approved_by_the_board_of_directors",
        "股東會日期": "shareholders_meeting_date",
        "公告日期": "announcement_date",
        "除權公告日期": "ex_rights_announcement_date",
        "除息公告日期": "ex_dividend_announcement_date",
        "現增除權日": "rights_offering_date_for_capital_increase",
        "現增類別": "type_of_capital_increase",
        "現增認購價": "subscription_price_for_capital_increase",
        "現增配股(股)": "stock_allotment_for_capital_increase_shares",
        "現增總額(百萬)": "total_amount_for_capital_increase",
        "董監改選年度": "year_of_directors_and_supervisors_resignation_and_election",
    }
    item_start_idx = 4
    items = df.iloc[1:, 3].str[item_start_idx:].unique()
    tmp_rows = {}
    for item in items:
        tmp_rows[item] = df.loc[df.iloc[:, 3].str[item_start_idx:] == item]

    for code in df.columns[4:]:
        tmp = pd.DataFrame(index=indexes, columns=items)
        for item in items:
            tmp.loc[:, item] = tmp_rows[item][code]

        tmp.dropna(how="all", axis=0, inplace=True)
        tmp.rename(columns=col_map, inplace=True)
        for col in tmp.columns:
            if col in [
                "ex_rights_date",
                "ex_rights_last_compensation_date",
                "ex_dividend_date",
                "ex_dividend_last_compensation_date",
                "ex_rights_allotment_reference_date",
                "ex_dividend_allotment_reference_date",
                "share_receipt_date",
                "dividend_receipt_date",
                "dividend_distribution_date_approved_by_the_board_of_directors",
                "shareholders_meeting_date",
                "announcement_date",
                "ex_rights_announcement_date",
                "ex_dividend_announcement_date",
                "rights_offering_date_for_capital_increase",
            ]:
                tmp.loc[pd.isnull(tmp[col]), col] = None

        for col in [
            "distribution_frequency",
            "total_shareholders_stock_dividend_allotment_shares",
            "total_shareholders_cash_dividend_amount",
            "employee_compensation_stock_allotment_shares",
            "employee_stock_allotment_amount",
            "employee_bonus_stock_allotment_ratio_to_earnings_stock_dividend",
            "employee_cash_compensation",
            "directors_and_supervisors_compensation",
            "compensation_difference",
            "total_amount_for_capital_increase",
            "year_of_directors_and_supervisors_resignation_and_election",
        ]:
            tmp.loc[pd.isnull(tmp[col]), col] = None

        if tmp.empty:
            continue
        tmp["code"] = code

        collection[code] = tmp

    return collection


@task(name="task-dividend_policy-save2db", log_prints=True)
def save2db(collection: Dict[str, pd.DataFrame]):
    dm = DataManager(verbose=False)
    for code, df in collection.items():
        dm.save(
            "cmoney.dividend_policy",
            df,
            method="upsert",
            conflict_cols=["year", "code"],
        )


@task(name="task-dividend_policy-get_last_date", log_prints=True)
def get_last_date() -> pd.Timestamp:
    dm = DataManager(verbose=False)
    last_date = dm.get_max_datetime("cmoney.dividend_policy", {}, "announcement_date")
    if last_date is None:
        return pd.to_datetime("1990-01-01")
    else:
        return pd.to_datetime(last_date)


@flow(
    retries=2,
    retry_delay_seconds=30,
    task_runner=SequentialTaskRunner(),
    on_failure=flow_error_handle,
)
def flow_dividend_policy_history():
    logger = get_run_logger()
    today = pd.Timestamp.today()
    start_date = get_last_date()
    while start_date <= today:
        end_date = start_date + 5 * pd.offsets.YearEnd()
        if end_date >= today:
            end_date = today
        logger.info(f"{start_date} ~ {end_date}")
        update_workbook(start_date, end_date)
        collections = process_data()
        save2db(collections)
        start_date = end_date + pd.offsets.YearBegin()


@flow(
    retries=2,
    retry_delay_seconds=30,
    task_runner=SequentialTaskRunner(),
    on_failure=flow_error_handle,
)
def flow_dividend_policy():
    logger = get_run_logger()
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.offsets.YearEnd()
    logger.info(f"{start_date} ~ {end_date}")
    update_workbook(start_date, end_date)
    collections = process_data()
    save2db(collections)
