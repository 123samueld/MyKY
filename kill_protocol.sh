#!/bin/bash

# MyKY Application Kill Script
# This script terminates all processes related to the MyKY application when no argument is provided,
# or specific ones if an argument is given.

# Function to kill everything (clients first, server last for reliability)
kill_all() {
    echo "Terminating Python scraper processes..."
    pkill -9 -f "MainScraper.py"
    pkill -9 -f "SeleniumAndWebDriverTest.py"

    echo "Terminating Chrome/Chromium processes..."
    pkill -9 chrome
    pkill -9 chromium-browser

    echo "Terminating ChromeDriver processes..."
    pkill -9 chromedriver

    echo "Terminating processes on port 5000..."
    fuser -k 5000/tcp  

    echo "Terminating processes on port 5001..."
    fuser -k 5001/tcp  
    
    echo "Terminating .NET processes (backup)..."
    pkill -9 dotnet
    pkill -9 -f MyKYWeb  

    echo "All done!"
}

# If no argument, kill all
if [ -z "$1" ]; then
    kill_all
    exit 0
fi

# Otherwise, handle individual cases
case "$1" in
  "dotnet")
    echo "Terminating .NET processes..."
    pkill -9 dotnet
    echo "Done"
    ;;
  "mykyweb")
    echo "Terminating MyKYWeb processes..."
    pkill -9 -f MyKYWeb
    echo "Done"
    ;;
  "python")
    echo "Terminating Python scraper processes..."
    pkill -9 -f "MainScraper.py"
    pkill -9 -f "SeleniumAndWebDriverTest.py"
    echo "Done"
    ;;
  "chrome")
    echo "Terminating Chrome/Chromium processes..."
    pkill -9 chrome
    pkill -9 chromium-browser
    echo "Done"
    ;;
  "chromedriver")
    echo "Terminating ChromeDriver processes..."
    pkill -9 chromedriver
    echo "Done"
    ;;
  "port5000")
    echo "Terminating processes on port 5000..."
    fuser -k 5000/tcp  
    echo "Done"
    ;;
  "port5001")
    echo "Terminating processes on port 5001..."
    fuser -k 5001/tcp  
    echo "Done"
    ;;
  *)
    echo "Error: Invalid task '$1'. Valid options: dotnet, mykyweb, python, chrome, chromedriver, port5000, port5001"
    exit 1
    ;;
esac

exit 0
