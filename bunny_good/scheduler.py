from enum import Enum
import time
from typing import Dict, TypedDict
from datetime import datetime, timedelta
import pandas as pd
from loguru import logger

from bunny_good.quote.quote_manager import QuoteManager
from bunny_good.database.data_manager import DataManager, DataManagerType
from bunny_good.alert_manager import AlertManager
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
    def __init__(self, verbose: bool = True):
        self.qm = QuoteManager()
        self.dm = DataManager(verbose, dm_type=DataManagerType.QUOTE)
        self.alert_manager = AlertManager()
        self.__active_schedule = False
        self.schedules: Dict[ScheduleJobs, Schedule] = {}

    def _save2db(self, job: ScheduleJobs, df: pd.DataFrame):
        if job == ScheduleJobs.Snapshots:
            self.dm.save("public.quote_snapshots", df, "upsert", conflict_cols=["code"])

    def register(self, schedule: Schedule):
        logger.info(f"register job: {schedule}")
        self.schedules[schedule["job"]] = schedule

    def _job_snapshots(self):
        if datetime.utcnow().weekday() >= 5:
            return
        if datetime.utcnow().hour >= 7:
            return
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
            cur_dt = datetime.utcnow()
            for job, schedule in self.schedules.items():
                try:
                    if cur_dt >= schedule["next_dt"]:
                        if job == ScheduleJobs.Snapshots:
                            self._job_snapshots()

                except Exception as e:
                    logger.exception(e)
                    self.alert_manager.send_alert(
                        title=f"{job} failed", content=f"{schedule} | failed"
                    )

                schedule["prev_dt"] = cur_dt
                schedule["next_dt"] = cur_dt + schedule["interval"]

            time.sleep(0.1)

    def __del__(self):
        self.__active_schedule = False
