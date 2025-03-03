from PIL import Image
import os

# Create directory for test images if it doesn't exist
os.makedirs('test_images', exist_ok=True)

# Create a simple test image (a gradient)
width, height = 300, 200
image = Image.new('RGB', (width, height))
pixels = image.load()

# Create a gradient
for x in range(width):
    for y in range(height):
        r = int(255 * x / width)
        g = int(255 * y / height)
        b = int(255 * (x + y) / (width + height))
        pixels[x, y] = (r, g, b)

# Save the image
image.save('test_images/test_gradient.jpg')
print(f"Created test image at: {os.path.abspath('test_images/test_gradient.jpg')}")
