#!/bin/bash

# MyKY Application Kill Script
# This script terminates all processes related to the MyKY application

echo "🔴 MyKY Kill Protocol Initiated..."

# Kill all dotnet processes (ASP.NET applications)
echo "Terminating .NET processes..."
pkill -9 dotnet

# Kill any MyKYWeb processes specifically
echo "Terminating MyKYWeb processes..."
pkill -9 -f MyKYWeb

# Kill any Python scraper processes
echo "Terminating Python scraper processes..."
pkill -9 -f "MainScraper.py"
pkill -9 -f "SeleniumAndWebDriverTest.py"

# Kill any Chrome/Chromium processes that might be running from scraping
echo "Terminating Chrome/Chromium processes..."
pkill -9 chrome
pkill -9 chromium-browser

# Kill any chromedriver processes
echo "Terminating ChromeDriver processes..."
pkill -9 chromedriver

# Optional: Kill any processes running on port 5000 (ASP.NET default)
echo "Terminating processes on port 5000..."
lsof -ti:5000 | xargs -r kill -9

echo "✅ MyKY Kill Protocol Complete"
echo "All related processes have been terminated."
