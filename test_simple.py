#!/usr/bin/env python3
"""
Simple API test script
"""

import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

async def test_endpoints():
    async with httpx.AsyncClient() as client:
        print("🚀 Testing Ultimate Library API")
        print("=" * 40)
        
        # Test 1: Health check
        print("\n1. 🔍 Testing health endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return
        
        # Test 2: Root endpoint
        print("\n2. 🏠 Testing root endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 3: Books endpoint
        print("\n3. 📚 Testing books endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/books")
            print(f"   Status: {response.status_code}")
            data = response.json()
            print(f"   Total books: {data.get('totalItems', 0)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print("\n✅ Tests completed!")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
