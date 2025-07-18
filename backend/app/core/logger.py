from loguru import logger
import sys
from pathlib import Path

# 日志目录
LOG_DIR = Path(__file__).resolve().parent.parent.parent / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 移除默认处理器
logger.remove()

# 控制台输出格式
console_format = "<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>[{level}]</level> <cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>"

# 文件输出格式
file_format = "[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {name}:{function}:{line} - {message}"

# 控制台输出
logger.add(sys.stdout, level="INFO", format=console_format, enqueue=True)

# 文件输出（INFO 及以上）
logger.add(str(LOG_DIR / "info.log"), level="INFO", format=file_format, rotation="10 MB", retention="10 days", encoding="utf-8", enqueue=True)
logger.add(str(LOG_DIR / "warning.log"), level="WARNING", format=file_format, rotation="5 MB", retention="15 days", encoding="utf-8", enqueue=True)
logger.add(str(LOG_DIR / "error.log"), level="ERROR", format=file_format, rotation="1 MB", retention="30 days", encoding="utf-8", enqueue=True) 