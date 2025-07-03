import asyncio
import json
import os
from typing import Any, Dict, List, Optional
import httpx
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

server = Server("maverick")

# Configuration
MAVERICK_BASE_URL = os.getenv("MAVERICK_BASE_URL", "https://maverick-staging.appiancloud.com")
MAVERICK_API_TOKEN = os.getenv("MAVERICK_API_TOKEN")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available Maverick tools"""
    return [
        types.Tool(
            name="create_site",
            description="Creates a new Maverick site with specified configuration",
            inputSchema={
                "type": "object",
                "properties": {
                    "subdomain": {
                        "type": "string",
                        "description": "Required. The site name/subdomain"
                    },
                    "installer": {
                        "type": "string",
                        "description": "Version of Appian to start the site with (e.g., '22.1.235.0')"
                    },
                    "installerLabel": {
                        "type": "string",
                        "description": "Installer label of Appian (e.g., '22.1-latest')"
                    },
                    "accountName": {
                        "type": "string",
                        "description": "Account to create the site in"
                    },
                    "region": {
                        "type": "string",
                        "description": "AWS region (e.g., 'us-east-1')"
                    },
                    "clusterVersion": {
                        "type": "string",
                        "description": "EKS version of the cluster (e.g., '1.21')"
                    },
                    "serverSize": {
                        "type": "string",
                        "description": "Server size (e.g., 'm5.large')"
                    },
                    "volumeSize": {
                        "type": "integer",
                        "description": "Volume size in GB (defaults to 50)"
                    },
                    "customerName": {
                        "type": "string",
                        "enum": ["Appian Engineering", "Appian Marketing", "Appian Training"],
                        "description": "Customer associated with the site"
                    },
                    "purpose": {
                        "type": "string",
                        "enum": [
                            "bugbounty", "community", "customerdev", "customerstaging",
                            "customerprod", "customertest", "customertraining", "demo",
                            "development", "externaltraining", "hackathon", "internaltraining", "partner"
                        ],
                        "description": "Purpose of the site"
                    },
                    "rpaEnabled": {
                        "type": "boolean",
                        "description": "Enable or disable RPA"
                    },
                    "rpaLabel": {
                        "type": "string",
                        "description": "RPA label to use (defaults to 'production-latest')"
                    },
                    "rpaVersion": {
                        "type": "string",
                        "description": "RPA version to use"
                    },
                    "encrypted": {
                        "type": "boolean",
                        "description": "Enable site node volume encryption (defaults to true)"
                    },
                    "expiresOn": {
                        "type": "string",
                        "description": "UTC timestamp when site expires (YYYY-MM-DDTHH:MM:ss:00Z)"
                    },
                    "ami": {
                        "type": "string",
                        "description": "Specific AMI ID to use"
                    },
                    "topology": {
                        "type": "string",
                        "enum": ["single", "ha", "distributed-3", "distributed-9"],
                        "description": "Site topology"
                    },
                    "isRecurring": {
                        "type": "boolean",
                        "description": "Whether site should restart with newer hotfix installers"
                    },
                    "immediatelyRecurring": {
                        "type": "boolean",
                        "description": "Restart immediately when new version available"
                    },
                    "timeToRestartSite": {
                        "type": "string",
                        "description": "Preferred restart time in GMT (hh:mm AM/PM format)"
                    },
                    "requestorFirstName": {
                        "type": "string",
                        "description": "First name of requestor"
                    },
                    "requestorLastName": {
                        "type": "string",
                        "description": "Last name of requestor"
                    },
                    "requestorEmail": {
                        "type": "string",
                        "description": "Email of requestor"
                    },
                    "siteProperties": {
                        "type": "object",
                        "description": "Custom properties for the site"
                    },
                    "siteLabels": {
                        "type": "object",
                        "description": "Labels to associate with the site"
                    },
                    "restoreSpec": {
                        "type": "object",
                        "properties": {
                            "siteID": {"type": "string"},
                            "createdAt": {"type": "string"}
                        },
                        "description": "Snapshot to restore from"
                    },
                    "siteTestConfig": {
                        "type": "object",
                        "properties": {
                            "importOneApp": {"type": "boolean"},
                            "selectedApplications": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "description": "Test configuration for the site"
                    },
                    "featureToggleOverrides": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Feature toggle overrides"
                    },
                    "dryRun": {
                        "type": "boolean",
                        "description": "Perform a dry run validation (defaults to false)"
                    }
                },
                "required": ["subdomain"]
            }
        ),
        types.Tool(
            name="query_sites",
            description="Query Maverick sites using various filters and criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "siteId": {
                        "type": "string",
                        "description": "Query by specific site ID or site name"
                    },
                    "siteList": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Query by multiple site IDs (comma-delimited list)"
                    },
                    "purpose": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by site purpose(s)"
                    },
                    "region": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by AWS region(s)"
                    },
                    "accountName": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by account name(s)"
                    },
                    "createdAfter": {
                        "type": "string",
                        "description": "Sites created after this time (MM/DD/YYYY hh:mm:ss AM/PM GMT or ISO8601)"
                    },
                    "createdBefore": {
                        "type": "string",
                        "description": "Sites created before this time (MM/DD/YYYY hh:mm:ss AM/PM GMT or ISO8601)"
                    },
                    "modifiedAfter": {
                        "type": "string",
                        "description": "Sites modified after this time (MM/DD/YYYY hh:mm:ss AM/PM GMT or ISO8601)"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["Active", "All", "Shutdown", "Error Starting", "Error Stopping", "Unknown", "Ready"],
                        "description": "Filter by site status"
                    },
                    "labelName": {
                        "type": "string",
                        "description": "Filter by label name (must be used with labelValue)"
                    },
                    "labelValue": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by label value(s) (must be used with labelName)"
                    },
                    "startIndex": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Starting index for pagination (defaults to 1)"
                    },
                    "batchSize": {
                        "type": "integer",
                        "minimum": -1,
                        "description": "Number of results per page (defaults to 20, -1 for all)"
                    }
                }
            }
        ),
        types.Tool(
            name="get_site_by_id",
            description="Get detailed information about a specific site by ID or name",
            inputSchema={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "Site ID (numeric) or site name/subdomain"
                    }
                },
                "required": ["identifier"]
            }
        ),
        types.Tool(
            name="manage_site",
            description="Perform actions on existing Maverick sites (start, stop, restart, delete, edit, clone, move, resize, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "identifier": {
                        "type": "string",
                        "description": "Site ID (numeric) or site name/subdomain"
                    },
                    "action": {
                        "type": "string",
                        "enum": [
                            "start", "restart", "stop", "force-stop", "force-restart", 
                            "delete", "revert", "on-demand-backup", "edit", "clone", 
                            "move", "resize"
                        ],
                        "description": "Action to perform on the site"
                    },
                    "dryRun": {
                        "type": "boolean",
                        "description": "Perform a dry run validation (defaults to false)"
                    },
                    "ami": {
                        "type": "string",
                        "description": "Specific AMI ID to use (edit action)"
                    },
                    "customerName": {
                        "type": "string",
                        "enum": ["Appian Engineering", "Appian Marketing", "Appian Training"],
                        "description": "Customer associated with the site (edit action)"
                    },
                    "expiresOn": {
                        "type": "string",
                        "description": "UTC timestamp when site expires (edit action)"
                    },
                    "installer": {
                        "type": "string",
                        "description": "Appian version (edit action)"
                    },
                    "installerLabel": {
                        "type": "string",
                        "description": "Installer label (edit action)"
                    },
                    "isRecurring": {
                        "type": "boolean",
                        "description": "Whether site should restart with newer hotfix installers (edit action)"
                    },
                    "immediatelyRecurring": {
                        "type": "boolean",
                        "description": "Restart immediately when new version available (edit action)"
                    },
                    "timeToRestartSite": {
                        "type": "string",
                        "description": "Preferred restart time in GMT (edit action)"
                    },
                    "purpose": {
                        "type": "string",
                        "enum": [
                            "development", "internaltraining", "externaltraining", "customerdev",
                            "customerstaging", "customerprod", "bugbounty", "community", 
                            "hackathon", "partner"
                        ],
                        "description": "Purpose of the site (edit action)"
                    },
                    "rpaEnabled": {
                        "type": "boolean",
                        "description": "Enable or disable RPA (edit action)"
                    },
                    "rpaLabel": {
                        "type": "string",
                        "description": "RPA label to use (edit action)"
                    },
                    "rpaVersion": {
                        "type": "string",
                        "description": "RPA version to use (edit action)"
                    },
                    "serverSize": {
                        "type": "string",
                        "description": "Server size (edit action)"
                    },
                    "siteProperties": {
                        "type": "object",
                        "description": "Custom properties for the site (edit action)"
                    },
                    "subdomain": {
                        "type": "string",
                        "description": "Site subdomain (edit action)"
                    },
                    "domain": {
                        "type": "string",
                        "description": "Site domain (edit action)"
                    },
                    "restoreSpec": {
                        "type": "object",
                        "properties": {
                            "siteID": {"type": "string"},
                            "createdAt": {"type": "string"}
                        },
                        "description": "Snapshot to restore from (revert action)"
                    },
                    "reason": {
                        "type": "string",
                        "description": "Reason for requesting the clone site (clone action)"
                    },
                    "requestorFirstName": {
                        "type": "string",
                        "description": "First name of requestor (clone action)"
                    },
                    "requestorLastName": {
                        "type": "string",
                        "description": "Last name of requestor (clone action)"
                    },
                    "requestorEmail": {
                        "type": "string",
                        "description": "Email of requestor (clone action)"
                    },
                    "supportCase": {
                        "type": "string",
                        "description": "Forum ticket number (clone action)"
                    },
                    "topology": {
                        "type": "string",
                        "enum": ["single", "ha", "distributed-3", "distributed-9"],
                        "description": "Site topology (clone action)"
                    },
                    "volumeSize": {
                        "type": "integer",
                        "description": "Volume size in GB (clone/resize action)"
                    },
                    "cluster": {
                        "type": "string",
                        "description": "Cluster name (clone action)"
                    },
                    "isWebAndEmailAccessible": {
                        "type": "boolean",
                        "description": "Allow web and email access for clone (clone action)"
                    },
                    "region": {
                        "type": "string",
                        "description": "Target region (move action)"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email for notifications (move action)"
                    }
                },
                "required": ["identifier", "action"]
            }
        ),
        types.Tool(
            name="get_site_resize_status",
            description="Get the status of an ongoing site resize operation",
            inputSchema={
                "type": "object",
                "properties": {
                    "siteId": {
                        "type": "string",
                        "description": "Site ID to check resize status for"
                    }
                },
                "required": ["siteId"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    if name == "create_site":
        return await create_site(arguments)
    elif name == "query_sites":
        return await query_sites(arguments)
    elif name == "get_site_by_id":
        return await get_site_by_id(arguments)
    elif name == "manage_site":
        return await manage_site(arguments)
    elif name == "get_site_resize_status":
        return await get_site_resize_status(arguments)
    
    raise ValueError(f"Unknown tool: {name}")

async def create_site(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Create a new Maverick site"""
    if not MAVERICK_API_TOKEN:
        return [types.TextContent(
            type="text",
            text="Error: MAVERICK_API_TOKEN environment variable not set"
        )]
    
    # Extract dry run parameter
    dry_run = arguments.pop("dryRun", False)
    
    # Build the request URL
    url = f"{MAVERICK_BASE_URL}/suite/webapi/sites"
    if dry_run:
        url += "?dryRun=true"
    
    # Prepare headers
    headers = {
        "appian-api-key": MAVERICK_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=arguments,
                headers=headers,
                timeout=30.0
            )
            
            # Handle different response codes
            if response.status_code == 201:
                result = response.json()
                return [types.TextContent(
                    type="text",
                    text=f"✅ Site created successfully: {result.get('message', 'Site created')}"
                )]
            elif response.status_code == 400:
                error_data = response.json()
                errors = error_data.get('errors', ['Validation error'])
                return [types.TextContent(
                    type="text",
                    text=f"❌ Validation errors:\n" + "\n".join(f"• {error}" for error in errors)
                )]
            elif response.status_code == 405:
                return [types.TextContent(
                    type="text",
                    text="✅ Dry run successful - no validation errors found. Site would be created if dryRun=false"
                )]
            elif response.status_code == 500:
                return [types.TextContent(
                    type="text",
                    text="❌ Internal server error occurred"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Unexpected response: {response.status_code} - {response.text}"
                )]
                
    except httpx.TimeoutException:
        return [types.TextContent(
            type="text",
            text="❌ Request timed out"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error creating site: {str(e)}"
        )]

