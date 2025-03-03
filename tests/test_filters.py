import os
import sys
import unittest
from PIL import Image

# Add the parent directory to the path so we can import the tools package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import filters

class TestFilters(unittest.TestCase):
    """Test cases for image filters."""
    
    def setUp(self):
        """Create a test image for all tests."""
        # Create a simple test image (a red square)
        self.test_image = Image.new('RGB', (100, 100), color='red')
    
    def test_grayscale(self):
        """Test the grayscale filter."""
        result = filters.apply_grayscale(self.test_image)
        self.assertEqual(result.mode, 'RGB')
        # Check that the result is actually grayscale (R=G=B)
        r, g, b = result.getpixel((50, 50))
        self.assertEqual(r, g)
        self.assertEqual(g, b)
    
    def test_sepia(self):
        """Test the sepia filter."""
        result = filters.apply_sepia(self.test_image)
        self.assertEqual(result.mode, 'RGB')
        # Sepia should change the color values
        r, g, b = result.getpixel((50, 50))
        self.assertNotEqual(r, 255)  # Original red was 255
    
    def test_blur(self):
        """Test the blur filter."""
        result = filters.apply_blur(self.test_image, radius=2.0)
        self.assertEqual(result.mode, 'RGB')
    
    def test_sharpen(self):
        """Test the sharpen filter."""
        result = filters.apply_sharpen(self.test_image)
        self.assertEqual(result.mode, 'RGB')
    
    def test_edge_detection(self):
        """Test the edge detection filter."""
        result = filters.apply_edge_detection(self.test_image)
        self.assertEqual(result.mode, 'RGB')
    
    def test_invert(self):
        """Test the invert filter."""
        result = filters.apply_invert(self.test_image)
        self.assertEqual(result.mode, 'RGB')
        # Red (255, 0, 0) should become Cyan (0, 255, 255)
        r, g, b = result.getpixel((50, 50))
        self.assertEqual(r, 0)
        self.assertEqual(g, 255)
        self.assertEqual(b, 255)
    
    def test_emboss(self):
        """Test the emboss filter."""
        result = filters.apply_emboss(self.test_image)
        self.assertEqual(result.mode, 'RGB')
    
    def test_contour(self):
        """Test the contour filter."""
        result = filters.apply_contour(self.test_image)
        self.assertEqual(result.mode, 'RGB')
    
    def test_smooth(self):
        """Test the smooth filter."""
        result = filters.apply_smooth(self.test_image)
        self.assertEqual(result.mode, 'RGB')
    
    def test_solarize(self):
        """Test the solarize filter."""
        result = filters.apply_solarize(self.test_image, threshold=128)
        self.assertEqual(result.mode, 'RGB')
        # Red (255, 0, 0) should become (0, 0, 0) with threshold 128
        r, g, b = result.getpixel((50, 50))
        self.assertEqual(r, 0)

if __name__ == '__main__':
    unittest.main()
