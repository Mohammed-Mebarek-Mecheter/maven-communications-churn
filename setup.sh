#!/bin/bash
# setup.sh - Initialize environment

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo "Error: .env file not found."
    exit 1
fi

# Check for required environment variables
required_vars=("SUPABASE_URL" "SUPABASE_KEY" "DBT_HOST" "DBT_USER" "DBT_PASS" "DBT_PORT" "DBT_NAME")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not set. Please set it in your .env file."
        exit 1
    fi
done

# Install any additional Python dependencies
# pip install -r requirements.txt
echo "Workspace setup complete."