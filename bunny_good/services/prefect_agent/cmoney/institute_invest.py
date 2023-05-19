from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
import xlwings as xw
import pandas as pd
from typing import Dict
from pathlib import Path

from bunny_good.database.data_manager import DataManager
from bunny_good.services.prefect_agent.utils import flow_error_handle


def inject_history_data():
    dm = DataManager()
    df = pd.read_excel(
        "./bunny_good/services/prefect_agent/cmoney/docs/institute_invest_hist.xlsx",
        0,
        dtype=str,
    )
    col_mapping = {
        "日期": "tdate",
        "代號": "inst_id",
        "上市買進金額(百萬)": "tse_buy",
        "上市賣出金額(百萬)": "tse_sell",
        "上市買賣超金額(百萬)": "tse_net",
        "上櫃買進金額(百萬)": "otc_buy",
        "上櫃賣出金額(百萬)": "otc_sell",
        "上櫃買賣超金額(百萬)": "otc_net",
        "合計買進金額(百萬)": "total_buy",
        "合計賣出金額(百萬)": "total_sell",
        "合計買賣超金額(百萬)": "total_net",
        "上櫃股票買進金額(百萬)": "otc_stock_buy",
        "上櫃股票賣出金額(百萬)": "otc_stock_sell",
        "上櫃股票買賣超金額(百萬)": "otc_stock_net",
        "興櫃買進金額(百萬)": "oes_buy",
        "興櫃賣出金額(百萬)": "oes_sell",
        "興櫃買賣超金額(百萬)": "oes_net",
    }
    df.drop([x for x in df.columns if x not in col_mapping], axis=1, inplace=True)
    df.rename(col_mapping, axis=1, inplace=True)
    df.replace("- -", "nan", inplace=True)
    df.loc[:, "inst_id"] = df.loc[:, "inst_id"].str[1:].astype(int)

    dm.save("cmoney.institute_invest", df, method="direct")


def get_workbook_path() -> Path:
    try:
        name = Path(__file__).absolute().name.replace(".py", "")
        wb_path = Path(__file__).parent.joinpath(f"docs/{name}.xlsm")
    except:
        wb_path = (
            Path()
            .absolute()
            .joinpath(
                "bunny_good/services/prefect_agent/cmoney/docs/institute_invest.xlsm"
            )
        )
    return wb_path


@task(name="task-institute_invest-update_workbook", retries=3, retry_delay_seconds=3)
def update_workbook(start_date: pd.Timestamp, end_date: pd.Timestamp):
    logger = get_run_logger()
    items = {
        "上市買進金額(百萬)": "三大法人買賣超",
        "上市賣出金額(百萬)": "三大法人買賣超",
        "上市買賣超金額(百萬)": "三大法人買賣超",
        "上櫃買進金額(百萬)": "三大法人買賣超",
        "上櫃賣出金額(百萬)": "三大法人買賣超",
        "上櫃買賣超金額(百萬)": "三大法人買賣超",
        "合計買進金額(百萬)": "三大法人買賣超",
        "合計賣出金額(百萬)": "三大法人買賣超",
        "合計買賣超金額(百萬)": "三大法人買賣超",
        "上櫃股票買進金額(百萬)": "三大法人買賣超",
        "上櫃股票賣出金額(百萬)": "三大法人買賣超",
        "上櫃股票買賣超金額(百萬)": "三大法人買賣超",
        "興櫃買進金額(百萬)": "三大法人買賣超",
        "興櫃賣出金額(百萬)": "三大法人買賣超",
        "興櫃買賣超金額(百萬)": "三大法人買賣超",
    }
    wb_path = get_workbook_path()
    logger.info(wb_path)

    with xw.App() as app:
        wb = xw.Book(wb_path)
        sh = wb.sheets("工作表1")

        logger.info("clear contents...")
        sh.range("A3:Y1000").clear_contents()

        logger.info("update request items...")
        idx = 3
        for item, table in items.items():
            req_date = start_date
            while req_date <= end_date:
                sh.range(f"A{idx}").value = f"{table}.{item}"
                sh.range(f"B{idx}").value = req_date.strftime(
                    "%Y%m%d"
                )
                req_date = pd.to_datetime(req_date) + pd.offsets.BDay()
                idx += 1

        logger.info("update data...")
        wb.macro("工作表1.CM_Renew")()

        logger.info("save and close workbook")
        wb.save()
        wb.close()


@task(name="task-institute_invest-process_data")
def process_data() -> Dict[str, pd.DataFrame]:
    collection = {}
    wb_path = get_workbook_path()
    df = pd.read_excel(wb_path, 0, dtype=str)
    indexes = df.iloc[1:, 1].unique()
    indexes.sort()
    df.set_index("基準日:最近一日", inplace=True)

    columns = df.iloc[1:, 3].str[8:].unique()
    df
    col_map = {
        "日期": "tdate",
        "代號": "inst_id",
        "上市買進金額(百萬)": "tse_buy",
        "上市賣出金額(百萬)": "tse_sell",
        "上市買賣超金額(百萬)": "tse_net",
        "上櫃買進金額(百萬)": "otc_buy",
        "上櫃賣出金額(百萬)": "otc_sell",
        "上櫃買賣超金額(百萬)": "otc_net",
        "合計買進金額(百萬)": "total_buy",
        "合計賣出金額(百萬)": "total_sell",
        "合計買賣超金額(百萬)": "total_net",
        "上櫃股票買進金額(百萬)": "otc_stock_buy",
        "上櫃股票賣出金額(百萬)": "otc_stock_sell",
        "上櫃股票買賣超金額(百萬)": "otc_stock_net",
        "興櫃買進金額(百萬)": "oes_buy",
        "興櫃賣出金額(百萬)": "oes_sell",
        "興櫃買賣超金額(百萬)": "oes_net",
    }

    for _id in df.columns[4:]:
        tmp = pd.DataFrame(index=indexes)
        for col in columns:
            cond_row = df.iloc[:, 3].str.endswith(col)
            tmp[col] = df.loc[cond_row, _id]

        tmp.dropna(how="all", axis=0, inplace=True)
        tmp.rename(columns=col_map, inplace=True)
        tmp["tdate"] = pd.to_datetime(tmp.index)
        inst_id = int(_id[1:])
        tmp["inst_id"] = inst_id

        collection[inst_id] = tmp

    return collection


@task(name="task-institute_invest-save2db")
def save2db(collection: Dict[str, pd.DataFrame]):
    dm = DataManager(verbose=False)
    for inst_id, df in collection.items():
        dm.save(
            "cmoney.institute_invest",
            df,
            method="timeseries",
            time_col="tdate",
            conditions={"inst_id": inst_id},
        )


@flow(
    retries=2,
    retry_delay_seconds=30,
    task_runner=SequentialTaskRunner(),
    on_failure=[flow_error_handle],
)
def flow_institute_invest():
    logger = get_run_logger()
    end_date = pd.Timestamp.today()
    start_date = end_date - 5 * pd.offsets.BDay()
    logger.info(f"{start_date} ~ {end_date}")
    update_workbook(start_date, end_date)
    collections = process_data()
    save2db(collections)
