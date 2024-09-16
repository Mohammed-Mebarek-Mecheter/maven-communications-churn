from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import maven_communications_dbt_assets
from .project import maven_communications_project
from .schedules import schedules

defs = Definitions(
    assets=[maven_communications_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=maven_communications_project),
    },
)