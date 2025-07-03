#!/usr/bin/env python3
"""
Test script to verify Maverick API authentication methods
"""

import asyncio
import os
import httpx

MAVERICK_BASE_URL = os.getenv("MAVERICK_BASE_URL", "https://maverick-staging.appiancloud.com")
MAVERICK_API_TOKEN = os.getenv("MAVERICK_API_TOKEN")

async def test_authentication_methods():
    """Test different authentication methods supported by Maverick API"""
    
    if not MAVERICK_API_TOKEN:
        print("❌ MAVERICK_API_TOKEN environment variable not set")
        print("Please set your API token to test authentication:")
        print("export MAVERICK_API_TOKEN='your-api-key-here'")
        return
    
    print("🔐 Testing Maverick API Authentication Methods...")
    print("=" * 60)
    
    # Test endpoint - simple query to get sites
    url = f"{MAVERICK_BASE_URL}/suite/webapi/sites"
    params = {"batchSize": 1}  # Just get 1 site to test auth
    
    # Method 1: appian-api-key header (used by our server)
    print("\n1. Testing appian-api-key header...")
    try:
        headers = {
            "appian-api-key": MAVERICK_API_TOKEN,
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=10.0)
            if response.status_code in [200, 204]:
                print("✅ appian-api-key header: SUCCESS")
            else:
                print(f"❌ appian-api-key header: FAILED ({response.status_code})")
                print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ appian-api-key header: ERROR - {e}")
    
    # Method 2: Bearer token header
    print("\n2. Testing Authorization: Bearer header...")
    try:
        headers = {
            "Authorization": f"Bearer {MAVERICK_API_TOKEN}",
            "Content-Type": "application/json"
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers, timeout=10.0)
            if response.status_code in [200, 204]:
                print("✅ Bearer token header: SUCCESS")
            else:
                print(f"❌ Bearer token header: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Bearer token header: ERROR - {e}")
    
    # Method 3: Basic auth with null username
    print("\n3. Testing Basic auth (null username)...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, 
                params=params, 
                auth=("", MAVERICK_API_TOKEN),
                timeout=10.0
            )
            if response.status_code in [200, 204]:
                print("✅ Basic auth (null username): SUCCESS")
            else:
                print(f"❌ Basic auth (null username): FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Basic auth (null username): ERROR - {e}")
    
    # Method 4: Basic auth with null password
    print("\n4. Testing Basic auth (null password)...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url, 
                params=params, 
                auth=(MAVERICK_API_TOKEN, ""),
                timeout=10.0
            )
            if response.status_code in [200, 204]:
                print("✅ Basic auth (null password): SUCCESS")
            else:
                print(f"❌ Basic auth (null password): FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Basic auth (null password): ERROR - {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Authentication test completed!")
    print("\nThe MCP server uses the 'appian-api-key' header method.")
    print("If that method failed, you may need to check your API token or try a different method.")

if __name__ == "__main__":
    asyncio.run(test_authentication_methods())
