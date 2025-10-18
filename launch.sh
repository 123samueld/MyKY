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
fi

# Start Flask FIRST (in background, from correct dir)
cd "$scraper_dir"  # Change to the scraper directory
source "$SCRIPT_DIR/venv/bin/activate"  # Activate the virtual environment

# Ensure Python dependencies are installed (Flask, Flask-CORS)
pip install -r "$SCRIPT_DIR/Utilities/requirements.txt" >/dev/null 2>&1

# Ensure Playwright browsers are installed (Chromium)
python3 -m playwright install chromium >/dev/null 2>&1

# Start Flask in background with logging
FLASK_LOG="$SCRIPT_DIR/flask_server.log"
python3 scraper_endpoint.py >"$FLASK_LOG" 2>&1 &
FLASK_PID=$!
FLASK_STARTED=$?
cd "$SCRIPT_DIR"  # Return to project root

# Check if Flask started successfully
if [ $FLASK_STARTED -ne 0 ]; then
    echo "[launch] Flask failed to start (exit code $FLASK_STARTED). See $FLASK_LOG" >&2
    exit 1
fi

echo "[launch] Flask started with PID $FLASK_PID, logging to $FLASK_LOG"

# Setup database before starting .NET backend
echo "[launch] Setting up database..."
cd "$backend_dir" || exit 1  # Navigate to the backend directory, exit if failed

# Check if migrations exist, if not create them
if [ ! -d "Migrations" ]; then
    echo "[launch] Creating initial database migration..."
    dotnet ef migrations add InitialCreate --no-build
    if [ $? -ne 0 ]; then
        echo "[launch] Failed to create migration" >&2
        exit 1
    fi
fi

# Update database (without starting the app)
echo "[launch] Updating database..."
dotnet ef database update --no-build --verbose
if [ $? -ne 0 ]; then
    echo "[launch] Failed to update database" >&2
    exit 1
fi

echo "[launch] Database setup complete"

# Check if .NET backend is already running
if pgrep -f "dotnet.*MyKYWeb" > /dev/null; then
    echo "[launch] .NET backend already running, skipping startup"
else
    # Start .NET backend
    echo "[launch] Starting .NET backend..."
    dotnet run --project MyKYWeb.csproj &  # Start .NET backend in background
    DOTNET_PID=$!
    cd "$SCRIPT_DIR"  # Return to project root
    echo "[launch] .NET backend started with PID $DOTNET_PID"
fi

# Wait for .NET backend to be ready
echo "[launch] Waiting for .NET backend to be ready..."
sleep 5

# Health check for .NET backend
echo "[launch] Checking .NET backend health..."
for i in {1..10}; do
    if curl -s http://localhost:5000/api/property >/dev/null 2>&1; then
        echo "[launch] .NET backend is responding"
        break
    else
        echo "[launch] Waiting for .NET backend... (attempt $i/10)"
        sleep 2
    fi
done

# Check if database has data, if not, try to load some
echo "[launch] Checking if database has data..."
cd "$scraper_dir"

# Ensure Python dependencies are installed
echo "[launch] Ensuring Python dependencies are installed..."
source "$SCRIPT_DIR/venv/bin/activate"
pip install -r "$SCRIPT_DIR/Utilities/requirements.txt" >/dev/null 2>&1

if [ -f "ScrapedDataCache/landsearch_scrape_cache.json" ]; then
    echo "[launch] Found cached scraped data, transferring to database..."
    python3 post_to_database.py 2>&1 | head -20  # Show first 20 lines of output for debugging
    TRANSFER_RESULT=${PIPESTATUS[0]}
    if [ $TRANSFER_RESULT -eq 0 ]; then
        echo "[launch] Data transfer successful"
    else
        echo "[launch] Data transfer failed (exit code: $TRANSFER_RESULT), but continuing..."
    fi
else
    echo "[launch] No cached data found, database may be empty"
fi

cd "$SCRIPT_DIR"  # Return to project root

# Wait a bit for services to start before opening dashboard
sleep 2
echo "[launch] Opening dashboard..."
xdg-open http://localhost:5000/dashboard  # Open the dashboard in the browser
