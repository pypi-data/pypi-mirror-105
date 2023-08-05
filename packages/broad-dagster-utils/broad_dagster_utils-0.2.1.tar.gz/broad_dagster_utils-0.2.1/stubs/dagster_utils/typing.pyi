from dagster import HookContext, InputDefinition as InputDefinition
from dagster.config import ConfigType as DagsterConfigType
from typing import Any, Callable, TypedDict

DagsterConfigDict: Any
DagsterObjectConfigSchema = dict[str, DagsterConfigType]
DagsterHookFunction = Callable[[HookContext], None]

class DagsterSolidConfig(TypedDict):
    required_resource_keys: set[str]
    input_defs: list[InputDefinition]
    config_schema: DagsterObjectConfigSchema

class LocatablePackage:
    @property
    def __file__(self) -> str: ...