async def query_sites(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Query sites with various filters"""
    if not MAVERICK_API_TOKEN:
        return [types.TextContent(
            type="text",
            text="Error: MAVERICK_API_TOKEN environment variable not set"
        )]
    
    # Build query parameters
    params = {}
    
    # Handle different query types
    if "siteList" in arguments and arguments["siteList"]:
        params["siteList"] = ",".join(str(site_id) for site_id in arguments["siteList"])
    
    if "purpose" in arguments and arguments["purpose"]:
        params["purpose"] = ",".join(arguments["purpose"])
    
    if "region" in arguments and arguments["region"]:
        params["region"] = ",".join(arguments["region"])
    
    if "accountName" in arguments and arguments["accountName"]:
        params["accountName"] = ",".join(arguments["accountName"])
    
    if "createdAfter" in arguments:
        params["createdAfter"] = arguments["createdAfter"]
    
    if "createdBefore" in arguments:
        params["createdBefore"] = arguments["createdBefore"]
    
    if "modifiedAfter" in arguments:
        params["modifiedAfter"] = arguments["modifiedAfter"]
    
    if "status" in arguments:
        params["status"] = arguments["status"]
    
    if "labelName" in arguments and "labelValue" in arguments:
        params["labelName"] = arguments["labelName"]
        params["labelValue"] = ",".join(arguments["labelValue"])
    
    # Pagination parameters
    if "startIndex" in arguments:
        params["startIndex"] = arguments["startIndex"]
    
    if "batchSize" in arguments:
        params["batchSize"] = arguments["batchSize"]
    
    # Build the request URL
    url = f"{MAVERICK_BASE_URL}/suite/webapi/sites"
    
    # Prepare headers
    headers = {
        "appian-api-key": MAVERICK_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
                timeout=30.0
            )
            
            # Handle different response codes
            if response.status_code == 200:
                sites = response.json()
                total_count = response.headers.get("X-Total-Count", "Unknown")
                
                if not sites:
                    return [types.TextContent(
                        type="text",
                        text="No sites found matching the query criteria."
                    )]
                
                # Format the response
                result = f"Found {len(sites)} sites (Total matching: {total_count})\n\n"
                
                for site in sites:
                    result += format_site_info(site) + "\n" + "="*50 + "\n"
                
                return [types.TextContent(type="text", text=result)]
                
            elif response.status_code == 204:
                return [types.TextContent(
                    type="text",
                    text="No sites found matching the query criteria."
                )]
            elif response.status_code == 400:
                error_data = response.json()
                errors = error_data.get('errors', ['Validation error'])
                return [types.TextContent(
                    type="text",
                    text=f"❌ Validation errors:\n" + "\n".join(f"• {error}" for error in errors)
                )]
            elif response.status_code == 500:
                return [types.TextContent(
                    type="text",
                    text="❌ Internal server error occurred"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Unexpected response: {response.status_code} - {response.text}"
                )]
                
    except httpx.TimeoutException:
        return [types.TextContent(
            type="text",
            text="❌ Request timed out"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error querying sites: {str(e)}"
        )]

async def get_site_by_id(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Get a specific site by ID or name"""
    if not MAVERICK_API_TOKEN:
        return [types.TextContent(
            type="text",
            text="Error: MAVERICK_API_TOKEN environment variable not set"
        )]
    
    identifier = arguments.get("identifier")
    if not identifier:
        return [types.TextContent(
            type="text",
            text="❌ Site identifier is required"
        )]
    
    # Build the request URL
    url = f"{MAVERICK_BASE_URL}/suite/webapi/sites/{identifier}"
    
    # Prepare headers
    headers = {
        "appian-api-key": MAVERICK_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                timeout=30.0
            )
            
            # Handle different response codes
            if response.status_code == 200:
                sites = response.json()
                
                # Handle both single site and multiple sites with same name
                if isinstance(sites, list):
                    if len(sites) == 0:
                        return [types.TextContent(
                            type="text",
                            text=f"No site found with identifier: {identifier}"
                        )]
                    
                    result = f"Found {len(sites)} site(s) with identifier '{identifier}':\n\n"
                    for site in sites:
                        result += format_site_info(site) + "\n" + "="*50 + "\n"
                else:
                    result = f"Site details for '{identifier}':\n\n"
                    result += format_site_info(sites)
                
                return [types.TextContent(type="text", text=result)]
                
            elif response.status_code == 404:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Site not found: {identifier}"
                )]
            elif response.status_code == 400:
                error_data = response.json()
                errors = error_data.get('errors', ['Validation error'])
                return [types.TextContent(
                    type="text",
                    text=f"❌ Validation errors:\n" + "\n".join(f"• {error}" for error in errors)
                )]
            elif response.status_code == 500:
                return [types.TextContent(
                    type="text",
                    text="❌ Internal server error occurred"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Unexpected response: {response.status_code} - {response.text}"
                )]
                
    except httpx.TimeoutException:
        return [types.TextContent(
            type="text",
            text="❌ Request timed out"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error getting site: {str(e)}"
        )]

