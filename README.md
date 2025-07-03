# Maverick MCP Server

An MCP (Model Context Protocol) server for managing Maverick sites through Amazon Q CLI.

## Features

- **Create Sites**: Create new Maverick sites with comprehensive configuration options
- **Query Sites**: Search and filter sites using various criteria
- **Get Site Details**: Retrieve detailed information about specific sites

## Installation

1. Install the package:
```bash
cd /Users/vigneshwaran.rajesh/companyWork/EE-hackathon/maverick-mcp
pip install -e .
pip install -r requirements.txt
```

2. Test the installation:
```bash
python3 test_server.py
```

3. Set up environment variables:
```bash
export MAVERICK_BASE_URL="https://maverick-staging.appiancloud.com"
export MAVERICK_API_TOKEN="your-api-token-here"
```

## Configuration for Amazon Q CLI

Add to your Q CLI MCP configuration file at `~/.aws/amazonq/mcp.json`:

```json
{
  "mcpServers": {
    "maverick": {
      "command": "python3",
      "args": ["/Users/vigneshwaran.rajesh/companyWork/EE-hackathon/maverick-mcp/server.py"],
      "env": {
        "MAVERICK_BASE_URL": "https://maverick-staging.appiancloud.com",
        "MAVERICK_API_TOKEN": "your-actual-api-token-here"
      }
    }
  }
}
```

**Note**: Use the full path to your server.py file in the configuration.

## Available Tools

### 1. `maverick___create_site`
Creates a new Maverick site with specified configuration.

**Required Parameters:**
- `subdomain`: The site name/subdomain

**Optional Parameters:**
- `installer`: Appian version (e.g., "22.1.235.0")
- `installerLabel`: Installer label (e.g., "22.1-latest")
- `region`: AWS region (e.g., "us-east-1")
- `serverSize`: Server size (e.g., "m5.large")
- `purpose`: Site purpose (development, hackathon, etc.)
- `customerName`: Customer name
- `dryRun`: Validate without creating (boolean)
- And many more configuration options...

### 2. `maverick___query_sites`
Query sites using various filters and criteria.

**Filter Options:**
- `siteList`: Array of site IDs
- `purpose`: Array of purposes to filter by
- `region`: Array of regions to filter by
- `accountName`: Array of account names
- `createdAfter`: Sites created after specified time
- `createdBefore`: Sites created before specified time
- `modifiedAfter`: Sites modified after specified time
- `status`: Site status (Active, Shutdown, etc.)
- `labelName` + `labelValue`: Filter by labels
- `startIndex`: Pagination start (default: 1)
- `batchSize`: Results per page (default: 20)

### 3. `maverick___get_site_by_id`
Get detailed information about a specific site.

**Parameters:**
- `identifier`: Site ID (numeric) or site name/subdomain

### 4. `maverick___manage_site`
Perform various actions on existing Maverick sites.

**Required Parameters:**
- `identifier`: Site ID (numeric) or site name/subdomain
- `action`: Action to perform

**Supported Actions:**
- `start`: Start a stopped site
- `restart`: Restart a running site
- `stop`: Stop a running site (data persists)
- `force-stop`: Force stop (bypasses standard checks)
- `force-restart`: Force restart (force stop + start)
- `delete`: Permanently delete a site
- `revert`: Revert site to a specific snapshot
- `on-demand-backup`: Take an on-demand backup
- `edit`: Edit site configuration
- `clone`: Create a copy of the site
- `move`: Move site to different region
- `resize`: Increase site volume size

**Action-Specific Parameters:**
- **Edit**: `installer`, `serverSize`, `purpose`, `siteProperties`, etc.
- **Revert**: `restoreSpec` (with `siteID` and `createdAt`)
- **Clone**: `reason`, `requestorFirstName`, `requestorLastName`, `requestorEmail`, `supportCase`
- **Move**: `region`, `email` (optional)
- **Resize**: `volumeSize`

