import json
import torch

class DepthRangeTo230Manual:
    """
    Manual min/max remap in 8-bit domain (0..255) for depth maps.

    New:
    - Optional stats_json (from Olm Histogram) to auto-fill luminance min/max.

    Output will be scaled so that max maps to target_max_8bit (default 230).
    Optionally subtract min first to force black = 0.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "min_8bit": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "max_8bit": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1}),
                "target_max_8bit": ("INT", {"default": 230, "min": 1, "max": 255, "step": 1}),
                "subtract_min": ("BOOLEAN", {"default": True}),
                "clamp_to_target": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                # Connect Olm Histogram "Histogram Data (JSON)" output here
                "stats_json": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "Depth/Normalize"

    def run(self, image, min_8bit, max_8bit, target_max_8bit, subtract_min, clamp_to_target, stats_json=""):
        # Prefer stats_json if provided
        if isinstance(stats_json, str) and stats_json.strip():
            try:
                stats = json.loads(stats_json)
                lum = stats.get("luminance", {})
                min_8bit = int(lum.get("min", min_8bit))
                max_8bit = int(lum.get("max", max_8bit))
            except Exception:
                # Fall back to manual values if JSON parsing fails
                pass

        x = image  # ComfyUI IMAGE is typically float32 in 0..1
        x255 = x * 255.0  # convert to 0..255 domain

        minv = float(min_8bit)
        maxv = float(max_8bit)
        target = float(target_max_8bit)

        if subtract_min:
            denom = max(maxv - minv, 1e-6)
            y255 = (x255 - minv) * (target / denom)
        else:
            denom = max(maxv, 1e-6)
            y255 = x255 * (target / denom)

        if clamp_to_target:
            y255 = torch.clamp(y255, 0.0, target)
        else:
            y255 = torch.clamp(y255, 0.0, 255.0)

        y = y255 / 255.0  # back to 0..1 float
        return (y,)
