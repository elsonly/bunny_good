from typing import List
import pandas as pd

from bunny_good.quote.shioaji_client import ShioajiClient
from bunny_good.config import Config


class QuoteManager:
    def __init__(self):
        self.cli = ShioajiClient(
            api_key=Config.SHIOAJI_API_KEY,
            api_secret=Config.SHIOAJI_SECRET,
            simulation=True,
        )
        self.cli.login()

    def get_market_codes(self) -> List[str]:
        return self.cli.get_market_codes()

    def snapshots(self, codes: List[str]) -> pd.DataFrame:
        return self.cli.snapshots(codes)
