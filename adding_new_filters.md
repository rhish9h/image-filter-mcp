# Adding New Filters to the MCP Server

This guide explains how to add new image filters to the existing MCP server.

## Step 1: Add a New Filter Function

First, add your new filter function to `tools/filters.py`. Follow the pattern of the existing functions:

```python
def apply_new_filter(img: Image.Image, param1: type = default_value) -> Image.Image:
    """Description of what the filter does."""
    # Your image processing code here
    return processed_img
```

For example, let's add a "posterize" filter that reduces the number of colors:

```python
def apply_posterize(img: Image.Image, bits: int = 2) -> Image.Image:
    """Apply a posterize effect to reduce the number of colors."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    return ImageOps.posterize(img, bits)
```

## Step 2: Register the Filter in the Server

Open `server.py` and add your new filter to the `OPERATIONS` dictionary:

```python
OPERATIONS = {
    # Existing filters...
    "grayscale": filters.apply_grayscale,
    "sepia": filters.apply_sepia,
    # ... other filters ...
    
    # Add your new filter here
    "posterize": filters.apply_posterize
}
```

Also, your new filter will be automatically included in the MCP tools listing when clients request the available tools.

## Step 3: Test Your New Filter

You can test your new filter using the `manual_test.py` script:

```bash
python manual_test.py posterize test_images/test_gradient.jpg test_outputs/posterize.jpg bits=3
```

Or test it with direct JSON-RPC calls:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "posterize", "arguments": {"image_path": "test_images/test_gradient.jpg", "output_path": "test_outputs/posterize.jpg", "bits": 3}}}' | python server.py
```

## Step 4: Add Unit Tests (Optional but Recommended)

Add a test for your new filter in `tests/test_filters.py`:

```python
def test_posterize(self):
    """Test the posterize filter."""
    result = filters.apply_posterize(self.test_image, bits=2)
    self.assertEqual(result.mode, 'RGB')
    # Add any specific assertions for your filter
```

And update the test requests in `tests/test_server.py` to include your new filter:

```python
{
    "jsonrpc": "2.0",
    "id": 11,  # Use a new unique ID
    "method": "tools/call",
    "params": {
        "name": "posterize",
        "arguments": {
            "image_path": test_image,
            "output_path": "test_outputs/posterize.jpg",
            "bits": 2
        }
    }
}
```

## Example: Adding a "Pixelate" Filter

Here's a complete example of adding a pixelate filter:

1. Add to `tools/filters.py`:

```python
def apply_pixelate(img: Image.Image, pixel_size: int = 10) -> Image.Image:
    """Pixelate the image by reducing and then enlarging."""
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # Get original dimensions
    width, height = img.size
    
    # Reduce image to create pixelation effect
    small_img = img.resize((width // pixel_size, height // pixel_size), 
                           resample=Image.NEAREST)
    
    # Scale back up to original size
    result = small_img.resize((width, height), resample=Image.NEAREST)
    
    return result
```

2. Add to `OPERATIONS` in `server.py`:

```python
OPERATIONS = {
    # Existing filters...
    "pixelate": filters.apply_pixelate
}
```

3. Test with:

```bash
python manual_test.py pixelate test_images/test_gradient.jpg test_outputs/pixelate.jpg pixel_size=20
```

4. Test with direct JSON-RPC:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "pixelate", "arguments": {"image_path": "test_images/test_gradient.jpg", "output_path": "test_outputs/pixelate.jpg", "pixel_size": 20}}}' | python server.py
```

## Tips for Creating New Filters

1. **Parameter Types**: Make sure to specify the correct parameter types and default values
2. **Documentation**: Add a clear docstring explaining what the filter does
3. **Error Handling**: Handle potential errors gracefully
4. **Image Mode**: Check and convert the image mode if needed (most filters work best with RGB)
5. **Performance**: For complex filters, consider performance implications for large images
6. **MCP Tools Schema**: The input arguments will be automatically included in the JSON Schema for your tool in the MCP tools list
