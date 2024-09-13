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

echo "Workspace setup complete."
