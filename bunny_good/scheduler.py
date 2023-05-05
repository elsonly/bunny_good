from enum import Enum
import time
from typing import Dict, TypedDict
from datetime import datetime, timedelta
import pandas as pd

from bunny_good.quote.quote_manager import QuoteManager
from bunny_good.database.data_manager import DataManager
from bunny_good.config import Config


class ScheduleJobs(Enum):
    Snapshots = 1


class Schedule(TypedDict):
    job: ScheduleJobs
    active: bool
    prev_dt: datetime
    next_dt: datetime
    interval: timedelta


class Scheduler:
    def __init__(self):
        self.qm = QuoteManager()
        self.dm = DataManager()
        self.__active_schedule = False
        self.schedules: Dict[str, Schedule] = {}
        self.interval_snapshot = 5

    def _save2db(self, job: ScheduleJobs, df: pd.DataFrame):
        if job == ScheduleJobs.Snapshots:
            pass

    def register(self, schedule: Schedule):
        self.schedules[schedule["name"]] = schedule

    def _job_snapshots(self):
        codes = self.qm.get_market_codes()
        rng = 500
        for idx in range(0, len(codes), rng):
            df = self.qm.snapshots(codes[idx : idx + rng])
            time.sleep(0.25)
            if df.empty:
                continue
            self._save2db(ScheduleJobs.Snapshots, df)

    def run(self):
        self.__active_schedule = True
        while self.__active_schedule:
            cur_dt = datetime.now()
            for name, schedule in self.schedules.items():
                if schedule.get("prev_dt"):
                    if schedule["prev_dt"] + schedule["interval"] >= cur_dt:
                        if ScheduleJobs.Snapshots:
                            self._job_snapshots()

            time.sleep(0.1)

    def __del__(self):
        self.__active_schedule = False


if __name__ == "__main__":
    scheduler = Scheduler()
