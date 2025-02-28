
from .LongTextSplit import LongTextSplitterNode

NODE_CLASS_MAPPINGS = { "LongTextSplitter": LongTextSplitterNode }

NODE_DISPLAY_NAME_MAPPINGS = { "LongTextSplitter": "Long Text Splitter"}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']