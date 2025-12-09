import os
import shutil
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.core.config import CHROMA_PERSIST_DIR

CHROMA_DIR = Path(CHROMA_PERSIST_DIR)

def clear_chromadb_dir():
    if CHROMA_DIR.exists() and CHROMA_DIR.is_dir():
        for item in CHROMA_DIR.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        print(f"已彻底清空目录: {CHROMA_DIR}")
        return True
    else:
        print(f"目录不存在: {CHROMA_DIR}")
        return False

if __name__ == "__main__":
    # 支持命令行参数 --yes 或 -y 跳过确认
    force = len(sys.argv) > 1 and (sys.argv[1] == '--yes' or sys.argv[1] == '-y')
    
    if force:
        print(f"正在清空目录 '{CHROMA_DIR}' 下的所有数据...")
        clear_chromadb_dir()
    else:
        try:
            confirm = input(f"确定要彻底清空目录 '{CHROMA_DIR}' 下的所有数据吗？(y/n): ").strip().lower()
            if confirm == 'y':
                clear_chromadb_dir()
            else:
                print("操作已取消")
        except (EOFError, KeyboardInterrupt):
            print("\n操作已取消（使用 --yes 或 -y 参数可跳过确认）")