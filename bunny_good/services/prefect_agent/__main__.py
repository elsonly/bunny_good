from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from bunny_good.services.prefect_agent import cmoney

deployments = {}
deployments[0] = Deployment.build_from_flow(
    flow=cmoney.flow_daily_price,
    name="cmoney",
    version=1,
    schedule=(CronSchedule(cron="0 0 * * *", timezone="Asia/Taipei")),
    is_schedule_active=True,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)
deployments[1] = Deployment.build_from_flow(
    flow=cmoney.flow_daily_price_history,
    name="cmoney",
    version=1,
    is_schedule_active=False,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)
deployments[1] = Deployment.build_from_flow(
    flow=cmoney.flow_institute_invest,
    name="cmoney",
    version=1,
    schedule=(CronSchedule(cron="5 0 * * *", timezone="Asia/Taipei")),
    is_schedule_active=True,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)

if __name__ == "__main__":
    for deployment in deployments.values():
        deployment.apply()