# Image Filters MCP Server Implementation Guide

This guide explains how to build an MCP (Model Context Protocol) server that supports **10 image filters**. The server will be written in Python, use the lightweight Pillow library for image processing, and communicate via STDIO (for Claude Desktop integration). Each filter is implemented as a separate tool. Follow these steps to set up the project, implement the filters, and create the MCP server.

---

## 1. Project Structure

Organize your project with a clean, modular folder structure. Create the following directories and files:

image_filters_mcp/           # Project root
├── server.py                # Main MCP server script (entry point)
├── tools/                   # Package for image filter functions
│   ├── __init__.py          # Makes tools a package
│   └── filters.py           # Contains all filter implementations
├── tests/                   # (Optional) Contains test scripts and sample images
│   └── test_filters.py
└── BUILD_INSTRUCTIONS.md    # This instructions file

---

## 2. Dependencies

Ensure you have the following installed:
- **Python 3.x**
- **Pillow**: A lightweight image processing library.  
  Install via pip:  
  ```bash
  pip install Pillow
  ```

## 3. List of 10 Filters

Implement these filters as separate functions in tools/filters.py:
1. Grayscale – Convert the image to grayscale.
2. Sepia – Apply a sepia tone effect.
3. Blur – Apply Gaussian blur.
4. Sharpen – Enhance image details.
5. Edge Detection – Highlight edges.
6. Invert Colors – Invert the image colors.
7. Emboss – Create an embossed look.
8. Contour – Detect image contours.
9. Smooth – Smooth the image.
10. Solarize – Apply a solarize effect.

## 4. Implementing the Filters

### 4.1 Create the tools/filters.py File

Open tools/filters.py and add the following code:

```python
from PIL import Image, ImageFilter, ImageOps

def apply_grayscale(img: Image.Image) -> Image.Image:
    """Convert image to grayscale."""
    # Convert to grayscale then back to RGB (if consistency is needed)
    return img.convert("L").convert("RGB")

def apply_sepia(img: Image.Image) -> Image.Image:
    """Apply a sepia tone filter."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()  # Get pixel data
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
    return img

def apply_blur(img: Image.Image, radius: float = 2.0) -> Image.Image:
    """Blur the image using a Gaussian filter."""
    return img.filter(ImageFilter.GaussianBlur(radius))

def apply_sharpen(img: Image.Image) -> Image.Image:
    """Sharpen the image to enhance details."""
    return img.filter(ImageFilter.SHARPEN)

def apply_edge_detection(img: Image.Image) -> Image.Image:
    """Detect edges in the image."""
    return img.filter(ImageFilter.FIND_EDGES)

def apply_invert(img: Image.Image) -> Image.Image:
    """Invert the colors of the image."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    return ImageOps.invert(img)

def apply_emboss(img: Image.Image) -> Image.Image:
    """Apply an emboss filter to the image."""
    return img.filter(ImageFilter.EMBOSS)

def apply_contour(img: Image.Image) -> Image.Image:
    """Apply a contour filter to the image."""
    return img.filter(ImageFilter.CONTOUR)

def apply_smooth(img: Image.Image) -> Image.Image:
    """Smooth the image."""
    return img.filter(ImageFilter.SMOOTH)

def apply_solarize(img: Image.Image, threshold: int = 128) -> Image.Image:
    """Apply a solarize effect to the image."""
    return ImageOps.solarize(img, threshold)
```

Note: Each function accepts a Pillow Image object (and extra parameters where needed) and returns a modified image.

## 5. Implementing the MCP Server

Create the main server script in server.py that will handle STDIO-based communication.

### 5.1 Create the server.py File

In server.py, add the following code:

