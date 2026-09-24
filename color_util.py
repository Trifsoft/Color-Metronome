import requests
from io import BytesIO
from PIL import Image


def get_two_colors(image_url, distinct_threshold=60):
    """
    Fetch an image from a URL and return two representative RGB colors.

    The first is the most dominant color in the image. The second is the
    next most common color that's visually distinct from the first (useful
    for gradients, e.g. a pulsing effect that shifts between two tones
    instead of one flat color).

    Args:
        image_url: URL of the image (e.g. Spotify album art).
        distinct_threshold: minimum Euclidean distance in RGB space for the
            second color to count as "distinct" from the first. Raise this
            if you want more contrast between the two colors.

    Returns:
        (primary, secondary): two (R, G, B) tuples, each 0-255.
    """
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content)).convert("RGB")

    # Downscale for speed, then reduce to a small palette
    img = img.resize((150, 150))
    palette_img = img.quantize(colors=8, method=Image.MEDIANCUT)
    palette = palette_img.getpalette()
    color_counts = sorted(palette_img.getcolors(), reverse=True, key=lambda c: c[0])

    def rgb_at(idx):
        return tuple(palette[idx * 3: idx * 3 + 3])

    def distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

    primary = rgb_at(color_counts[0][1])
    secondary = primary
    for _, idx in color_counts[1:]:
        candidate = rgb_at(idx)
        if distance(primary, candidate) > distinct_threshold:
            secondary = candidate
            break

    return primary, secondary


def to_hex_color(rgb_color: tuple) -> str:
    return "#%02x%02x%02x" % rgb_color


def get_mixed_color(color1, color2, first_color_percentage):
    first_color_percentage = max(0.0, min(1.0, first_color_percentage))
    second_color_percentage = 1.0 - first_color_percentage

    return tuple(
        int(color1[i] * first_color_percentage + color2[i] * second_color_percentage)
        for i in range(3)
    )