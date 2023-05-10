from datetime import datetime, timedelta

from bunny_good.scheduler import Scheduler, Schedule, ScheduleJobs


if __name__ == "__main__":
    scheduler = Scheduler(verbose=False)
    schedule = Schedule(
        job=ScheduleJobs.Snapshots,
        active=True,
        prev_dt=None,
        next_dt=datetime.utcnow() + timedelta(seconds=5),
        interval=timedelta(seconds=5),
    )
    scheduler.register(schedule)
    scheduler.run()
