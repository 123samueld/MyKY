#!/bin/bash

# MyKY Application Kill Script
# This script terminates specific processes related to the MyKY application based on input argument

# Check for argument
if [ -z "$1" ]; then
  echo "Error: No task specified. Usage: $0 [dotnet|mykyweb|python|chrome|chromedriver|port5000]"
  exit 1
fi

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
    lsof -ti:5000 | xargs -r kill -9
    echo "Done"
    ;;
  *)
    echo "Error: Invalid task '$1'. Valid options: dotnet, mykyweb, python, chrome, chromedriver, port5000"
    exit 1
    ;;
esac

exit 0