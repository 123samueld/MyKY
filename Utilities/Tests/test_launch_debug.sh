#!/bin/bash

echo "🔍 Debug Launch Script - Database Initialization"
echo "================================================"

# Change to the project directory
cd /home/samuel/Desktop/MyKY

echo "1️⃣ Checking for existing .NET processes..."
pgrep -f "dotnet.*MyKYWeb" && echo "Found existing .NET processes" || echo "No existing .NET processes"

echo "2️⃣ Testing database update without starting app..."
cd DatabaseSystem/MyKYWeb

echo "Running: dotnet ef database update --no-build"
timeout 10s dotnet ef database update --no-build 2>&1 | head -10

echo "3️⃣ Checking if app started during database update..."
pgrep -f "dotnet.*MyKYWeb" && echo "App started during database update!" || echo "App did not start during database update"

echo "4️⃣ Cleanup any processes that started..."
pkill -f "dotnet.*MyKYWeb" 2>/dev/null || true

echo "✅ Debug complete"
