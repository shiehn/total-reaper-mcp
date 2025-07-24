#!/bin/bash

# REAPER MCP Server Startup Script
# This script handles all necessary setup to start the MCP server without relay

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo -e "${GREEN}Starting REAPER MCP Server Setup...${NC}"
echo "Working directory: $SCRIPT_DIR"
echo ""

# Check if we have a suitable Python version
check_python_version() {
    local python_cmd=$1
    local version=$($python_cmd -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    local major=$(echo $version | cut -d. -f1)
    local minor=$(echo $version | cut -d. -f2)
    
    if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
        return 0
    else
        return 1
    fi
}

# Find suitable Python command
PYTHON_CMD=""
if command -v python3.10 &> /dev/null && check_python_version python3.10; then
    PYTHON_CMD="python3.10"
elif command -v python3.11 &> /dev/null && check_python_version python3.11; then
    PYTHON_CMD="python3.11"
elif command -v python3.12 &> /dev/null && check_python_version python3.12; then
    PYTHON_CMD="python3.12"
elif command -v python3 &> /dev/null && check_python_version python3; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null && check_python_version python; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python 3.10 or higher is required but not found.${NC}"
    echo "Please install Python 3.10+ and try again."
    exit 1
fi

echo -e "${GREEN}✓ Found suitable Python:${NC} $PYTHON_CMD ($(${PYTHON_CMD} --version))"

# Check for virtual environment
VENV_DIR=".venv"
VENV_ACTIVATE="${VENV_DIR}/bin/activate"

# Check if venv exists and has correct Python version
if [ -d "$VENV_DIR" ]; then
    # Check Python version in existing venv
    if [ -f "${VENV_DIR}/bin/python" ]; then
        if check_python_version "${VENV_DIR}/bin/python"; then
            echo -e "${GREEN}✓ Found existing virtual environment with suitable Python version${NC}"
        else
            echo -e "${YELLOW}⚠ Existing virtual environment has incompatible Python version${NC}"
            echo "Creating new virtual environment..."
            rm -rf "$VENV_DIR"
            $PYTHON_CMD -m venv "$VENV_DIR"
        fi
    else
        echo -e "${YELLOW}⚠ Virtual environment appears corrupted${NC}"
        echo "Creating new virtual environment..."
        rm -rf "$VENV_DIR"
        $PYTHON_CMD -m venv "$VENV_DIR"
    fi
else
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_ACTIVATE"

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python -c "import mcp" 2>/dev/null; then
    echo -e "${YELLOW}⚠ MCP package not found. Installing dependencies...${NC}"
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install dependencies
    pip install "mcp>=1.1.2" "uvicorn[standard]>=0.32.1" "websockets>=12.0"
    
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Dependencies already installed${NC}"
fi

# Check if mcp_bridge_file_v2.lua is running in REAPER
BRIDGE_DIR="$HOME/Library/Application Support/REAPER/Scripts/mcp_bridge_data"
echo ""
echo -e "${YELLOW}Important: Make sure mcp_bridge_file_v2.lua is running in REAPER!${NC}"
echo "Bridge directory: $BRIDGE_DIR"
echo ""

# Clear any relay environment variables to ensure we don't use relay
unset MCP_RELAY_URL
unset MCP_AUTH_TOKEN

# Start the server
echo -e "${GREEN}Starting MCP Server (without relay)...${NC}"
echo "=" | sed 's/.*/========================================/'
echo ""

# Run the server
python -m server.app