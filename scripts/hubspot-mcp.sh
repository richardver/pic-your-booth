#!/bin/bash
# Load .env from project root and start HubSpot MCP server
DIR="$(cd "$(dirname "$0")/.." && pwd)"
set -a
source "$DIR/.env" 2>/dev/null
set +a
export PRIVATE_APP_ACCESS_TOKEN="$HUBSPOT_ACCESS_TOKEN"
exec npx -y @hubspot/mcp-server
