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
