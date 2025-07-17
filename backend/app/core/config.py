import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
QWEN3_API_KEY = os.getenv("QWEN3_API_KEY", "")
MEDICINE_BOX_FILE = os.path.join(BASE_DIR, "medicine_box.json")