# 药品字段中英文映射
CN2EN = {
    "药品名称": "name",
    "主治功效": "indications",
    "用法用量": "usage",
    "禁忌症": "contraindications",
    "注意事项": "precautions",
    "药品类别": "category",
     "剂型": "dosage_form",
    "规格": "specification"
}
EN2CN = {v: k for k, v in CN2EN.items()} 