### 5. `maverick___get_site_resize_status`
Check the status of an ongoing site resize operation.

**Parameters:**
- `siteId`: Site ID to check resize status for

## Usage Examples

### Create a Simple Site
```
Create a new Maverick site with subdomain "my-test-site"
```

### Create an Advanced Site
```
Create a Maverick site with subdomain "hackathon-site", purpose "hackathon", customer "Appian Engineering", server size "m5.large", and region "us-east-1"
```

### Query Sites by Purpose
```
Find all Maverick sites with purpose "development"
```

### Query Sites by Region
```
Show me all sites in us-east-1 and us-west-2 regions
```

### Query Recent Sites
```
Find all sites created after 01/01/2024
```

### Get Specific Site
```
Get details for Maverick site with ID 1004544
```

### Query with Pagination
```
Show me the first 10 active sites
```

### Site Management Actions
```
Start Maverick site with ID 1004544
```

```
Stop site "my-test-site" gracefully
```

```
Restart site 1004544 with force restart
```

```
Delete site "old-test-site" permanently
```

```
Take an on-demand backup of site 1004544
```

### Edit Site Configuration
```
Edit site 1004544 to change server size to "m5.xlarge" and purpose to "hackathon"
```

```
Update site "my-site" to use installer label "23.1-latest"
```

### Clone Site
```
Clone site 1004544 for debugging with reason "Reproduce customer issue" and support case "CN-1234"
```

### Move and Resize Sites
```
Move site 1004544 to region "us-west-2"
```

```
Resize site 1004544 volume to 100 GB
```

```
Check resize status for site 1004544
```

## Testing

Run the test script to verify everything is working:
```bash
python3 test_server.py
```

This will test all three tools and show you what to expect.

## Response Format

The server provides formatted, human-readable responses with:
- ✅ Success indicators
- ❌ Error indicators  
- 📊 Structured site information with emojis for easy reading
- Pagination information when applicable
- Total count of matching results

## Error Handling

The server handles various error scenarios:
- Missing API tokens
- Validation errors (400)
- Not found errors (404)
- Server errors (500)
- Network timeouts
- Invalid parameters

## Files in this Project

- `server.py` - Main MCP server implementation with all 5 tools
- `requirements.txt` - Python dependencies
- `setup.py` - Package configuration
- `test_server.py` - Test script to verify all functionality
- `test_auth.py` - Authentication testing script
- `q-config-example.json` - Example Q CLI configuration
- `README.md` - This documentation

## Next Steps

1. **Get your Maverick API token** from your Maverick instance
2. **Set the environment variables** with your actual token
3. **Add the MCP server configuration** to `~/.aws/amazonq/mcp.json`
4. **Restart Amazon Q CLI** and test with: `q chat`
5. **Try the example commands** to verify everything works

## Development

To extend the server with additional Maverick APIs:

1. Add new tool definitions to `handle_list_tools()`
2. Add corresponding handlers to `handle_call_tool()`
3. Implement the API call functions
4. Update this README with the new functionality

## Environment Variables

- `MAVERICK_BASE_URL`: Base URL for Maverick API (default: staging)
- `MAVERICK_API_TOKEN`: Authentication token for Maverick API (required)

**Note**: The server uses the `appian-api-key` header for authentication, which is one of the supported methods in Maverick API. Other supported methods include:
- `appian-api-key` header (used by this server)
- `Authorization: Bearer` header
- Basic Authentication with null username
- Basic Authentication with null password

## Authentication Setup

To get your API token:
1. Configure object security for a service account in your Maverick instance
2. Generate an API key for that service account
3. Set the `MAVERICK_API_TOKEN` environment variable with your key

Example:
```bash
export MAVERICK_API_TOKEN="your-actual-api-key-here"
```

## Dependencies

- `mcp>=1.10.0`: Model Context Protocol library
- `httpx>=0.25.0`: Async HTTP client
- Python 3.8+
