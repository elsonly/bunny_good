from shioaji.contracts import Contract
import shioaji as sj
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import List, Dict
from threading import Lock, Thread
from loguru import logger
from functools import wraps


def api_wrapper(retries: int = 1, retry_wait: int = 3):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for k in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    exc = e
                    logger.error(f"func: {func.__name__} | failed | retry: {k}")
                    logger.exception(e)
                    time.sleep(retry_wait)
            raise exc

        return inner

    return wrapper


class ShioajiClient:
    def __init__(self, api_key: str, api_secret: str, simulation: bool):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.simulation = simulation
        self.api = sj.Shioaji(simulation=simulation)
        self.contracts: Dict[str, Contract] = {}
        self.snapshot_collection = {}

        self.__thread = Thread(target=self._backgroud_tasks)
        self.__thread.setDaemon(True)
        self.__lock = Lock()
        self._active_backgroud_tasks = False
        self.connected = False

        self.__thread.start()

    def __del__(self):
        self._active_backgroud_tasks = False
        if self.__thread.is_alive():
            self.__thread.join(timeout=5)
        if self.connected:
            self.api.logout()

    def _backgroud_tasks(self):
        logger.info("start backgroud tasks")
        self._active_backgroud_tasks = True
        cur_dt = datetime.utcnow()
        # 8 am
        next_reconnect_dt = (cur_dt + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        while self._active_backgroud_tasks:
            cur_dt = datetime.now()
            if cur_dt > next_reconnect_dt:
                if self.connected:
                    self.logout()
                self.login()
                next_reconnect_dt += timedelta(days=1)

            time.sleep(15)

    def login(self):
        self.api.login(
            self.__api_key,
            self.__api_secret,
            fetch_contract=False,
            subscribe_trade=False,
        )
        self.api.fetch_contracts(contract_download=True)
        time.sleep(10)
        self.contracts = {
            code: contract
            for name, iter_contract in self.api.Contracts
            for code, contract in iter_contract._code2contract.items()
        }
        self.connected = True

    def logout(self):
        self.api.logout()
        self.connected = False

    def subscribe(self):
        pass

    def unsubscribe(self):
        pass

    @api_wrapper(retries=3, retry_wait=3)
    def snapshots(self, codes: List[str]) -> pd.DataFrame:
        contracts = [self.contracts[code] for code in codes if code in self.contracts]
        snapshots = self.api.snapshots(contracts)
        df = pd.DataFrame([x.__dict__ for x in snapshots])
        if df.empty:
            return pd.DataFrame()
        df["dt"] = pd.to_datetime(df.ts)
        df.drop(columns=["ts"], inplace=True)
        return df

    def get_market_codes(self) -> List[str]:
        return [
            code
            for code, contract in self.contracts.items()
            if len(code) == 4 and contract.security_type == "STK"
        ]


if __name__ == "__main__":
    from bunny_good.config import Config

    cli = ShioajiClient(
        api_key=Config.SHIOAJI_API_KEY,
        api_secret=Config.SHIOAJI_SECRET,
        simulation=False,
    )
    cli.login()

    cli.snapshots(["2330", "2317"])
    cli.contracts["2330"].security_type == "STK"
    [
        code
        for code, contract in cli.contracts.items()
        if len(code) == 4 and contract.security_type == "STK"
    ]
