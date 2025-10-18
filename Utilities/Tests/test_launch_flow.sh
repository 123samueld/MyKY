#!/bin/bash

echo "🧪 Testing Updated Launch Flow"
echo "============================="

# Change to the project directory
cd /home/samuel/Desktop/MyKY

echo "1️⃣ Testing launch.sh script..."
echo "This will:"
echo "  - Start Flask scraper backend"
echo "  - Setup database (migrations if needed)"
echo "  - Start .NET backend"
echo "  - Health check .NET backend"
echo "  - Transfer any cached data to database"
echo "  - Open dashboard"
echo ""

echo "⚠️  This will start the full application stack."
echo "Press Enter to continue or Ctrl+C to cancel..."
read

echo "🚀 Starting launch.sh..."
./launch.sh

echo ""
echo "✅ Launch script completed!"
echo "Check your browser - the dashboard should be open."
echo "Click 'Load Properties' in the Properties Database panel to see the data."
