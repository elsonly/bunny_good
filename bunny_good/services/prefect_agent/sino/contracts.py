from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
import pandas as pd
import shioaji as sj
import time

from bunny_good.database.data_manager import DataManager
from bunny_good.services.prefect_agent.utils import flow_error_handle
from bunny_good.config import Config


@task(name="task-contracts-fetch_contracts", retries=3, retry_delay_seconds=30)
def fetch_contracts() -> pd.DataFrame:
    logger = get_run_logger()
    api = sj.Shioaji(simulation=True)
    api.login(Config.SHIOAJI_API_KEY, Config.SHIOAJI_SECRET, fetch_contract=False)
    api.fetch_contracts(contract_download=True)
    time.sleep(10)
    contracts = [
        contract
        for name, iter_contract in api.Contracts
        for code, contract in iter_contract._code2contract.items()
    ]
    df = pd.DataFrame([x.__dict__ for x in contracts])
    df["update_date"] = df["update_date"].str.replace("/", "-")
    df.loc[df["update_date"] == "", "update_date"] = None

    df["delivery_date"] = df["delivery_date"].str.replace("/", "-")
    df.loc[df["delivery_date"] == "", "delivery_date"] = None

    update_date = df.loc[~pd.isnull(df["update_date"]), "update_date"].max()

    logger.info(f"Contract Date: {update_date}")
    if (
        pd.Timestamp.now().date() != pd.to_datetime(update_date).date()
        and pd.Timestamp.now().weekday() < 5
    ):
        raise Exception(f"Invalid Contract Date: {update_date}")

    return df


@task(name="task-contracts-save2db")
def save2db(df: pd.DataFrame):
    dm = DataManager(verbose=False)
    dm.save(
        "tsdb.sino.contracts",
        df,
        method="upsert",
        time_col="update_date",
        conflict_cols=["code"],
    )


@flow(
    retries=2,
    retry_delay_seconds=30,
    task_runner=SequentialTaskRunner(),
    on_failure=flow_error_handle,
)
def flow_contracts():
    df = fetch_contracts()
    save2db(df)
