"""
ComfyUI-DepthNormalizer
A ComfyUI custom node for normalizing depth maps to a specific range.
"""

from .nodes.depth_range_manual import DepthRangeTo230Manual

NODE_CLASS_MAPPINGS = {
    "DepthRangeTo230Manual": DepthRangeTo230Manual,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DepthRangeTo230Manual": "Depth Range (Manual)",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
