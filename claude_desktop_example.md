# Using Image Filters MCP with Claude Desktop

This guide explains how to set up and use the Image Filters MCP server with Claude Desktop.

## Setup

1. **Configure Claude Desktop**

   Add the following configuration to your Claude Desktop configuration file located at `~/Library/Application Support/Claude/claude_desktop_config.json`:

   ```json
   {
     "mcpServers": {
       "image-filters": {
         "command": "/path/to/python",
         "args": [
           "/path/to/image-filter-mcp/server.py"
         ]
       }
     }
   }
   ```

   Replace `/path/to/python` with the path to your Python executable (preferably from your virtual environment) and `/path/to/image-filter-mcp/server.py` with the absolute path to the server.py file.

2. **Restart Claude Desktop**

   After updating the configuration, restart Claude Desktop to apply the changes.

## Using Image Filters in Claude

Once configured, you can use the image filters in Claude Desktop. Claude will automatically discover the available tools from the MCP server. You can simply ask Claude to apply a filter to an image, and it will use the appropriate MCP tool.

Example prompts:

- "Can you apply a sepia filter to my image at `/path/to/image.jpg` and save it to `/path/to/output.jpg`?"
- "Use the blur filter on this image at `/path/to/photo.jpg` with a radius of 5."
- "Convert my image at `/Users/username/Pictures/vacation.jpg` to grayscale."

Claude will automatically invoke the appropriate image filter tool with the correct parameters.

## Advanced Usage: Manual Tool Invocation

If you prefer to manually specify the tool parameters, you can use the following JSON-RPC format:

```
Can you apply a sepia filter to this image? Use the image-filters MCP server with this JSON-RPC request:

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "sepia",
    "arguments": {
      "image_path": "/path/to/your/image.jpg",
      "output_path": "/path/to/desired/output.jpg"
    }
  }
}
```

Replace:
- `sepia` with any of the available filters: `grayscale`, `blur`, `sharpen`, `edge_detection`, `invert`, `emboss`, `contour`, `smooth`, or `solarize`
- `/path/to/your/image.jpg` with the path to your input image
- `/path/to/desired/output.jpg` with where you want to save the filtered image

## Example Requests

Here are some example requests for different filters:

### Grayscale

```
Apply a grayscale filter to my image using the image-filters MCP:

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "grayscale",
    "arguments": {
      "image_path": "/path/to/image.jpg",
      "output_path": "/path/to/grayscale_output.jpg"
    }
  }
}
```

### Blur with Custom Radius

```
Blur my image with a radius of 10 using the image-filters MCP:

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "blur",
    "arguments": {
      "image_path": "/path/to/image.jpg",
      "output_path": "/path/to/blur_output.jpg",
      "radius": 10.0
    }
  }
}
```

### Solarize with Custom Threshold

```
Apply a solarize effect with threshold 100 using the image-filters MCP:

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "solarize",
    "arguments": {
      "image_path": "/path/to/image.jpg",
      "output_path": "/path/to/solarize_output.jpg",
      "threshold": 100
    }
  }
}
```

## Troubleshooting

If you encounter issues:

1. **Check paths**: Ensure all file paths are absolute and accessible to Claude Desktop
2. **Check permissions**: Make sure Claude Desktop has permission to read/write the specified files
3. **Verify Python environment**: Ensure the Python environment has the Pillow library installed
4. **Check logs**: Look at Claude Desktop logs for any error messages related to the MCP server
5. **Test the server**: Run the manual test script to verify that the server is working correctly
