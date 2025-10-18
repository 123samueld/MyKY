#!/usr/bin/env python3
"""
Script to clean up duplicate properties from the database
"""
import requests
import json

API_BASE_URL = "http://localhost:5000/api"

def get_properties():
    """Get all properties from the database"""
    try:
        response = requests.get(f"{API_BASE_URL}/property")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get properties: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return []

def find_duplicates(properties):
    """Find duplicate properties based on price and fullAddress"""
    seen = set()
    duplicates = []
    
    for prop in properties:
        key = (prop['price'], prop['fullAddress'])
        if key in seen:
            duplicates.append(prop)
        else:
            seen.add(key)
    
    return duplicates

def main():
    print("🧹 Cleaning up duplicate properties...")
    
    # Get all properties
    properties = get_properties()
    if not properties:
        print("❌ No properties found")
        return
    
    print(f"📊 Found {len(properties)} total properties")
    
    # Find duplicates
    duplicates = find_duplicates(properties)
    print(f"🔍 Found {len(duplicates)} duplicate properties")
    
    if duplicates:
        print("📋 Duplicate properties:")
        for dup in duplicates:
            print(f"  - ID {dup['id']}: {dup['price']} - {dup['fullAddress']}")
        
        print("\n⚠️  Note: This script only identifies duplicates.")
        print("To remove them, you would need to implement a DELETE endpoint")
        print("or manually clean the database.")
    else:
        print("✅ No duplicates found!")

if __name__ == "__main__":
    main()
