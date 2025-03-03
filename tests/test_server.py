import json
import os
import subprocess
import time
from pathlib import Path

# Ensure output directory exists
os.makedirs('test_outputs', exist_ok=True)

# Path to test image
test_image = os.path.abspath('test_images/test_gradient.jpg')

# Define test requests for each filter
test_requests = [
    # Initialize request
    {
        "jsonrpc": "2.0",
        "id": 100,
        "method": "initialize"
    },
    # List tools
    {
        "jsonrpc": "2.0",
        "id": 101,
        "method": "tools/list"
    },
    # Filter operations
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "grayscale",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/grayscale.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "sepia",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/sepia.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "blur",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/blur.jpg",
                "radius": 5.0
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "sharpen",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/sharpen.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "edge_detection",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/edge_detection.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/call",
        "params": {
            "name": "invert",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/invert.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "tools/call",
        "params": {
            "name": "emboss",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/emboss.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 8,
        "method": "tools/call",
        "params": {
            "name": "contour",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/contour.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 9,
        "method": "tools/call",
        "params": {
            "name": "smooth",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/smooth.jpg"
            }
        }
    },
    {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "tools/call",
        "params": {
            "name": "solarize",
            "arguments": {
                "image_path": test_image,
                "output_path": "test_outputs/solarize.jpg",
                "threshold": 128
            }
        }
    }
]

def test_server_with_subprocess():
    """Test the server by running it as a subprocess and sending requests."""
    # Start the server process
    server_process = subprocess.Popen(
        ['python', 'server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    print("Server started. Sending test requests...")
    
    # Send each request and collect responses
    for request in test_requests:
        # Send request to server
        request_json = json.dumps(request) + '\n'
        server_process.stdin.write(request_json)
        server_process.stdin.flush()
        
        # Read response
        response_json = server_process.stdout.readline().strip()
        try:
            response = json.loads(response_json)
            
            if request["method"] == "initialize":
                print(f"Initialization Response: {response}")
            elif request["method"] == "tools/list":
                print(f"Tools List Response: {response}")
            elif request["method"] == "tools/call":
                filter_name = request["params"]["name"]
                print(f"Filter: {filter_name}, Response: {response}")
                
                # Check if operation was successful (no error in response)
                if "error" not in response:
                    output_path = request["params"]["arguments"].get("output_path")
                    if output_path and os.path.exists(output_path):
                        print(f"  Output file created: {output_path}")
                    else:
                        print(f"  Warning: Output file not found at {output_path}")
                else:
                    print(f"  Error: {response['error']}")
        except json.JSONDecodeError:
            print(f"Error decoding response: {response_json}")
    
    # Terminate the server
    server_process.terminate()
    server_process.wait()
    print("Server terminated.")

if __name__ == "__main__":
    # Check if test image exists
    if not os.path.exists(test_image):
        print(f"Test image not found at {test_image}. Please run create_test_image.py first.")
        exit(1)
    
    test_server_with_subprocess()
    
    # Print summary of created files
    print("\nCreated output files:")
    for file in Path('test_outputs').glob('*.jpg'):
        print(f"- {file}")
