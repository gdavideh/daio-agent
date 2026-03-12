#!/bin/bash

# Start the MCP Server in the background
echo "Starting DrSarmiento-I MCP Server on port 8000..."
python3 mcp_server.py &

# Start the Autonomous Agent loop
echo "Starting DrSarmiento-I Autonomous Loop..."
python3 main.py
