"""Color analysis utilities for background images"""

from PIL import Image
import base64
from io import BytesIO
from collections import Counter


def analyze_background_colors(image_path: str, num_colors: int = 5):
    """Analyze dominant colors in an image

    Args:
        image_path: Path to image file
        num_colors: Number of dominant colors to extract

    Returns:
        List of (color_hex, percentage) tuples
    """
    # Open and resize image for faster processing
    img = Image.open(image_path)
    img = img.resize((150, 150))  # Small size for speed
    img = img.convert('RGB')

    # Get all pixels
    pixels = list(img.getdata())

    # Count color frequencies
    color_count = Counter(pixels)
    most_common = color_count.most_common(num_colors)

    total_pixels = len(pixels)

    # Convert to hex and percentages
    results = []
    for color, count in most_common:
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        percentage = (count / total_pixels) * 100
        results.append((hex_color, percentage, color))

    return results


def get_complementary_color(rgb_tuple, desaturation=0.3):
    """Get a muted version of the dominant color

    Args:
        rgb_tuple: (r, g, b) tuple
        desaturation: 0-1, how much to desaturate (0=original, 1=gray)

    Returns:
        Hex color string
    """
    r, g, b = rgb_tuple

    # Calculate grayscale value
    gray = int(0.299 * r + 0.587 * g + 0.114 * b)

    # Desaturate moderately (blend with gray)
    r_desat = int(r * (1 - desaturation) + gray * desaturation)
    g_desat = int(g * (1 - desaturation) + gray * desaturation)
    b_desat = int(b * (1 - desaturation) + gray * desaturation)

    # Scale up to maintain visibility (multiply by 3-4x instead of darkening)
    # This keeps the hue but makes it less saturated and more visible
    r_final = min(255, int(r_desat * 3.5))
    g_final = min(255, int(g_desat * 3.5))
    b_final = min(255, int(b_desat * 3.5))

    return '#{:02x}{:02x}{:02x}'.format(r_final, g_final, b_final)


def suggest_left_background_color(image_path: str):
    """Suggest a background color for the left side based on the image

    Args:
        image_path: Path to the background image

    Returns:
        Hex color string
    """
    colors = analyze_background_colors(image_path, num_colors=3)

    print(f"\n🎨 Analyzing background colors for: {image_path}")
    print(f"   Top 3 dominant colors:")
    for i, (hex_color, percentage, rgb) in enumerate(colors, 1):
        print(f"   {i}. {hex_color} ({percentage:.1f}%) - RGB{rgb}")

    # Get the most dominant color
    dominant_hex, dominant_pct, dominant_rgb = colors[0]

    # Get complementary dark color
    suggested = get_complementary_color(dominant_rgb)

    print(f"\n   ✅ Suggested left background: {suggested}")

    return suggested


if __name__ == "__main__":
    # Test with bg15.png
    import sys

    if len(sys.argv) > 1:
        bg_path = sys.argv[1]
    else:
        bg_path = "background/bg15.png"

    suggested_color = suggest_left_background_color(bg_path)
    print(f"\nUse this color in your template: {suggested_color}")
