from app.core.config import MEDICINE_BOX_FILE
from app.utils.file_io import load_json_file, save_json_file
from app.models.drug import Drug

def save_drug_to_box(drug: Drug):
    box = load_json_file(MEDICINE_BOX_FILE, default=[])
    if not any(item.get('name') == drug.name for item in box):
        box.insert(0, drug.model_dump())  # 新药品插入到头部
        save_json_file(MEDICINE_BOX_FILE, box)
    return True

def get_medicine_box_list():
    return load_json_file(MEDICINE_BOX_FILE, default=[])