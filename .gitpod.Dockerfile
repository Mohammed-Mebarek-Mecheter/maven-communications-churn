FROM gitpod/workspace-full:latest

# Install Python, dbt, Dagster, and other dependencies
USER gitpod

# Install Python packages for data analysis
RUN pip3 install pandas numpy scikit-learn plotly streamlit supabase

# Install dbt (Data Build Tool)
RUN pip3 install dbt-postgres

# Install Dagster
RUN pip3 install dagster dagit dagster-postgres dagster-dbt

# Install additional packages
RUN sudo apt-get update && \
    sudo apt-get install -y postgresql-client
