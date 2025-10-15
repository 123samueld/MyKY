#!/bin/bash

# Set the working directory to the script's location (app root)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Read paths from JSON (use absolute paths)
config_file="$SCRIPT_DIR/Utilities/FilePathCompendium.json"
backend_dir=$(jq -r '.backendDirectory | rtrimstr("/")' "$config_file")
scraper_dir=$(jq -r '.scraperDirectory | rtrimstr("/")' "$config_file")
csproj_path="${backend_dir}/MyKYWeb.csproj"

# Check if the backend project file exists
if [ ! -f "$csproj_path" ]; then
    exit 1  # Exit if the CSProj is not found
fi

# Create/Setup venv if needed
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    python3 -m venv "$SCRIPT_DIR/venv"  # Create virtual environment
    source "$SCRIPT_DIR/venv/bin/activate"
    pip install flask  # Install flask into the virtual environment
    deactivate
fi

# Start Flask FIRST (in background, from correct dir)
cd "$scraper_dir"  # Change to the scraper directory
source "$SCRIPT_DIR/venv/bin/activate"  # Activate the virtual environment
python3 scraper_endpoint.py &  # Start Flask in background
FLASK_STARTED=$?
cd "$SCRIPT_DIR"  # Return to project root

# Check if Flask started successfully
if [ $FLASK_STARTED -ne 0 ]; then
    exit 1  # Exit if Flask fails to start
fi

# Start .NET backend from CORRECT directory
cd "$backend_dir" || exit 1  # Navigate to the backend directory, exit if failed
dotnet run --project MyKYWeb.csproj &  # Start .NET backend in background
DOTNET_STARTED=$?
cd "$SCRIPT_DIR"  # Return to project root

# Check if .NET backend started successfully
if [ $DOTNET_STARTED -ne 0 ]; then
    exit 1  # Exit if .NET backend fails to start
fi

# Wait a bit for services to start before opening dashboard
sleep 3
xdg-open http://localhost:5000/dashboard  # Open the dashboard in the browser
