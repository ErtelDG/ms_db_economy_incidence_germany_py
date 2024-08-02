#!/bin/bash
# Script to update and start the Python service

LOGFILE="/var/www/ms_db_economy_incidence_germany_py/scripts/service.log"

# Function to log messages
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" >> $LOGFILE
}

# Change to the working directory
cd /var/www/ms_db_economy_incidence_germany_py || { log "Error: Working directory not found."; exit 1; }
log "Changed working directory."

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    log "Error: Virtual environment '.venv' not found."
    exit 1
fi

# Activate the virtual environment
source .venv/bin/activate || { log "Error: Could not activate .venv."; exit 1; }
log "Virtual environment activated."

# Check if Python and pip are available in the virtual environment
if ! command -v python > /dev/null; then
    log "Error: Python not found in the virtual environment."
    exit 1
fi

if ! command -v pip > /dev/null; then
    log "Error: pip not found in the virtual environment."
    exit 1
fi

# Update the code from the repository
git pull origin main || { log "Error: Git pull failed."; exit 1; }
log "Code updated."

# Install requirements from the requirements.txt file
pip install -r /var/www/ms_db_economy_incidence_germany_py/requirements.txt || { log "Error: pip install failed."; exit 1; }
log "Requirements installed."

# Start the Python script
exec .venv/bin/python /var/www/ms_db_economy_incidence_germany_py/src/main.py || { log "Error: Failed to start Python script."; exit 1; }
