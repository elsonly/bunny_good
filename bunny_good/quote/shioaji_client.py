from shioaji.contracts import Contract
import shioaji as sj
import pandas as pd
import time
from typing import List
from threading import Lock
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
        # self.__lock = Lock()
        self.contracts: Dict[str, Contract] = {}
        self.snapshot_collection = {}

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

    def logout(self):
        self.api.logout()

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
        df.ts = pd.to_datetime(df.ts)
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
