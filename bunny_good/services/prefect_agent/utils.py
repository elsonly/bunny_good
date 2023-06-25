from prefect.states import get_state_exception
from prefect.flows import FlowRun
from prefect import Flow, State
from datetime import timedelta, datetime

from bunny_good.alert_manager import AlertManager


def flow_error_handle(flow: Flow, flow_run: FlowRun, state: State):
    am = AlertManager()
    title = f"{flow.name} failed"
    msg = (
        f"flow: {flow.name}\n"
        f"module: {flow.__module__}\n"
        f"start time: {(flow_run.start_time + timedelta(hours=8)).isoformat()}\n"
        f"message: {state.message}\n"
    )
    print(msg)
    am.send_alert(title, msg)


def get_tpe_datetime() -> datetime:
    return datetime.utcnow() + timedelta(hours=8)