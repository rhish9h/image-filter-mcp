# Image Filters MCP Server

A Model Context Protocol (MCP) server that provides 10 different image filters using Python and the Pillow library. This server implements the MCP protocol over STDIO, making it suitable for integration with Claude Desktop.

## Features

- **10 Image Filters**:
  - Grayscale - Convert the image to grayscale
  - Sepia - Apply a sepia tone effect
  - Blur - Apply Gaussian blur
  - Sharpen - Enhance image details
  - Edge Detection - Highlight edges
  - Invert Colors - Invert the image colors
  - Emboss - Create an embossed look
  - Contour - Detect image contours
  - Smooth - Smooth the image
  - Solarize - Apply a solarize effect

## Project Structure

```
image_filters_mcp/           # Project root
├── server.py                # Main MCP server script (entry point)
├── tools/                   # Package for image filter functions
│   ├── __init__.py          # Makes tools a package
│   └── filters.py           # Contains all filter implementations
├── tests/                   # Contains test scripts
│   ├── test_filters.py      # Unit tests for filters
│   ├── test_server.py       # Integration tests for the server
│   └── create_test_image.py # Script to create test images
├── run_server.sh            # Script to run the server with venv
├── manual_test.py           # Script for manual testing
├── adding_new_filters.md    # Guide for adding new filters
├── claude_desktop_example.md # Guide for using with Claude Desktop
└── requirements.txt         # Python dependencies
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rhish9h/image-filter-mcp.git
   cd image-filter-mcp
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

Run the server directly:

```bash
./run_server.sh
```

Or manually:

```bash
source venv/bin/activate
python server.py
```

The server will wait for JSON-RPC input on STDIN and write responses to STDOUT.

### Example Request Format

MCP uses the JSON-RPC 2.0 protocol. Here are examples of different request types:

#### Initialization

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize"
}
```

#### List Available Tools

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

#### Call a Tool (Apply a Filter)

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "grayscale",
    "arguments": {
      "image_path": "path/to/input/image.jpg",
      "output_path": "path/to/output/image.jpg"
    }
  }
}
```

For filters with additional parameters (like blur or solarize), you can add them to the arguments object:

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "blur",
    "arguments": {
      "image_path": "path/to/input/image.jpg",
      "output_path": "path/to/output/image.jpg",
      "radius": 5.0
    }
  }
}
```

### Using the Manual Test Script

The repository includes a manual test script to easily test filters:

```bash
# Basic usage
python manual_test.py <filter_name> <input_image> <output_image> [param_name=param_value]

# Examples
python manual_test.py grayscale test_images/test_gradient.jpg output.jpg
python manual_test.py blur test_images/test_gradient.jpg output.jpg radius=5.0
python manual_test.py solarize test_images/test_gradient.jpg output.jpg threshold=100
```

### Integration with Claude Desktop

To use this MCP server with Claude Desktop, update your Claude Desktop configuration file at `~/Library/Application Support/Claude/claude_desktop_config.json` to include:

```json
{
  "mcpServers": {
    "image-filters": {
      "command": "/path/to/venv/bin/python",
      "args": [
        "/path/to/image-filter-mcp/server.py"
      ]
    }
  }
}
```

See `claude_desktop_example.md` for more detailed instructions on using the server with Claude Desktop.

## Testing

### Creating Test Images

Create a test gradient image:

```bash
python tests/create_test_image.py
```

### Running Unit Tests

Test the filter implementations:

```bash
python -m unittest tests/test_filters.py
```

### Testing the Server

Test all filters with the test server script:

```bash
python tests/test_server.py
```

## Extending the Server

This server is designed to be easily extensible. See `adding_new_filters.md` for a guide on how to add new filters to the system.

## License

MIT