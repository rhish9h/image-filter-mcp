#!/usr/bin/env python3
"""
Manual test script for the image filters MCP server.
This script allows you to test the server by sending a request for a specific filter.

Usage:
    python manual_test.py <filter_name> <input_image> <output_image> [param_name=param_value]

Example:
    python manual_test.py blur test_images/test_gradient.jpg output.jpg radius=5.0
    python manual_test.py solarize test_images/test_gradient.jpg output.jpg threshold=100
"""

import json
import sys
import subprocess
import os

def main():
    if len(sys.argv) < 4:
        print("Usage: python manual_test.py <filter_name> <input_image> <output_image> [param_name=param_value]")
        sys.exit(1)
    
    filter_name = sys.argv[1]
    input_image = os.path.abspath(sys.argv[2])
    output_image = os.path.abspath(sys.argv[3])
    
    # Parse additional parameters
    arguments = {
        "image_path": input_image,
        "output_path": output_image
    }
    
    for arg in sys.argv[4:]:
        if '=' in arg:
            name, value = arg.split('=', 1)
            # Try to convert value to number if possible
            try:
                if '.' in value:
                    arguments[name] = float(value)
                else:
                    arguments[name] = int(value)
            except ValueError:
                arguments[name] = value
    
    # Create JSON-RPC request for initialization
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize"
    }
    
    # Create JSON-RPC request for the tool execution
    tool_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": filter_name,
            "arguments": arguments
        }
    }
    
    # Start the server process
    server_process = subprocess.Popen(
        ['python', 'server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Send initialization request
    print(f"Sending initialization request: {json.dumps(init_request, indent=2)}")
    init_json = json.dumps(init_request) + '\n'
    server_process.stdin.write(init_json)
    server_process.stdin.flush()
    
    # Read initialization response
    init_response_json = server_process.stdout.readline().strip()
    try:
        init_response = json.loads(init_response_json)
        print(f"Initialization Response: {json.dumps(init_response, indent=2)}")
    except json.JSONDecodeError:
        print(f"Error decoding initialization response: {init_response_json}")
    
    # Send tool request
    print(f"\nSending tool request: {json.dumps(tool_request, indent=2)}")
    tool_json = json.dumps(tool_request) + '\n'
    server_process.stdin.write(tool_json)
    server_process.stdin.flush()
    
    # Read tool response
    tool_response_json = server_process.stdout.readline().strip()
    try:
        tool_response = json.loads(tool_response_json)
        print(f"Tool Response: {json.dumps(tool_response, indent=2)}")
        
        # Check if operation was successful
        if "error" not in tool_response:
            output_path = arguments.get('output_path')
            if output_path and os.path.exists(output_path):
                print(f"Output file created: {output_path}")
            else:
                print(f"Warning: Output file not found at {output_path}")
        else:
            print(f"Error: {tool_response['error']['message']}")
    except json.JSONDecodeError:
        print(f"Error decoding tool response: {tool_response_json}")
    
    # Terminate the server
    server_process.terminate()
    server_process.wait()

if __name__ == "__main__":
    main()