def format_site_info(site: Dict[str, Any]) -> str:
    """Format site information for display"""
    info = []
    
    # Basic site information
    info.append(f"🏷️  Site ID: {site.get('siteId', 'N/A')}")
    info.append(f"🌐 Site URL: {site.get('siteUrl', 'N/A')}")
    info.append(f"📝 Subdomain: {site.get('subdomain', 'N/A')}")
    info.append(f"📊 Status: {site.get('status', 'N/A')}")
    info.append(f"🔄 Active: {'Yes' if site.get('isActive') else 'No'}")
    
    # Technical details
    info.append(f"⚙️  Installer: {site.get('installer', 'N/A')}")
    if site.get('installerLabel'):
        info.append(f"🏷️  Installer Label: {site.get('installerLabel')}")
    info.append(f"🌍 Region: {site.get('region', 'N/A')}")
    info.append(f"🖥️  Server Size: {site.get('serverSize', 'N/A')}")
    info.append(f"💾 Volume Size: {site.get('volumeSize', 'N/A')} GB")
    info.append(f"🏗️  Topology: {site.get('topology', 'N/A')}")
    
    # Account and customer info
    info.append(f"🏢 Customer: {site.get('customerName', 'N/A')}")
    info.append(f"📁 Account: {site.get('accountName', 'N/A')}")
    info.append(f"🎯 Purpose: {site.get('purpose', 'N/A')}")
    
    # Dates
    info.append(f"📅 Created: {site.get('createdOn', 'N/A')}")
    info.append(f"👤 Created By: {site.get('createdBy', 'N/A')}")
    info.append(f"🔄 Updated: {site.get('updatedOn', 'N/A')}")
    info.append(f"👤 Updated By: {site.get('updatedBy', 'N/A')}")
    
    if site.get('startedOn'):
        info.append(f"🚀 Started: {site.get('startedOn')}")
    if site.get('shutdownOn'):
        info.append(f"🛑 Shutdown: {site.get('shutdownOn')}")
    
    # RPA info
    if site.get('rpaEnabled'):
        info.append(f"🤖 RPA Enabled: Yes")
        if site.get('rpaVersion'):
            info.append(f"🤖 RPA Version: {site.get('rpaVersion')}")
        if site.get('rpaLabel'):
            info.append(f"🤖 RPA Label: {site.get('rpaLabel')}")
    else:
        info.append(f"🤖 RPA Enabled: No")
    
    # Security
    info.append(f"🔒 Encrypted: {'Yes' if site.get('encrypted') else 'No'}")
    
    # Requestor info
    if site.get('requestorFirstName') or site.get('requestorLastName'):
        requestor_name = f"{site.get('requestorFirstName', '')} {site.get('requestorLastName', '')}".strip()
        info.append(f"👤 Requestor: {requestor_name}")
    if site.get('requestorEmail'):
        info.append(f"📧 Requestor Email: {site.get('requestorEmail')}")
    
    # Labels
    if site.get('siteLabels'):
        info.append("🏷️  Labels:")
        for key, value in site.get('siteLabels', {}).items():
            info.append(f"   • {key}: {value}")
    
    # Properties (show first few)
    if site.get('siteProperties'):
        info.append("⚙️  Properties:")
        props = site.get('siteProperties', {})
        for i, (key, value) in enumerate(props.items()):
            if i < 5:  # Show first 5 properties
                info.append(f"   • {key}: {value}")
            elif i == 5:
                info.append(f"   • ... and {len(props) - 5} more properties")
                break
    
    # Record link
    if site.get('recordLink'):
        info.append(f"🔗 Record Link: {site.get('recordLink')}")
    
    return "\n".join(info)

