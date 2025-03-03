#!/usr/bin/env python3
import sys
import os
from PIL import Image
from tools import filters
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Image Filters", version="1.0.0")

# Map filter names to functions
OPERATIONS = {
    "grayscale": filters.apply_grayscale,
    "sepia": filters.apply_sepia,
    "blur": filters.apply_blur,
    "sharpen": filters.apply_sharpen,
    "edge_detection": filters.apply_edge_detection,
    "invert": filters.apply_invert,
    "emboss": filters.apply_emboss,
    "contour": filters.apply_contour,
    "smooth": filters.apply_smooth,
    "solarize": filters.apply_solarize
}

# Define a function to create a filter tool for a specific operation
def create_filter_tool(op_name, op_func):
    def filter_tool(image_path: str, output_path: str = None, **kwargs):
        """Apply a filter to an image.
        
        Args:
            image_path: Path to the input image file
            output_path: Optional path to save the filtered image. If not provided, a default path will be used.
        """
        print(f"Applying {op_name} filter to {image_path}", file=sys.stderr)
        
        try:
            img = Image.open(image_path)
        except Exception as e:
            print(f"Error opening image: {e}", file=sys.stderr)
            raise ValueError(f"Error opening image: {e}")
        
        try:
            # Extract any additional parameters for the filter
            filter_params = {k: v for k, v in kwargs.items() if k not in ("image_path", "output_path")}
            result_img = op_func(img, **filter_params)
        except Exception as e:
            print(f"Error processing image: {e}", file=sys.stderr)
            raise ValueError(f"Error processing image: {e}")
        
        try:
            if output_path:
                result_img.save(output_path)
            else:
                # Create output directory if it doesn't exist
                os.makedirs("outputs", exist_ok=True)
                output_path = f"outputs/{op_name}_output.jpg"
                result_img.save(output_path)
        except Exception as e:
            print(f"Error saving image: {e}", file=sys.stderr)
            raise ValueError(f"Error saving image: {e}")
        
        return f"Filter '{op_name}' applied successfully. Image saved to {output_path}"
    
    # Set the function name and docstring
    filter_tool.__name__ = op_name
    filter_tool.__doc__ = f"Apply {op_name} filter to an image."
    
    return filter_tool

# Register all filter tools
for op_name, op_func in OPERATIONS.items():
    tool_func = create_filter_tool(op_name, op_func)
    mcp.tool(name=op_name)(tool_func)

if __name__ == "__main__":
    print("Starting Image Filter MCP Server...", file=sys.stderr)
    mcp.run(transport='stdio')
