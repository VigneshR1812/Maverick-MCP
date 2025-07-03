#!/usr/bin/env python3
"""
Test script to verify the Maverick MCP server functionality
"""

import asyncio
import json
from server import handle_list_tools, handle_call_tool

async def test_server():
    """Test the MCP server functionality"""
    print("🧪 Testing Maverick MCP Server...")
    print("=" * 50)
    
    # Test 1: List available tools
    print("\n1. Testing list_tools()...")
    try:
        tools = await handle_list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   • {tool.name}: {tool.description}")
    except Exception as e:
        print(f"❌ Error listing tools: {e}")
        return
    
    # Test 2: Test create_site tool (dry run)
    print("\n2. Testing create_site tool (dry run)...")
    try:
        result = await handle_call_tool("create_site", {
            "subdomain": "test-mcp-server",
            "purpose": "development",
            "dryRun": True
        })
        print(f"✅ Create site test result: {result[0].text}")
    except Exception as e:
        print(f"❌ Error testing create_site: {e}")
    
    # Test 3: Test query_sites tool
    print("\n3. Testing query_sites tool...")
    try:
        result = await handle_call_tool("query_sites", {
            "purpose": ["development"],
            "batchSize": 5
        })
        print(f"✅ Query sites test result: {result[0].text[:200]}...")
    except Exception as e:
        print(f"❌ Error testing query_sites: {e}")
    
    # Test 4: Test get_site_by_id tool
    print("\n4. Testing get_site_by_id tool...")
    try:
        result = await handle_call_tool("get_site_by_id", {
            "identifier": "1004544"
        })
        print(f"✅ Get site by ID test result: {result[0].text[:200]}...")
    except Exception as e:
        print(f"❌ Error testing get_site_by_id: {e}")
    
    # Test 5: Test manage_site tool (dry run)
    print("\n5. Testing manage_site tool (dry run start)...")
    try:
        result = await handle_call_tool("manage_site", {
            "identifier": "1004544",
            "action": "start",
            "dryRun": True
        })
        print(f"✅ Manage site test result: {result[0].text}")
    except Exception as e:
        print(f"❌ Error testing manage_site: {e}")
    
    # Test 6: Test get_site_resize_status tool
    print("\n6. Testing get_site_resize_status tool...")
    try:
        result = await handle_call_tool("get_site_resize_status", {
            "siteId": "1004544"
        })
        print(f"✅ Resize status test result: {result[0].text[:200]}...")
    except Exception as e:
        print(f"❌ Error testing get_site_resize_status: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 MCP Server test completed!")
    print("\nNext steps:")
    print("1. Set your MAVERICK_API_TOKEN environment variable")
    print("2. Configure the server in Amazon Q CLI")
    print("3. Test with real API calls")

if __name__ == "__main__":
    asyncio.run(test_server())
