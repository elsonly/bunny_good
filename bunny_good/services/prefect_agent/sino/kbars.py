from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
import pandas as pd
import shioaji as sj
from shioaji.contracts import BaseContract
from shioaji.constant import SecurityType, Exchange
import time
from typing import List, Tuple

from bunny_good.database.data_manager import DataManager
from bunny_good.services.prefect_agent.utils import flow_error_handle, get_tpe_datetime
from bunny_good.config import Config


def create_api() -> sj.Shioaji:
    api = sj.Shioaji(simulation=True)
    api.login(Config.SHIOAJI_API_KEY, Config.SHIOAJI_SECRET, fetch_contract=False)
    return api


@task(name="task-kbars-get_kbars", retries=3, retry_delay_seconds=30)
def get_kbars(
    dm: DataManager,
    api: sj.Shioaji,
    table: str,
    contract: BaseContract,
    max_retries: int = 3,
    rate_limit: int = 5,
) -> Tuple[pd.DataFrame, List[dict]]:
    logger = get_run_logger()
    col_mapping = {
        "ts": "dt",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "vol",
        "Amount": "amt",
    }
    max_time = dm.get_max_datetime(table, {"code": contract.code}, "dt")
    if max_time is None:
        start_dt = pd.to_datetime("2020-03-22")
    else:
        start_dt = pd.to_datetime(max_time) + pd.offsets.BDay()
    end_dt = start_dt + pd.offsets.MonthEnd()
    cur_dt = pd.Timestamp.now().date() - pd.offsets.BDay()

    df_list = []
    errors = []
    logger.info(f"get kbars: {contract.code}: {start_dt} ~ {cur_dt}")
    while start_dt < cur_dt:
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")
        kbars = None
        logger.info(f"{contract.code}: {start_date} ~ {end_date}")
        for _ in range(max_retries):
            try:
                time.sleep(rate_limit)
                kbars = api.kbars(contract, start_date, end_date)
                break
            except:
                pass
        if kbars is not None:
            df = pd.DataFrame(kbars.__dict__)
            df["code"] = contract.code
            df.loc[:, "ts"] = pd.to_datetime(df.loc[:, "ts"])
            df.rename(col_mapping, inplace=True, axis=1)

            if not df.empty:
                df_list.append(df)
        else:
            errors.append(
                {"code": contract.code, "start_date": start_date, "end_date": end_date}
            )
        start_dt = end_dt + pd.offsets.BDay()
        end_dt = end_dt + pd.offsets.MonthEnd()

    if df_list:
        df = pd.concat(df_list, axis=0)
        return df, errors
    else:
        return pd.DataFrame(), errors


@task(name="task-kbars-save2db")
def save2db(dm: DataManager, table: str, code: str, df: pd.DataFrame):
    dm.save(
        table,
        df,
        method="timeseries",
        conditions={"code": code},
        time_col="dt",
    )


@flow(
    retries=2,
    retry_delay_seconds=30,
    task_runner=SequentialTaskRunner(),
    on_failure=[flow_error_handle],
    on_crashed=[flow_error_handle],
)
def flow_kbars():
    dm = DataManager()
    api = create_api()
    table = "sino.kbars"
    all_errors = []
    stock_list = dm.get_twse_stock_list()
    for code in stock_list:
        contract = BaseContract(
            security_type=SecurityType.Stock, exchange=Exchange.TSE, code=code
        )
        df, errors = get_kbars(dm=dm, table=table, api=api, contract=contract)
        if not df.empty:
            save2db(dm=dm, table=table, code=code, df=df)
        all_errors.extend(errors)

    if all_errors:
        raise Exception(f"errors: {all_errors}")
