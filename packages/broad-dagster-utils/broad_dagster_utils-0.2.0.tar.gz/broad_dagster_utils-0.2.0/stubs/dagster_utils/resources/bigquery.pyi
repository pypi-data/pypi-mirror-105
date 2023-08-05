from dagster import InitResourceContext as InitResourceContext
from dagster_utils.contrib.google import get_credentials as get_credentials
from google.cloud.bigquery import Client, Dataset as Dataset

def bigquery_client(init_context: InitResourceContext) -> Client: ...

class NoopBigQueryClient:
    def create_dataset(self, dataset: Dataset) -> None: ...

def noop_bigquery_client(init_context: InitResourceContext) -> Client: ...
