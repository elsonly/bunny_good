from typing import Dict
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator

from dags import config


def get_dag_info(file_path: str) -> Dict[str, str]:
    info = {}
    path_split = file_path.split("/")
    info["dag_id"] = f"{path_split[-2]}_{path_split[-1].replace('.py', '')}"
    info["group"] = path_split[-2]
    return info


def create_docker_operator(
    project_id: str, task_id: str, command: str, environment: dict = {}
):
    return DockerOperator(
        task_id=task_id,
        image="bunny_good:latest",
        container_name=f"task_{project_id}_{task_id}",
        command=command,
        environment=environment,
        auto_remove=True,
        docker_url=f"tcp://{config.AIRFLOW_WORKER_URL}",
        api_version="auto",
        network_mode="bridge",
    )


def get_default_args(project_id: str):
    return {
        "depends_on_past": False,
        "email": [],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 5,
        "retry_delay": timedelta(seconds=10),
    }
