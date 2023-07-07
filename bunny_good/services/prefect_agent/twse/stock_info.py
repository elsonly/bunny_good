import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from prefect import flow, task, get_run_logger
from prefect.task_runners import SequentialTaskRunner
import pandas as pd

from bunny_good.database.data_manager import DataManager
from bunny_good.services.prefect_agent.utils import flow_error_handle


@task(name="task-stock_info-get_stock_info", retries=3, retry_delay_seconds=3)
def get_stock_info(strMode: int) -> pd.DataFrame:
    """
    strMode:
        2:'上市'
        4:'上櫃'
        5:'興櫃'
        #6:'期貨選擇權'

    return (pd.DataFrame):
            code	name    isin	        ipo_date	listed_type	   ind	     cfic	 memo	 upd_date
        0	1101	台泥	TW0001101004	1962/02/09	上市	        水泥工業	ESVUFR		    2021/08/24
        1	1102	亞泥	TW0001102002	1962/06/08	上市	        水泥工業	ESVUFR		    2021/08/24
    """
    url = f"https://isin.twse.com.tw/isin/C_public.jsp?strMode={strMode}"
    res = requests.get(url)

    # parse
    soup = BeautifulSoup(res.text, features="lxml")

    # upd_date
    upd_date_raw = soup(text=re.compile("最近更新日期"))[0]
    upd_date = upd_date_raw.strip().split(":")[-1]

    if strMode in [2, 4, 5]:
        table: pd.DataFrame = pd.read_html(res.text)[0]
        table = table.iloc[1:]
        # columns name
        table.columns = [
            "code_name",
            "isin",
            "ipo_date",
            "listed_type",
            "ind",
            "cfic",
            "memo",
        ]

        # sec_type
        table["sec_type"] = None
        cond = table.iloc[:, 0] == table.iloc[:, 1]
        table.loc[cond, "sec_type"] = table.iloc[:, 0].loc[cond]
        table["sec_type"].fillna(method="ffill", inplace=True)
        table = table.loc[~cond]

        # split code, name
        table["code"] = [x.split("\u3000")[0] for x in table.iloc[:, 0].to_list()]
        table["name"] = [
            " ".join(x.split("\u3000")[1:]) for x in table.iloc[:, 0].to_list()
        ]

        # fillna
        for col in ["ind", "memo"]:
            table.loc[:, col].fillna("", inplace=True)

        # drop columns
        table.drop("code_name", axis=1, inplace=True)

        # reset_index
        table.reset_index(drop=True, inplace=True)

        # upd_date
        table["upd_date"] = upd_date

        return table

    else:
        raise Exception(f"Invalid strMode:{strMode}")


@task(name="task-stock_info-save2db", log_prints=True)
def save2db(df: pd.DataFrame):
    dm = DataManager(verbose=False)
    dm.save(
        "twse.stock_info",
        df,
        method="upsert",
        conflict_cols=["code"],
    )


@flow(
    retries=2,
    retry_delay_seconds=30,
    timeout_seconds=1200,
    task_runner=SequentialTaskRunner(),
    on_failure=[flow_error_handle],
    on_crashed=[flow_error_handle],
)
def flow_stock_info():
    logger = get_run_logger()
    for strMode in [2, 4, 5]:
        logger.info(f"get stock_info: {strMode}")
        df = get_stock_info(strMode)
        save2db(df)
