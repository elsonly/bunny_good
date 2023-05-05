import datetime as dt
from typing import Dict, List
import pandas as pd
from loguru import logger

from .tsdb_client import TSDBClient
from bunny_good.config import Config


class DataManager:
    def __init__(self, verbose: bool = True):
        self.cli = TSDBClient(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            db=Config.DB_DATABASE
        )
        self.verbose = verbose

    # def convert_condition_to_sql_string(self, conditions: dict) -> str:
    #     cond_list = []
    #     for key, val in conditions.items():
    #         sql = ""
    #         if isinstance(val, bool):
    #             if val:
    #                 sql = f"{key}=true"
    #             else:
    #                 sql = f"{key}=false"
    #         elif isinstance(val, str):
    #             sql = f"{key}='{val}'"
    #         elif isinstance(val, (int, float)):
    #             sql = f"{key}={val}"
    #         elif isinstance(val, (dt.date, dt.datetime, pd.Timestamp)):
    #             sql = f"{key}='{val.strftime('%Y-%m-%d')}'"
    #         elif isinstance(val, list):
    #             if val:
    #                 if isinstance(val[0], str):
    #                     sql = f"""{key} in ( {",".join([f"'{x}'" for x in val])} ) """
    #                 elif isinstance(val[0], (int, float)):
    #                     sql = f"""{key} in ( {",".join([f"{x}" for x in val])} ) """
    #                 elif isinstance(val[0], (dt.date, dt.datetime, pd.Timestamp)):
    #                     sql = f"""{key} in ( {",".join([f"'{x.strftime('%Y-%m-%d')}'" for x in val])} ) """
    #                 else:
    #                     raise Exception(f"not handle type in list: {type(val)}")
    #         else:
    #             raise Exception(f"not handle type: {type(val)}")

    #         if sql:
    #             cond_list.append(sql)

    #     if cond_list:
    #         return " and ".join(cond_list)
    #     else:
    #         return " true "

    # def get_max_time(
    #     self, table: str, conditions: Dict[str, str], time_col: str
    # ) -> str:
    #     if conditions:
    #         sql_cond = self.convert_condition_to_sql_string(conditions=conditions)
    #         max_time = self.cli.execute_query(
    #             f"select max({time_col}) from {table} where {sql_cond}",
    #         )[0][0]
    #     else:
    #         max_time = self.cli.execute_query(f"select max({time_col}) from {table}")[
    #             0
    #         ][0]

    #     if isinstance(max_time, (dt.datetime, dt.date)):
    #         if "dt" in time_col:
    #             time_format = "%FT%X"
    #         else:
    #             time_format = "%F"
    #         return max_time.strftime(time_format)
    #     else:
    #         return max_time

    # def check_exists(self, table: str, conditions: dict):
    #     cond_sql = self.convert_condition_to_sql_string(conditions)
    #     counts = self.cli.execute_query(
    #         f"select count(*) from {table} where {cond_sql}",
    #     )[0][0]
    #     if counts:
    #         return True
    #     else:
    #         return False

    # def save(
    #     self,
    #     schema: str,
    #     table: str,
    #     df: pd.DataFrame,
    #     method: str = "max_conds",
    #     time_col: str = None,
    #     conflict_cols: List[str] = None,
    #     max_conds: Dict[str, str] = None,
    # ):
        # """
        # method (str): {direct, upsert, max_conds}
        # """
        # if df.empty:
        #     return
        # _table = f"{schema}.{table}"
        # if self.verbose:
        #     logger.info(f"save {_table} | size: {len(df)}")

        # result = 1
        # if method == "direct":
        #     result = self.cli.execute_values_df(df, _table)
        # elif method == "insert_if_not_exists":
        #     if not self.check_exists(table=_table, conditions=max_conds):
        #         result = self.cli.execute_values_df(df, _table)
        #     else:
        #         result = 0
        #         logger.warning("data already exists | skip insert")
        # elif method == "max_conds":
        #     max_time = self.get_max_time(_table, max_conds, time_col)
        #     if max_time:
        #         df_save = df.loc[df[time_col] > max_time]
        #     else:
        #         df_save = df
        #     result = self.cli.execute_values_df(df_save, _table)

        # else:
        #     result = self.cli.excute_batch_upsert_df(
        #         df, _table, conflict_cols=conflict_cols
        #     )

        # if self.verbose:
        #     if result == 1:
        #         raise Exception(f"save {_table} | failed")
        #     elif isinstance(result, str) and "Error" in result:
        #         raise Exception(f"save {_table} | failed", result)
        #     else:
        #         logger.info(f"save {_table} | success")