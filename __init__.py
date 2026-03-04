"""
ComfyUI-DepthNormalizer
A ComfyUI custom node for normalizing depth maps to a specific range.
"""

from .nodes.depth_range_manual import DepthRangeTo190Manual

NODE_CLASS_MAPPINGS = {
    "DepthRangeTo190Manual": DepthRangeTo190Manual,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DepthRangeTo190Manual": "Depth Range → 0–190 (Manual)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
