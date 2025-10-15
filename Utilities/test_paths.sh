#!/bin/bash

# MyKY Path Configuration Test Script
# This script tests if the FilePathCompendium.json configuration is correct

echo "=== MyKY Path Configuration Test ==="
echo

# Get the current directory (should be Utilities directory)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Current script directory: $SCRIPT_DIR"

# Get the project root directory (one level up from Utilities)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
echo "Project root directory: $PROJECT_ROOT"

# Read the RootPath from JSON
config_file="$SCRIPT_DIR/FilePathCompendium.json"
if [ ! -f "$config_file" ]; then
    echo "❌ ERROR: FilePathCompendium.json not found at $config_file"
    exit 1
fi

root_path=$(jq -r '.RootPath' "$config_file")
echo "RootPath from config: $root_path"

# Test if the root path exists
if [ ! -d "$root_path" ]; then
    echo "❌ ERROR: RootPath '$root_path' does not exist on this system"
    echo "   Please update the RootPath in FilePathCompendium.json to match your system"
    exit 1
fi

echo "✅ RootPath exists"

# Test if the configured root path matches our actual project location
expected_project_path="$root_path/Desktop/MyKY"
if [ "$PROJECT_ROOT" != "$expected_project_path" ]; then
    echo "⚠️  WARNING: Project location mismatch"
    echo "   Actual project location: $PROJECT_ROOT"
    echo "   Expected location from config: $expected_project_path"
    echo "   This might be OK if you've moved the project or configured custom paths"
else
    echo "✅ Project location matches configuration: $PROJECT_ROOT"
fi

# Test key directories and files
echo
echo "Testing key files and directories:"

# Test Dashboard directory
dashboard_path="$PROJECT_ROOT/Dashboard"
if [ -d "$dashboard_path" ]; then
    echo "✅ Dashboard directory: $dashboard_path"
else
    echo "❌ Dashboard directory missing: $dashboard_path"
fi

# Test Resources directory
resources_path="$PROJECT_ROOT/Resources"
if [ -d "$resources_path" ]; then
    echo "✅ Resources directory: $resources_path"
else
    echo "❌ Resources directory missing: $resources_path"
fi

# Test kill_protocol.sh
kill_script="$PROJECT_ROOT/kill_protocol.sh"
if [ -f "$kill_script" ]; then
    echo "✅ Kill script: $kill_script"
    if [ -x "$kill_script" ]; then
        echo "✅ Kill script is executable"
    else
        echo "⚠️(Expected) Kill script exists but is not executable (run: chmod +x kill_protocol.sh)"
    fi
else
    echo "❌ Kill script missing: $kill_script"
fi

# Test launch.sh
launch_script="$PROJECT_ROOT/launch.sh"
if [ -f "$launch_script" ]; then
    echo "✅ Launch script: $launch_script"
    if [ -x "$launch_script" ]; then
        echo "✅ Launch script is executable"
    else
        echo "⚠️(Expected) Launch script exists but is not executable (run: chmod +x launch.sh)"
    fi
else
    echo "❌ Launch script missing: $launch_script"
fi

# Test ScrapeSystem configuration
echo
echo "Testing ScrapeSystem configuration:"
scraper_config_test="$PROJECT_ROOT/ScrapeSystem/test_config.py"
if [ -f "$scraper_config_test" ]; then
    echo "✅ ScrapeSystem config test script exists"
    echo "   Running ScrapeSystem configuration test..."
    cd "$PROJECT_ROOT/ScrapeSystem" && python3 test_config.py
    cd "$PROJECT_ROOT"
else
    echo "⚠️ ScrapeSystem config test script missing: $scraper_config_test"
fi

echo
echo "=== Test Complete ==="
echo "If all items show ✅, your path configuration is correct!"
echo "If any items show ❌, please report the issue."
echo "If any items show ⚠️ (Expected), this is expected and can be ignored."
echo "If any items show ⚠️ (but no \"Expected\"), please report the issue.."