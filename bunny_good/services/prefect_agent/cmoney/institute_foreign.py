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
                "bunny_good/services/prefect_agent/cmoney/docs/institute_foreign.xlsm"
            )
        )
    return wb_path


@task(name="task-institute_foreign-update_workbook", retries=3, retry_delay_seconds=3)
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
        "外資買張": "日外資持股與排行",
        "外資賣張": "日外資持股與排行",
        "外資買賣超": "日外資持股與排行",
        "外資持股異動": "日外資持股與排行",
        "外資持股張數": "日外資持股與排行",
        "外資及陸資(不含外資自營商)買張": "日外資持股與排行",
        "外資及陸資(不含外資自營商)賣張": "日外資持股與排行",
        "外資及陸資(不含外資自營商)買賣超": "日外資持股與排行",
        "外資自營商買張": "日外資持股與排行",
        "外資自營商賣張": "日外資持股與排行",
        "外資自營商買賣超": "日外資持股與排行",
        "外資買金額(千)": "日外資持股與排行",
        "外資賣金額(千)": "日外資持股與排行",
        "外資買賣超金額(千)": "日外資持股與排行",
        "外資買均價": "日外資持股與排行",
        "外資賣均價": "日外資持股與排行",
        "外資持股比率(%)": "日外資持股與排行",
        "外資持股市值(百萬)": "日外資持股與排行",
        "外資持股成本": "日外資持股與排行",
        "外資尚可投資張數": "日外資持股與排行",
        "外資尚可投資比率(%)": "日外資持股與排行",
        "外資投資上限比率(%)": "日外資持股與排行",
        "陸資投資上限比率(%)": "日外資持股與排行",
        "與前日異動原因": "日外資持股與排行",
    }
    wb_path = get_workbook_path()
    logger.info(wb_path)

    with xw.App() as app:
        wb = xw.Book(wb_path)
        sh = wb.sheets("工作表1")

        logger.info("clear contents...")
        sh.range("A3:CNZ1000").clear_contents()

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


@task(name="task-institute_foreign-process_data")
def process_data() -> Dict[str, pd.DataFrame]:
    collection = {}
    wb_path = get_workbook_path()
    df = pd.read_excel(wb_path, 0, dtype=str)
    indexes = df.iloc[1:, 1].unique()
    indexes.sort()
    df.set_index("基準日:最近一日", inplace=True)

    columns = df.iloc[1:, 3].str[8:].unique()
    col_map = {
        "外資買張": "buy",
        "外資賣張": "sell",
        "外資買賣超": "net",
        "外資持股異動": "holding_chg",
        "外資持股張數": "holding_chg_shares",
        "外資及陸資(不含外資自營商)買張": "buy_ex_dealer",
        "外資及陸資(不含外資自營商)賣張": "sell_ex_dealer",
        "外資及陸資(不含外資自營商)買賣超": "net_ex_dealer",
        "外資自營商買張": "buy_dealer",
        "外資自營商賣張": "sell_dealer",
        "外資自營商買賣超": "net_dealer",
        "外資買金額(千)": "buy_amt",
        "外資賣金額(千)": "sell_amt",
        "外資買賣超金額(千)": "net_amt",
        "外資買均價": "buy_avg_prc",
        "外資賣均價": "sell_avg_prc",
        "外資持股比率(%)": "holding_ratio",
        "外資持股市值(百萬)": "holding_mkt_value",
        "外資持股成本": "holding_avg_prc",
        "外資尚可投資張數": "avalible_shares",
        "外資尚可投資比率(%)": "avalible_ratio",
        "外資投資上限比率(%)": "avalible_limit",
        "陸資投資上限比率(%)": "avalible_limit_cn",
        "與前日異動原因": "reason_for_chg",
    }

    for code in df.columns[4:]:
        tmp = pd.DataFrame(index=indexes)
        for col in columns:
            cond_row = df.iloc[:, 3].str.endswith(col)
            tmp[col] = df.loc[cond_row, code]

        tmp.dropna(how="all", axis=0, inplace=True)
        tmp.rename(columns=col_map, inplace=True)
        if tmp.empty:
            continue
        tmp["tdate"] = pd.to_datetime(tmp.index)
        tmp["code"] = code
        tmp["reason_for_chg"] = tmp["reason_for_chg"].astype(str)
        tmp.loc[tmp["reason_for_chg"] == "nan", "reason_for_chg"] = None

        collection[code] = tmp

    return collection


@task(name="task-institute_foreign-save2db")
def save2db(collection: Dict[str, pd.DataFrame]):
    dm = DataManager(verbose=False)
    for code, df in collection.items():
        dm.save(
            "cmoney.institute_foreign",
            df,
            method="timeseries",
            time_col="tdate",
            conditions={"code": code},
        )


@task(name="task-institute_foreign-get_last_date")
def get_last_date() -> pd.Timestamp:
    dm = DataManager(verbose=False)
    last_date = dm.get_max_datetime("cmoney.institute_foreign", {}, "tdate")
    if last_date is None:
        return pd.to_datetime("1994-01-06")
    else:
        return pd.to_datetime(last_date)


@task(name="task-institute_foreign-get_trading_dates")
def get_trading_dates() -> List[pd.Timestamp]:
    dm = DataManager(verbose=False)
    tdates = [pd.to_datetime(x) for x in dm.get_twse_trading_dates()]
    return tdates


@flow(
    retries=2,
    retry_delay_seconds=30,
    task_runner=SequentialTaskRunner(),
    on_failure=flow_error_handle,
)
def flow_institute_foreign_history():
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
    task_runner=SequentialTaskRunner(),
    on_failure=flow_error_handle,
)
def flow_institute_foreign():
    logger = get_run_logger()
    end_date = pd.Timestamp.today()
    start_date = end_date - 5 * pd.offsets.BDay()
    logger.info(f"{start_date} ~ {end_date}")
    update_workbook(start_date, end_date)
    collections = process_data()
    save2db(collections)