```python
import sys
import json
from PIL import Image
from tools import filters

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

def process_request(request: dict) -> dict:
    """Process a single MCP request and apply the specified filter."""
    req_id = request.get("id")
    tool = request.get("tool")
    params = request.get("params", {})

    if tool not in OPERATIONS:
        return {"id": req_id, "status": "error", "message": f"Unknown tool '{tool}'"}
    
    image_path = params.get("image_path")
    output_path = params.get("output_path")
    if not image_path:
        return {"id": req_id, "status": "error", "message": "Missing 'image_path'"}

    try:
        img = Image.open(image_path)
    except Exception as e:
        return {"id": req_id, "status": "error", "message": f"Error opening image: {e}"}

    try:
        # Extract any additional parameters for the filter
        filter_params = {k: v for k, v in params.items() if k not in ("image_path", "output_path")}
        result_img = OPERATIONS[tool](img, **filter_params)
    except Exception as e:
        return {"id": req_id, "status": "error", "message": f"Error processing image: {e}"}

    try:
        if output_path:
            result_img.save(output_path)
        else:
            output_path = "output.jpg"
            result_img.save(output_path)
    except Exception as e:
        return {"id": req_id, "status": "error", "message": f"Error saving image: {e}"}

    return {"id": req_id, "status": "ok", "output_path": output_path}

def main():
    """Main loop: read from STDIN, process requests, and write responses to STDOUT."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except Exception:
            error_resp = {"status": "error", "message": "Invalid JSON"}
            print(json.dumps(error_resp), flush=True)
            continue
        response = process_request(request)
        print(json.dumps(response), flush=True)

if __name__ == "__main__":
    main()
```

### 5.2 Explanation
- **OPERATIONS Dictionary**: Maps filter names (as strings) to the corresponding functions defined in tools/filters.py.
- **process_request Function**:
  - Reads the JSON request, which should include:
    - An "id" (to track requests)
    - A "tool" field specifying the filter name (e.g., "grayscale", "sepia", etc.)
    - A "params" object containing at least an "image_path" (input file) and optionally an "output_path". Additional parameters (like radius for blur or threshold for solarize) are forwarded to the filter function.
  - Opens the image, applies the filter, saves the output, and returns a JSON response.
- **Main Loop**: Continuously reads STDIN (one JSON per line) and writes a JSON response to STDOUT. This is how Claude Desktop communicates with the MCP server.

## 6. Testing & Running

### 6.1 Manual Testing
1. **Run the Server Locally**:
   - Open a terminal in the project directory.
   - Activate your virtual environment (if not already activated).
   - Start the server by running:
   ```
   python server.py
   ```
   - The server will now wait for JSON input.

2. **Send a Test Request**:
   - In another terminal, simulate a request using echo. For example, to apply the grayscale filter:
   ```
   echo '{"id": 1, "tool": "grayscale", "params": {"image_path": "test.jpg", "output_path": "test_gray.jpg"}}' | python server.py
   ```
   - Check that test_gray.jpg is created and is a grayscale version of test.jpg.

3. **Test Additional Filters**:
   - Replace "tool": "grayscale" with any of the following:
     - "sepia"
     - "blur" (you can add an extra parameter like "radius": 3)
     - "sharpen"
     - "edge_detection"
     - "invert"
     - "emboss"
     - "contour"
     - "smooth"
     - "solarize" (you can add "threshold": 128)
   - Verify that each produces the expected result.

### 6.2 Integration with Claude Desktop
1. **Configure MCP**:
   - Update your Claude Desktop configuration file (typically located in the user profile) to point to this server. An example entry might be:
   ```json
   {
       "mcpServers": {
           "image-filters-server": {
               "command": "C:\\path\\to\\image_filters_mcp\\venv\\Scripts\\python.exe",
               "args": [
                   "C:\\path\\to\\image_filters_mcp\\server.py"
               ]
           }
       }
   }
   ```
   - Ensure that the paths are correct and absolute.

2. **Launch Claude Desktop**:
   - Claude Desktop should now start your MCP server automatically.
   - Invoke image filter commands from within Claude using the expected JSON format.

## 7. Additional Notes
- **Paths**: Make sure the image paths (both input and output) are correctly specified relative to the working directory of the server or as absolute paths.
- **Error Handling**: The server responds with clear error messages for unknown tools, missing parameters, or issues during image processing. Adjust logging or error handling as needed.
- **Extensibility**: This modular design lets you add more filters easily by defining a new function in tools/filters.py and updating the OPERATIONS dictionary in server.py.

## 8. Conclusion

By following this guide, you will build an MCP server with 10 image filters using Python and Pillow. The server communicates via STDIO, making it ready for integration with Claude Desktop. This modular and well-documented approach should ensure a smooth implementation and future extensibility.

Happy coding!
