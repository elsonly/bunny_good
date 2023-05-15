from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from bunny_good.services.prefect_agent import cmoney, sino

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
deployments[2] = Deployment.build_from_flow(
    flow=cmoney.flow_institute_invest,
    name="cmoney",
    version=1,
    schedule=(CronSchedule(cron="5 0 * * *", timezone="Asia/Taipei")),
    is_schedule_active=True,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)
deployments[3] = Deployment.build_from_flow(
    flow=cmoney.flow_institute_foreign,
    name="cmoney",
    version=1,
    schedule=(CronSchedule(cron="10 0 * * *", timezone="Asia/Taipei")),
    is_schedule_active=True,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)
deployments[4] = Deployment.build_from_flow(
    flow=cmoney.flow_institute_foreign_history,
    name="cmoney",
    version=1,
    is_schedule_active=False,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)
deployments[5] = Deployment.build_from_flow(
    flow=cmoney.flow_institute_dealer,
    name="cmoney",
    version=1,
    schedule=(CronSchedule(cron="15 0 * * *", timezone="Asia/Taipei")),
    is_schedule_active=True,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)
deployments[6] = Deployment.build_from_flow(
    flow=cmoney.flow_institute_dealer_history,
    name="cmoney",
    version=1,
    is_schedule_active=False,
    tags=["twse", "cmoney"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)
# sino
deployments[100] = Deployment.build_from_flow(
    flow=sino.flow_contracts,
    name="sino",
    version=1,
    schedule=(CronSchedule(cron="5 8 * * *", timezone="Asia/Taipei")),
    is_schedule_active=True,
    tags=["twse", "sino"],
    infra_overrides={"env": {}},
    work_pool_name="local-work",
)

if __name__ == "__main__":
    for deployment in deployments.values():
        deployment.apply()
