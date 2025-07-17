from app.utils.field_map import CN2EN
from app.models.drug import Drug

def get_mock_drug_info(drug_name: str) -> Drug:
    mock_cn = {
        "药品名称": f"{drug_name}（商品名：安灭菌）",
        "主治功效": "细菌性上呼吸道感染、中耳炎、泌尿系统感染",
        "用法用量": "成人：每次500mg，每8小时一次口服；儿童：每日40mg/kg分3次服用",
        "禁忌症": "青霉素过敏者禁用；传染性单核细胞增多症患者禁用",
        "注意事项": "常见腹泻、皮疹；与丙磺舒联用需减量；孕妇慎用",
        "药品类别": "抗生素"
    }
    data_en = {CN2EN[k]: v for k, v in mock_cn.items() if k in CN2EN}
    return Drug(**data_en) 