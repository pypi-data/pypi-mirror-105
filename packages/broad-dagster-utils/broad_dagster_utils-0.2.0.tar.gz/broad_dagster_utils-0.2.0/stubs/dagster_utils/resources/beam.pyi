from dagster import DagsterLogManager as DagsterLogManager
from dagster.core.execution.context.init import InitResourceContext as InitResourceContext
from kubernetes.client.models.v1_job import V1Job as V1Job
from typing import Any, List

class DataflowCloudConfig:
    project: str
    service_account: str
    subnet_name: str
    region: str
    worker_machine_type: str
    starting_workers: int
    max_workers: int
    subnetwork: str = ...
    def __post_init__(self) -> None: ...
    def __init__(self, project: Any, service_account: Any, subnet_name: Any, region: Any, worker_machine_type: Any, starting_workers: Any, max_workers: Any) -> None: ...

class DataflowBeamRunner:
    cloud_config: DataflowCloudConfig
    kubernetes_service_account: str
    temp_bucket: str
    image_name: str
    image_version: str
    namespace: str
    logger: DagsterLogManager
    def run(self, job_name: str, input_prefix: str, output_prefix: str) -> None: ...
    def dispatch_k8s_job(self, image_name: str, job_name_prefix: str, args: List[str]) -> V1Job: ...
    def __init__(self, cloud_config: Any, kubernetes_service_account: Any, temp_bucket: Any, image_name: Any, image_version: Any, namespace: Any, logger: Any) -> None: ...

def dataflow_beam_runner(init_context: InitResourceContext) -> DataflowBeamRunner: ...

class LocalBeamRunner:
    working_dir: str
    logger: DagsterLogManager
    target_class: str
    def run(self, job_name: str, input_prefix: str, output_prefix: str) -> None: ...
    def __init__(self, working_dir: Any, logger: Any, target_class: Any) -> None: ...

def local_beam_runner(init_context: InitResourceContext) -> LocalBeamRunner: ...

class TestBeamRunner:
    def run(self, job_name: str, input_prefix: str, output_prefix: str) -> None: ...

def test_beam_runner(init_context: InitResourceContext) -> TestBeamRunner: ...
