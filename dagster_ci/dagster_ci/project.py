from pathlib import Path

from dagster_dbt import DbtProject

maven_communications_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", "..", "..", "maven_communications").resolve(),
    packaged_project_dir=Path(__file__).joinpath("..", "..", "dbt-project").resolve(),
)
maven_communications_project.prepare_if_dev()