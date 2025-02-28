import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LongTextSplitterNode:
    def __init__(self):
        self.state_file = os.path.join(os.path.dirname(__file__), "text_splitter_state.json")
        self.state = self.load_state()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "separator": ("STRING", {"default": "---"}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 10000})
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("prompt", "status", "current_index")
    FUNCTION = "process_text"
    CATEGORY = "LongTextSplit"

    def process_text(self, text, separator, start_index):
        try:
            if not text.strip():
                return ("", "Error: Input text is empty", -1)

            text_changed = self.state.get("last_text") != text
            separator_changed = self.state.get("last_separator") != separator
            index_changed = self.state.get("last_start_index") != start_index

            if text_changed or separator_changed:
                self.load_prompts(text, separator)
                self.state["last_text"] = text
                self.state["last_separator"] = separator
                self.state["current_index"] = start_index
            elif index_changed:
                self.state["current_index"] = start_index
            else:
                self.state["current_index"] = (self.state.get("current_index", 0) + 1) % len(self.state["prompts"])

            self.state["last_start_index"] = start_index
            current_index = self.state["current_index"]

            prompt = self.state["prompts"][current_index] if self.state["prompts"] else ""
            status = f"Prompt {current_index + 1}/{len(self.state['prompts'])}"
            
            self.save_state()
            return (prompt, status, current_index)
            
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            return ("", f"Error: {str(e)}", -1)

    def load_prompts(self, text, separator):
        try:
            self.state["prompts"] = [p.strip() for p in text.split(separator) if p.strip()]
            logger.info(f"Split text into {len(self.state['prompts'])} prompts")
        except Exception as e:
            logger.error(f"Prompt loading failed: {str(e)}")
            raise

    def load_state(self):
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"State load failed: {str(e)}")
        return {
            "prompts": [],
            "current_index": 0,
            "last_text": "",
            "last_separator": "",
            "last_start_index": 0
        }

    def save_state(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f)
        except Exception as e:
            logger.error(f"State save failed: {str(e)}")

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

NODE_CLASS_MAPPINGS = {
    "LongTextSplitter": LongTextSplitterNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LongTextSplitter": "Long Text Splitter (CR)"
}