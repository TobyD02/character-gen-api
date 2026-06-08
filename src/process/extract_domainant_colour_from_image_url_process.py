from io import BytesIO
from collections import Counter
import requests
from PIL import Image
import colorsys

class ExtractDominantColourFromImageUrlProcess:
    def __init__(self):
        self.resize = 150
        self.min_lightness = 0.15   # skip near-black
        self.max_lightness = 0.93   # skip near-white
        self.min_saturation = 0.10  # skip greys/neutrals
        self.quantize_bucket = 15   # group similar shades (larger = more aggressive)

    def _to_hsv(self, rgb):
        return colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

    def _is_neutral(self, rgb):
        """Returns True for near-black, near-white, and low-saturation greys."""
        h, s, v = self._to_hsv(rgb)
        return (
            v < self.min_lightness or      # near-black
            v > self.max_lightness or      # near-white
            s < self.min_saturation        # grey / unsaturated
        )

    def _quantize(self, rgb):
        b = self.quantize_bucket
        return tuple((c // b) * b for c in rgb)

    def execute(self, image_url: str) -> dict:
        response = requests.get(image_url)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        img = img.resize((self.resize, self.resize))

        pixels = list(img.getdata())

        filtered = [
            self._quantize(p) for p in pixels
            if not self._is_neutral(p)
        ]

        if not filtered:
            return {
                "primary": "#ffffff",
                "secondary": None,
                "tertiary": None,
                "note": "No non-neutral colours found"
            }

        counts = Counter(filtered)
        top = counts.most_common(10)  # grab top 10 buckets, then pick 3 distinct ones

        palette = []
        for color, count in top:
            # Skip if too visually similar to an already-chosen colour
            if not any(self._too_similar(color, chosen) for chosen in palette):
                palette.append(color)
            if len(palette) == 3:
                break

        hex_palette = ["#{:02x}{:02x}{:02x}".format(*c) for c in palette]

        return {
            "primary":   hex_palette[0] if len(hex_palette) > 0 else None,
            "secondary": hex_palette[1] if len(hex_palette) > 1 else None,
            "tertiary":  hex_palette[2] if len(hex_palette) > 2 else None,
        }

    def _too_similar(self, c1, c2, threshold=40):
        """Euclidean RGB distance — skip if colours are too close to each other."""
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5 < threshold
