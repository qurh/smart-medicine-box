from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import drug
from app.core.logger import logger
from app.schemas.base_response import BaseResponse
import os
import argparse
from contextlib import asynccontextmanager

# 默认值
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

# 命令行参数解析
parser = argparse.ArgumentParser()
parser.add_argument("--env", type=str, default=None, help="环境变量文件名，如 .env 或 .env.prod")
parser.add_argument("--host", type=str, default=None, help="服务主机地址")
parser.add_argument("--port", type=int, default=None, help="服务端口")
args, _ = parser.parse_known_args()

# 加载环境变量文件
if args.env:
    from dotenv import load_dotenv
    load_dotenv(args.env)

host = args.host or os.getenv("HOST") or DEFAULT_HOST
port = args.port or int(os.getenv("PORT") or DEFAULT_PORT)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("家庭智能药箱 API 启动完成！")
    logger.info(f"后端接口文档: http://{host}:{port}/docs")
    logger.info(f"后端根路由: http://{host}:{port}/")
    yield
    logger.info("家庭智能药箱 API 正在关闭...")

app = FastAPI(title="家庭智能药箱 API", lifespan=lifespan)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content=BaseResponse(code=exc.status_code, msg=exc.detail, data=None).model_dump())

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"ValidationError: {exc.errors()}")
    return JSONResponse(status_code=422, content=BaseResponse(code=422, msg="参数校验失败", data=exc.errors()).model_dump())

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}")
    return JSONResponse(status_code=500, content=BaseResponse(code=500, msg="服务器内部错误", data=None).model_dump())

# 路由注册
app.include_router(drug.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        factory=False
    )