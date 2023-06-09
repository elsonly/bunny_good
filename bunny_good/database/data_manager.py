import datetime as dt
from typing import Dict, List
import pandas as pd
from loguru import logger
from enum import Enum

from bunny_good.database.tsdb_client import TSDBClient
from bunny_good.config import Config


class DataManagerType(Enum):
    QUOTE = "Quote"
    PREFECT = "Prefect"


class DataManager:
    def __init__(
        self, verbose: bool = True, dm_type: DataManagerType = DataManagerType.PREFECT
    ):
        if dm_type == DataManagerType.QUOTE:
            self.cli = TSDBClient(
                host=Config.DB_QUOTE_HOST,
                port=Config.DB_QUOTE_PORT,
                user=Config.DB_QUOTE_USER,
                password=Config.DB_QUOTE_PASSWORD,
                db=Config.DB_QUOTE_DATABASE,
            )
        elif dm_type == DataManagerType.PREFECT:
            self.cli = TSDBClient(
                host=Config.DB_PREFECT_HOST,
                port=Config.DB_PREFECT_PORT,
                user=Config.DB_PREFECT_USER,
                password=Config.DB_PREFECT_PASSWORD,
                db=Config.DB_PREFECT_DATABASE,
            )
        else:
            raise Exception(f"Invalid Data Manager Type {dm_type}")
        self.type = dm_type
        self.verbose = verbose

    def convert_condition_to_sql_string(self, conditions: dict) -> str:
        cond_list = []
        for key, val in conditions.items():
            sql = ""
            if isinstance(val, bool):
                if val:
                    sql = f"{key}=true"
                else:
                    sql = f"{key}=false"
            elif isinstance(val, str):
                sql = f"{key}='{val}'"
            elif isinstance(val, (int, float)):
                sql = f"{key}={val}"
            elif isinstance(val, (dt.date, dt.datetime, pd.Timestamp)):
                sql = f"{key}='{val.strftime('%Y-%m-%d')}'"
            elif isinstance(val, list):
                if val:
                    if isinstance(val[0], str):
                        sql = f"""{key} in ( {",".join([f"'{x}'" for x in val])} ) """
                    elif isinstance(val[0], (int, float)):
                        sql = f"""{key} in ( {",".join([f"{x}" for x in val])} ) """
                    elif isinstance(val[0], (dt.date, dt.datetime, pd.Timestamp)):
                        sql = f"""{key} in ( {",".join([f"'{x.strftime('%Y-%m-%d')}'" for x in val])} ) """
                    else:
                        raise Exception(f"not handle type in list: {type(val)}")
            else:
                raise Exception(f"not handle type: {type(val)}")

            if sql:
                cond_list.append(sql)

        if cond_list:
            return " and ".join(cond_list)
        else:
            return " true "

    def get_max_datetime(
        self, table: str, conditions: Dict[str, str], time_col: str
    ) -> str:
        if conditions:
            sql_cond = self.convert_condition_to_sql_string(conditions=conditions)
            max_time = self.cli.execute_query(
                f"select max({time_col}) from {table} where {sql_cond}",
            )[0][0]
        else:
            max_time = self.cli.execute_query(f"select max({time_col}) from {table}")[
                0
            ][0]

        if isinstance(max_time, (dt.datetime, dt.date)):
            if "dt" in time_col:
                time_format = "%FT%X"
            else:
                time_format = "%F"
            return max_time.strftime(time_format)
        else:
            return max_time

    def _check_exists(self, table: str, conditions: dict):
        cond_sql = self.convert_condition_to_sql_string(conditions)
        counts = self.cli.execute_query(
            f"select count(*) from {table} where {cond_sql}",
        )[0][0]
        if counts:
            return True
        else:
            return False

    def save(
        self,
        table: str,
        df: pd.DataFrame,
        method: str,
        time_col: str = None,
        conflict_cols: List[str] = None,
        conditions: Dict[str, str] = None,
    ):
        """
        method (str): {direct, upsert, timeseries, if_not_exists}
        """
        if df.empty:
            return
        if self.verbose:
            logger.info(f"save {table} | size: {len(df)}")

        result = 1
        if method == "direct":
            result = self.cli.execute_values_df(df, table)

        elif method == "if_not_exists":
            if not self._check_exists(table=table, conditions=conditions):
                result = self.cli.execute_values_df(df, table)
            else:
                result = 0
                logger.warning("data already exists | skip insert")

        elif method == "timeseries":
            max_dt = self.get_max_datetime(table, conditions, time_col)
            if max_dt:
                df_save = df.loc[df[time_col] > max_dt]
            else:
                df_save = df
            result = self.cli.execute_values_df(df_save, table)

        elif method == "upsert":
            if not conflict_cols:
                raise Exception("conflict_cols is required")
            result = self.cli.excute_batch_upsert_df(
                df, table, conflict_cols=conflict_cols
            )

        if result == 1:
            raise Exception(f"save {table} | failed")
        elif isinstance(result, str) and "Error" in result:
            raise Exception(f"save {table} | failed", result)
        else:
            if self.verbose:
                logger.info(f"save {table} | success")

    def get_twse_trading_dates(self) -> List[dt.date]:
        sql = "select * from (select distinct tdate from tsdb.cmoney.institute_invest) t0 order by tdate"
        df = self.cli.execute_query(sql, out_type="df")
        if df.empty:
            return []
        tdates = df["tdate"].tolist()
        return tdates

    def get_twse_stock_list(self) -> List[str]:
        sql = """
            select code
            from tsdb.sino.contracts
            where length(code) = 4
                and security_type = 'STK'
        """
        df = self.cli.execute_query(sql, out_type="df")
        return df["code"].tolist()
