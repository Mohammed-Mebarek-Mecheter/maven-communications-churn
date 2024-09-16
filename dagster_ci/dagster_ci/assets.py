from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from .project import maven_communications_project


@dbt_assets(manifest=maven_communications_project.manifest_path)
def maven_communications_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
    