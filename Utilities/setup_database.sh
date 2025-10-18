#!/bin/bash

echo "🗄️ Setting up MyKY Database"
echo "============================"

# Change to the project directory
cd /home/samuel/Desktop/MyKY

echo "1️⃣ Checking Entity Framework tools..."
if command -v dotnet-ef &> /dev/null; then
    echo "✅ dotnet-ef found"
else
    echo "❌ dotnet-ef not found. Please install Entity Framework tools first."
    echo "Run: dotnet tool install --global dotnet-ef --version 6.0.0"
    echo "Then add to PATH: echo 'export PATH=\"\$PATH:\$HOME/.dotnet/tools\"' >> ~/.bashrc"
    exit 1
fi

echo "2️⃣ Creating database migration..."
cd DatabaseSystem/MyKYWeb

# Check if migrations already exist
if [ ! -d "Migrations" ]; then
    echo "📝 Creating initial migration..."
    dotnet ef migrations add InitialCreate
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create migration"
        exit 1
    fi
else
    echo "✅ Migrations already exist"
fi

echo "3️⃣ Creating/updating database..."
dotnet ef database update
if [ $? -ne 0 ]; then
    echo "❌ Failed to update database"
    exit 1
fi

echo "4️⃣ Verifying database..."
if [ -f "mykydb.db" ]; then
    echo "✅ Database file created: mykydb.db"
    ls -la mykydb.db
else
    echo "❌ Database file not found"
    exit 1
fi

echo ""
echo "🎉 Database setup complete!"
echo "You can now run ./Utilities/test_data_flow.sh to test the complete flow."
