import json
import os
from typing import Any

def load_json_file(path: str, default=None) -> Any:
    if default is None:
        default = []
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return default
    except Exception:
        return default

def save_json_file(path: str, data: Any):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 