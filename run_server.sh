#!/bin/bash
# Script to run the MCP server with the virtual environment

# Activate the virtual environment
source "$(dirname "$0")/venv/bin/activate"

# Run the server
python "$(dirname "$0")/server.py"

# Note: This script will start the server and wait for input on STDIN
# To test, you can pipe JSON-RPC requests to it, for example:
# echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "grayscale", "arguments": {"image_path": "test_images/test_gradient.jpg", "output_path": "output.jpg"}}}' | ./run_server.sh
