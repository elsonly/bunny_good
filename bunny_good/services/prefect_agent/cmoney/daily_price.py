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
            .joinpath("bunny_good/services/prefect_agent/cmoney/docs/daily_price.xlsm")
        )
    return wb_path


@task(retries=3, retry_delay_seconds=3)
def update_workbook(
    start_date: pd.Timestamp = None,
    end_date: pd.Timestamp = None,
    periods: List[pd.Timestamp] = [],
    validate_date: bool = False,
):
    def get_validate_date(tdate: pd.Timestamp) -> pd.Timestamp:
        if not validate_date or not periods:
            return tdate
        if tdate < pd.to_datetime("1997-02-01"):
            return tdate
        while tdate <= periods[-1]:
            if tdate in periods:
                return tdate
            tdate += pd.offsets.Day()
        return None

    logger = get_run_logger()
    items = {
        "開盤價": "日收盤表排行",
        "最高價": "日收盤表排行",
        "最低價": "日收盤表排行",
        "收盤價": "日收盤表排行",
        "成交量": "日收盤表排行",
        "成交筆數": "日收盤表排行",
        "成交金額(千)": "日收盤表排行",
        "成交值比重(%)": "日收盤表排行",
        "股本(百萬)": "日收盤表排行",
        "總市值(億)": "日收盤表排行",
        "本益比": "日收盤表排行",
        "股價淨值比": "日收盤表排行",
        "本益比(近四季)": "日收盤表排行",
        "週轉率(%)": "日收盤表排行",
        "漲跌停": "日收盤表排行",
    }
    wb_path = get_workbook_path()
    logger.info(wb_path)

    with xw.App() as app:
        wb = xw.Book(wb_path)
        sh = wb.sheets("工作表1")

        logger.info("clear contents...")
        rng = sh.range("A3:DIZ10000")
        rng.delete()

        logger.info("update request items...")
        idx = 3
        for item, table in items.items():
            req_date = get_validate_date(start_date)
            while req_date and req_date <= end_date:
                sh.range(f"A{idx}").value = f"{table}.{item}"
                sh.range(f"B{idx}").value = req_date.strftime("%Y%m%d")
                req_date = get_validate_date(req_date + pd.offsets.Day())

                idx += 1

        logger.info("update data...")
        wb.macro("工作表1.CM_Renew")()

        logger.info("save and close workbook")
        wb.save()
        wb.close()


@task
def process_data() -> Dict[str, pd.DataFrame]:
    collection = {}
    wb_path = get_workbook_path()
    df = pd.read_excel(wb_path, 0, dtype=str)
    indexes = df.iloc[1:, 1].unique()
    indexes.sort()
    df.set_index("基準日:最近一日", inplace=True)

    col_map = {
        "開盤價": "open",
        "最高價": "high",
        "最低價": "low",
        "收盤價": "close",
        "成交量": "volume",
        "成交筆數": "cnt",
        "成交金額(千)": "amt",
        "成交值比重(%)": "amt_ratio",
        "股本(百萬)": "shares",
        "總市值(億)": "market_value",
        "本益比": "pe",
        "股價淨值比": "pb",
        "本益比(近四季)": "pe_4q",
        "週轉率(%)": "turnover",
        "漲跌停": "up_down_limit",
    }
    item_start_idx = 8
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
        if tmp.empty:
            continue
        tmp["tdate"] = pd.to_datetime(tmp.index)
        tmp["code"] = code

        for col in ["volume", "cnt", "shares", "amt", "up_down_limit"]:
            tmp.loc[pd.isnull(tmp[col]), col] = None

        for col in [
            "open",
            "high",
            "low",
            "close",
            "pe",
            "pb",
            "pe_4q",
            "turnover",
            "amt_ratio",
            "market_value",
        ]:
            tmp.loc[:, col] = tmp.loc[:, col].astype(float)

        collection[code] = tmp

    return collection


@task(log_prints=True)
def save2db(collection: Dict[str, pd.DataFrame]):
    dm = DataManager(verbose=False)
    for code, df in collection.items():
        dm.save(
            "cmoney.daily_price",
            df,
            method="timeseries",
            time_col="tdate",
            conditions={"code": code},
        )


@task(log_prints=True)
def get_last_date() -> pd.Timestamp:
    dm = DataManager(verbose=False)
    last_date = dm.get_max_datetime("cmoney.daily_price", {}, "tdate")
    if last_date is None:
        return pd.to_datetime("1990-01-01")
    else:
        return pd.to_datetime(last_date)


@task(log_prints=True)
def get_trading_dates() -> List[pd.Timestamp]:
    dm = DataManager(verbose=False)
    tdates = [pd.to_datetime(x) for x in dm.get_twse_trading_dates()]
    return tdates


@flow(
    retries=2,
    retry_delay_seconds=30,
    task_runner=SequentialTaskRunner(),
    on_failure=[flow_error_handle],
    on_crashed=[flow_error_handle],
)
def flow_daily_price_history():
    logger = get_run_logger()
    today = pd.Timestamp.today()
    start_date = get_last_date() + pd.offsets.Day()
    trading_dates = get_trading_dates()
    while start_date <= today:
        end_date = start_date + pd.offsets.MonthEnd()
        if end_date >= today:
            end_date = today
        logger.info(f"{start_date} ~ {end_date}")
        update_workbook(start_date, end_date, periods=trading_dates, validate_date=True)
        collections = process_data()
        save2db(collections)
        start_date += pd.offsets.MonthBegin()


@flow(
    retries=2,
    retry_delay_seconds=30,
    timeout_seconds=1200,
    task_runner=SequentialTaskRunner(),
    on_failure=[flow_error_handle],
    on_crashed=[flow_error_handle],
)
def flow_daily_price():
    logger = get_run_logger()
    end_date = pd.Timestamp.today()
    start_date = end_date - 5 * pd.offsets.BDay()
    logger.info(f"{start_date} ~ {end_date}")
    update_workbook(start_date, end_date)
    collections = process_data()
    save2db(collections)
