#!/bin/bash
# setup.sh - Initialize environment

# Make sure SUPABASE_URL and SUPABASE_KEY are set
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ]; then
  echo "Error: SUPABASE_URL or SUPABASE_KEY not set. Please set them in your environment variables."
  exit 1
fi

# Install any additional Python dependencies
pip install -r requirements.txt

echo "Workspace setup complete."
