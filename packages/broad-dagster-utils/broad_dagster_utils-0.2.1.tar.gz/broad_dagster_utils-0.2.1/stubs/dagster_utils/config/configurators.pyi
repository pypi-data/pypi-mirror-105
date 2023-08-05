from dagster.core.definitions.configurable import ConfigurableDefinition as ConfigurableDefinition
from dagster_utils.config.preconfiguration_loader import PreconfigurationLoader as PreconfigurationLoader
from dagster_utils.typing import DagsterConfigDict as DagsterConfigDict, DagsterObjectConfigSchema as DagsterObjectConfigSchema, LocatablePackage as LocatablePackage
from typing import Optional

class PreconfiguratorFunction:
    def __call__(self, dagster_object: ConfigurableDefinition, mode_name: str, additional_schema: DagsterObjectConfigSchema=..., subdirectory: Optional[str]=...) -> ConfigurableDefinition: ...

def configurator_aimed_at(base_config_package: LocatablePackage) -> PreconfiguratorFunction: ...
