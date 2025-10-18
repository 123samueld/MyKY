# How The Main Components Work Together

This document explains how the different components of the MyKY application interact with each other to create a complete real estate data scraping and management system.

## 🏗️ System Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ScrapeSystem  │───▶│  DatabaseSystem │───▶│    Dashboard     │
│   (Python)      │    │    (.NET)       │    │    (HTML/JS)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  BackupSystem   │    │   FileSystem    │    │   UserInterface │
│   (Future)      │    │   (Cache/Logs)  │    │   (Browser)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 Data Flow Process

### 1. **ScrapeSystem** (Python Backend)
- **Purpose**: Scrapes real estate data from various websites
- **Technology**: Python with Playwright for browser automation
- **Components**:
  - `landsearch_scraper.py` - Scrapes LandSearch.com
  - `zillow_scraper.py` - Scrapes Zillow (placeholder)
  - `landwatch_scraper.py` - Scrapes LandWatch (placeholder)
  - `scraper_central_nexus.py` - Coordinates all scrapers
  - `scraper_endpoint.py` - Flask API for scraper control
  - `post_to_database.py` - Transfers scraped data to database

### 2. **DatabaseSystem** (.NET Backend)
- **Purpose**: Stores and manages scraped property data
- **Technology**: .NET 6 with Entity Framework Core and SQLite
- **Components**:
  - `PropertyController.cs` - REST API endpoints for properties
  - `MyKYDbContext.cs` - Database context and configuration
  - `Property.cs` - Data model for property records
  - `Program.cs` - Application startup and configuration

### 3. **Dashboard** (Frontend Interface)
- **Purpose**: User interface for viewing and managing data
- **Technology**: HTML, CSS, JavaScript with modern UI
- **Components**:
  - `dashboard.html` - Main dashboard interface
  - `countymap.js` - Interactive map functionality
  - `mapdata.js` - Map data and configuration
  - Various modal dialogs for different functions

### 4. **BackupSystem** (Future Component)
- **Purpose**: Data backup, recovery, and archival
- **Status**: 🚧 **Planned for Future Development**
- **Planned Features**:
  - Automated database backups
  - Scraped data archival
  - System restore capabilities
  - Data export/import functionality

## 🔗 Component Interactions

### **Scraper → Database Flow**
```
Python Scraper → Cache JSON → post_to_database.py → HTTP POST → .NET API → SQLite Database
```

1. **Data Collection**: Scrapers collect property data from websites
2. **Caching**: Data is stored in JSON cache files
3. **Transfer**: `post_to_database.py` reads cache and POSTs to .NET API
4. **Storage**: .NET backend stores data in SQLite database

### **Database → Dashboard Flow**
```
SQLite Database → .NET API → HTTP GET → Dashboard JavaScript → UI Display
```

1. **Data Retrieval**: Dashboard requests data via API calls
2. **Processing**: .NET backend queries database and returns JSON
3. **Display**: Dashboard renders data in user-friendly format

### **User Control Flow**
```
User Action → Dashboard → .NET API → Database → Response → Dashboard → User
```

1. **User Interaction**: User clicks buttons or loads pages
2. **API Calls**: Dashboard makes HTTP requests to .NET backend
3. **Data Processing**: Backend processes requests and queries database
4. **Response**: Data is returned and displayed to user

## 🚀 Launch Sequence

### **Complete System Startup**
```
launch.sh → Flask Backend → Database Setup → .NET Backend → Health Check → Data Transfer → Dashboard
```

1. **Flask Backend**: Starts Python scraper API (port 5001)
2. **Database Setup**: Creates migrations and updates schema
3. **.NET Backend**: Starts database API (port 5000)
4. **Health Check**: Verifies all services are responding
5. **Data Transfer**: Moves cached scraped data to database
6. **Dashboard**: Opens browser interface

## 📊 Data Models

### **Property Data Structure Example**
```json
{
  "id": 1,
  "site": "landsearch",
  "address": "123 Main St",
  "fullAddress": "123 Main St, City, KY 12345",
  "streetAddress": "123 Main St",
  "price": "$100,000",
  "acres": "5.0 acres",
  "listedDate": "2025-01-17",
  "county": "Jefferson County",
  "elevation": "500 feet",
  "coordinates": "38.2527, -85.7585",
  "detailUrl": "https://example.com/property/123",
  "createdAt": "2025-01-17T12:00:00Z"
}
```

## 🔧 Configuration Files

### **Path Management**
- `FilePathCompendium.json` - Central path configuration
- `AppConfig.cs` - .NET path resolution
- `FilePathCompendium.cs` - C# path utilities

### **Dependencies**
- `requirements.txt` - Python package dependencies
- `MyKYWeb.csproj` - .NET project dependencies
- `launch.sh` - System startup script

## 🧪 Testing Components

### **Test Files** (`Utilities/Tests/`)
- `test_data_flow.sh` - Tests complete Python → .NET → Database flow
- `test_launch_flow.sh` - Tests complete launch.sh script
- `test_dashboard_flow.html` - Web-based dashboard API tests
- `test_paths.sh` - Validates file path configuration

### **Setup Files** (`Utilities/`)
- `setup_database.sh` - Database initialization
- `update_chromium_and_driver.sh` - Browser driver updates

## 🔄 Future Integration Points

### **BackupSystem Integration** (Planned)
```
BackupSystem ←→ DatabaseSystem ←→ ScrapeSystem
     ↓              ↓              ↓
  Archive Data   Store Data    Collect Data
```

- **Scheduled Backups**: Automated database backups
- **Data Archival**: Long-term storage of scraped data
- **Recovery**: System restore capabilities
- **Export/Import**: Data portability features

## 🎯 Key Benefits of This Architecture

1. **Modular Design**: Each component can be developed and tested independently
2. **Scalable**: Easy to add new scrapers or data sources
3. **Maintainable**: Clear separation of concerns
4. **Extensible**: Ready for future components like BackupSystem
5. **User-Friendly**: Intuitive dashboard interface
6. **Robust**: Error handling and health checks throughout

## 🔍 Troubleshooting

### **Common Issues**
- **Duplicate Data**: Fixed with duplicate prevention in data transfer
- **Port Conflicts**: Managed by kill_protocol.sh
- **Missing Dependencies**: Handled by automated installation scripts
- **Database Issues**: Resolved with migration management

### **Debug Tools**
- Launch script with verbose output
- Health check endpoints
- Test scripts for each component
- Log files for troubleshooting

This architecture provides a solid foundation for a comprehensive real estate data management system, with clear paths for future expansion and enhancement.
