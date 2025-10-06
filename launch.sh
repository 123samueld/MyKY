#!/bin/bash

# Set the working directory to the script's location (app root)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || { echo "Error: Failed to change to $SCRIPT_DIR"; exit 1; }

# Read paths from the JSON file using jq
config_file="./Utilities/FilePathCompendium.json"
backend_dir=$(jq -r '.backendDirectory' "$config_file")
data_dir=$(jq -r '.utilities' "$config_file")

# Construct the .csproj path as absolute
csproj_path="$SCRIPT_DIR/$backend_dir/MyKYWeb.csproj"

# Debug: Print environment and paths
echo "DEBUG: Current directory: $(pwd)"
echo "DEBUG: SCRIPT_DIR=$SCRIPT_DIR"
echo "DEBUG: config_file=$config_file"
echo "DEBUG: backend_dir=$backend_dir"
echo "DEBUG: csproj_path=$csproj_path"
echo "DEBUG: dotnet version: $(dotnet --version)"
echo "DEBUG: Checking csproj existence: ls -l $csproj_path"

# Check if the .csproj file exists
if [ ! -f "$csproj_path" ]; then
    echo "Error: Project file $csproj_path does not exist."
    ls -l "$SCRIPT_DIR/$backend_dir"  # Show directory contents for debugging
    exit 1
fi

# Check for and kill any existing dotnet processes on port 5000
echo "DEBUG: Checking for existing dotnet processes"
if lsof -i :5000 > /dev/null; then
    echo "DEBUG: Killing existing process on port 5000"
    kill -9 $(lsof -t -i :5000) || { echo "Error: Failed to kill existing process"; }
fi

# Start backend (if it's not already running)
cd "$SCRIPT_DIR/$backend_dir" || { echo "Error: Failed to change to $SCRIPT_DIR/$backend_dir"; exit 1; }

# Clean and build to ensure latest code, comment this out for the production version.
echo "DEBUG: Cleaning project"
dotnet clean "$csproj_path" || { echo "Error: Clean failed"; exit 1; }
echo "DEBUG: Building project"
dotnet build "$csproj_path" || { echo "Error: Build failed"; exit 1; }

echo "DEBUG: Running command: dotnet run --project \"$csproj_path\""
dotnet run --project "$csproj_path" &

# Wait a few seconds for the server to start
sleep 3

# Open the dashboard in the browser
xdg-open http://localhost:5000/dashboard