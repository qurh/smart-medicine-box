import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from sentence_transformers import SentenceTransformer

if __name__ == "__main__":
    model_path = r"D:\projects\models\paraphrase-multilingual-MiniLM-L12-v2"
    print(f"加载本地模型: {model_path}")
    try:
        model = SentenceTransformer(model_path)
        test_text = "感冒发烧咳嗽"
        print(f"测试文本: {test_text}")
        embedding = model.encode(test_text).tolist()
        print(f"embedding 长度: {len(embedding)}")
        print(f"embedding 前10维: {embedding[:10]}")
        print("本地 paraphrase-multilingual-MiniLM-L12-v2 embedding 测试成功！")
    except Exception as e:
        print(f"embedding 测试失败: {e}")
        sys.exit(1) 