async def manage_site(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Manage a Maverick site (start, stop, restart, delete, edit, clone, move, resize, etc.)"""
    if not MAVERICK_API_TOKEN:
        return [types.TextContent(
            type="text",
            text="Error: MAVERICK_API_TOKEN environment variable not set"
        )]
    
    identifier = arguments.get("identifier")
    action = arguments.get("action")
    dry_run = arguments.get("dryRun", False)
    
    if not identifier or not action:
        return [types.TextContent(
            type="text",
            text="❌ Both identifier and action are required"
        )]
    
    # Build the request URL
    url = f"{MAVERICK_BASE_URL}/suite/webapi/sites/{identifier}"
    params = {"action": action}
    if dry_run:
        params["dryRun"] = "true"
    
    # Prepare headers
    headers = {
        "appian-api-key": MAVERICK_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Prepare request body based on action
    request_body = {}
    
    if action == "edit":
        # Edit action - include all edit-specific fields
        edit_fields = [
            "ami", "customerName", "expiresOn", "installer", "installerLabel",
            "isRecurring", "immediatelyRecurring", "timeToRestartSite", "purpose",
            "rpaEnabled", "rpaLabel", "rpaVersion", "serverSize", "siteProperties",
            "subdomain", "domain"
        ]
        for field in edit_fields:
            if field in arguments:
                request_body[field] = arguments[field]
    
    elif action == "revert":
        # Revert action - requires restoreSpec
        if "restoreSpec" in arguments:
            request_body["restoreSpec"] = arguments["restoreSpec"]
        else:
            return [types.TextContent(
                type="text",
                text="❌ Revert action requires restoreSpec with siteID and createdAt"
            )]
    
    elif action == "clone":
        # Clone action - requires specific fields
        required_clone_fields = ["reason", "requestorFirstName", "requestorLastName", "requestorEmail", "supportCase"]
        for field in required_clone_fields:
            if field not in arguments:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Clone action requires field: {field}"
                )]
            request_body[field] = arguments[field]
        
        # Optional clone fields
        optional_clone_fields = [
            "topology", "subdomain", "volumeSize", "cluster", "expiresOn",
            "installer", "installerLabel", "purpose", "customerName", "serverSize",
            "restoreSpec", "isWebAndEmailAccessible"
        ]
        for field in optional_clone_fields:
            if field in arguments:
                request_body[field] = arguments[field]
    
    elif action == "move":
        # Move action - requires region
        if "region" not in arguments:
            return [types.TextContent(
                type="text",
                text="❌ Move action requires region field"
            )]
        request_body["region"] = arguments["region"]
        if "email" in arguments:
            request_body["email"] = arguments["email"]
    
    elif action == "resize":
        # Resize action - requires volumeSize
        if "volumeSize" not in arguments:
            return [types.TextContent(
                type="text",
                text="❌ Resize action requires volumeSize field"
            )]
        request_body["volumeSize"] = arguments["volumeSize"]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                url,
                params=params,
                json=request_body if request_body else None,
                headers=headers,
                timeout=30.0
            )
            
            # Handle different response codes
            if response.status_code == 200:
                result = response.json()
                action_emoji = {
                    "start": "🚀", "restart": "🔄", "stop": "🛑", "force-stop": "⚠️🛑",
                    "force-restart": "⚠️🔄", "delete": "🗑️", "revert": "⏪", 
                    "on-demand-backup": "💾", "edit": "✏️", "clone": "👥", 
                    "move": "📦", "resize": "📏"
                }.get(action, "⚙️")
                
                return [types.TextContent(
                    type="text",
                    text=f"{action_emoji} {result.get('message', f'Site {action} completed successfully')}"
                )]
            elif response.status_code == 400:
                error_data = response.json()
                errors = error_data.get('errors', ['Validation error'])
                return [types.TextContent(
                    type="text",
                    text=f"❌ Validation errors:\n" + "\n".join(f"• {error}" for error in errors)
                )]
            elif response.status_code == 403:
                return [types.TextContent(
                    type="text",
                    text="❌ Multiple sites found with the same name. Please use site ID instead."
                )]
            elif response.status_code == 404:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Site not found: {identifier}"
                )]
            elif response.status_code == 405:
                return [types.TextContent(
                    type="text",
                    text=f"✅ Dry run successful - no validation errors found. {action.title()} would be executed if dryRun=false"
                )]
            elif response.status_code == 500:
                return [types.TextContent(
                    type="text",
                    text="❌ Internal server error occurred"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Unexpected response: {response.status_code} - {response.text}"
                )]
                
    except httpx.TimeoutException:
        return [types.TextContent(
            type="text",
            text="❌ Request timed out"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error managing site: {str(e)}"
        )]

async def get_site_resize_status(arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Get the status of an ongoing site resize operation"""
    if not MAVERICK_API_TOKEN:
        return [types.TextContent(
            type="text",
            text="Error: MAVERICK_API_TOKEN environment variable not set"
        )]
    
    site_id = arguments.get("siteId")
    if not site_id:
        return [types.TextContent(
            type="text",
            text="❌ Site ID is required"
        )]
    
    # Build the request URL
    url = f"{MAVERICK_BASE_URL}/suite/webapi/resizes/{site_id}"
    
    # Prepare headers
    headers = {
        "appian-api-key": MAVERICK_API_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                timeout=30.0
            )
            
            # Handle different response codes
            if response.status_code == 200:
                result = response.json()
                phase = result.get("phase", "Unknown")
                last_mod_time = result.get("lastVolumeModificationTime", "Unknown")
                
                status_emoji = {
                    "Complete": "✅",
                    "Optimizing": "⚙️",
                    "In Progress": "🔄",
                    "Pending": "⏳"
                }.get(phase, "📊")
                
                return [types.TextContent(
                    type="text",
                    text=f"{status_emoji} Resize Status for Site {site_id}:\n\n"
                         f"📊 Phase: {phase}\n"
                         f"⏰ Last Volume Modification: {last_mod_time}\n\n"
                         f"ℹ️  Note: If phase is 'Complete', the system is waiting out the 6-hour rate limit."
                )]
            elif response.status_code == 404:
                return [types.TextContent(
                    type="text",
                    text=f"✅ No resize operation in progress for site {site_id}. A new resize can be initiated."
                )]
            elif response.status_code == 500:
                return [types.TextContent(
                    type="text",
                    text="❌ Internal server error occurred"
                )]
            else:
                return [types.TextContent(
                    type="text",
                    text=f"❌ Unexpected response: {response.status_code} - {response.text}"
                )]
                
    except httpx.TimeoutException:
        return [types.TextContent(
            type="text",
            text="❌ Request timed out"
        )]
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error getting resize status: {str(e)}"
        )]

async def main():
    """Main server entry point"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="maverick",
                server_version="1.0.0",
                capabilities=types.ServerCapabilities(
                    tools=types.ToolsCapability(listChanged=True)
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
