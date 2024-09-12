#!/bin/bash
# setup.sh - Initialize environment

# Check for required environment variables
required_vars=("SUPABASE_URL" "SUPABASE_KEY" "DBT_HOST" "DBT_USER" "DBT_PASS" "DBT_PORT" "DBT_NAME")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not set. Please set it in your Gitpod environment variables."
        exit 1
    fi
done

# Install any additional Python dependencies
pip install -r requirements.txt

# Set up dbt profile
mkdir -p ~/.dbt
cat << EOF > ~/.dbt/profiles.yml
default:
  target: dev
  outputs:
    dev:
      type: postgres
      host: ${DBT_HOST}
      user: ${DBT_USER}
      pass: ${DBT_PASS}
      port: ${DBT_PORT}
      dbname: ${DBT_NAME}
      schema: public
      threads: 1
      keepalives_idle: 0
      sslmode: require
EOF

echo "Workspace setup complete."
echo "dbt profile created at ~/.dbt/profiles.yml"

# Test dbt connection
dbt debug --profiles-dir ~/.dbt