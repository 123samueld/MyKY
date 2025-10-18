#!/bin/bash

echo "🧪 Testing Python → .NET Data Flow"
echo "=================================="

# Change to the project directory
cd /home/samuel/Desktop/MyKY

echo "1️⃣ Starting .NET backend..."
cd DatabaseSystem/MyKYWeb
dotnet run &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 20

echo "2️⃣ Creating database..."
# Check if ef tools are available
if command -v dotnet-ef &> /dev/null; then
    # Check if migrations exist, if not create them
    if [ ! -d "Migrations" ]; then
        echo "📝 Creating initial migration..."
        dotnet ef migrations add InitialCreate --no-build
    fi
    echo "🔄 Updating database..."
    dotnet ef database update --no-build
else
    echo "⚠️ dotnet-ef not found, trying alternative approach..."
    # Create database manually by running the app briefly
    timeout 5s dotnet run --no-build || true
fi

echo "3️⃣ Running Python script to POST data..."
cd ../../ScrapeSystem
python3 post_to_database.py

echo "4️⃣ Checking if data was inserted..."
cd ../DatabaseSystem/MyKYWeb

# Check if sqlite3 is available
if command -v sqlite3 &> /dev/null; then
    echo "📊 Properties in database:"
    sqlite3 mykydb.db "SELECT COUNT(*) as PropertyCount FROM Properties;" 2>/dev/null || echo "❌ Could not query database"
    echo ""
    echo "📋 Sample data:"
    sqlite3 mykydb.db "SELECT Id, site, price, acres, county FROM Properties LIMIT 3;" 2>/dev/null || echo "❌ Could not query sample data"
else
    echo "⚠️ sqlite3 not found, checking database file..."
    if [ -f "mykydb.db" ]; then
        echo "✅ Database file exists: mykydb.db"
        ls -la mykydb.db
    else
        echo "❌ Database file not found"
    fi
fi

echo ""
echo "5️⃣ Cleaning up..."
kill $BACKEND_PID 2>/dev/null
sleep 2

echo "✅ Test complete!"
