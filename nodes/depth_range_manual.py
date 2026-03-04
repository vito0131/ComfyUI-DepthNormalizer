import torch


class DepthRangeTo190Manual:
    """
    Manual min/max remap in 8-bit domain (0..255) for depth maps.
    Output will be scaled so that max maps to target_max_8bit (default 190).
    Optionally subtract min first to force black = 0.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "min_8bit": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "max_8bit": ("INT", {"default": 190, "min": 0, "max": 255, "step": 1}),
                "target_max_8bit": ("INT", {"default": 190, "min": 1, "max": 255, "step": 1}),
                "subtract_min": ("BOOLEAN", {"default": True}),
                "clamp_to_target": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "run"
    CATEGORY = "Depth/Normalize"

    def run(self, image, min_8bit, max_8bit, target_max_8bit, subtract_min, clamp_to_target):
        x = image  # ComfyUI IMAGE is typically float32 in 0..1

        # Convert 0..1 float image to 0..255 domain
        x255 = x * 255.0

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

        # Back to 0..1 float for ComfyUI
        y = y255 / 255.0
        return (y,)
