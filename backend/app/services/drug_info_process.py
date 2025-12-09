import os
from app.prompts.drug_info_extract import DRUG_INFO_EXTRACT_PROMPT
from app.models.drug import Drug
from app.core.config import QWEN3_API_KEY
from app.utils.field_map import CN2EN
from app.services.mock_service import get_mock_drug_info
from loguru import logger
import json
import dashscope
from http import HTTPStatus

def enrich_drug_info_llm(drug_name: str) -> Drug:
    # 确保 API Key 已设置
    if not QWEN3_API_KEY:
        raise ValueError("QWEN3_API_KEY 未配置，请在 .env 文件中设置")
    
    dashscope.api_key = QWEN3_API_KEY
    # 设置 API 基础 URL（可选，使用默认值也可以）
    # dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    
    logger.info(f"使用 Qwen3 API 查询药品: {drug_name}")
    
    prompt = DRUG_INFO_EXTRACT_PROMPT.format(drug_name=drug_name)
    
    # 1. 直接调用 dashscope API（使用正确的 messages 格式）
    try:
        from dashscope import Generation
        
        # 构建 messages 格式
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        logger.debug(f"调用 Qwen3 API，模型: qwen-plus")
        resp = Generation.call(
            api_key=QWEN3_API_KEY,
            model="qwen-plus",
            messages=messages,
            result_format="message",
            temperature=0.7
        )
        logger.debug(f"Qwen3 API 响应状态码: {resp.status_code}")
        
        if resp.status_code != HTTPStatus.OK:
            error_msg = f"API 调用失败: status_code={resp.status_code}"
            if hasattr(resp, 'code'):
                error_msg += f", 错误码: {resp.code}"
            if hasattr(resp, 'message'):
                error_msg += f", 错误信息: {resp.message}"
            logger.error(f"Qwen3 API 调用失败: {error_msg}")
            
            # 处理配额用完的情况（403）
            if resp.status_code == 403:
                if hasattr(resp, 'message') and ("free tier" in resp.message.lower() or "exhausted" in resp.message.lower()):
                    logger.warning("Qwen3 API 免费额度已用完，建议切换到 Mock 模式或充值后使用")
                    raise ValueError(
                        "Qwen3 API 免费额度已用完。解决方案：\n"
                        "1. 在管理控制台关闭 '仅使用免费额度' 模式并充值\n"
                        "2. 或在 .env 中设置 USE_MOCK_DATA=true 使用 Mock 模式"
                    )
            
            # 处理其他错误
            raise ValueError(f"调用大模型服务失败: {error_msg}")
        
        # 提取响应内容（使用正确的响应结构）
        if not resp.output or not hasattr(resp.output, 'choices') or not resp.output.choices:
            logger.error(f"API 返回格式异常，响应内容: {resp}")
            raise ValueError("API 返回格式异常，未找到输出内容")
        
        result = resp.output.choices[0].message.content
        
    except ValueError as e:
        # 重新抛出 ValueError
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"调用 Qwen3 API 失败: {error_msg}")
        raise ValueError(f"调用大模型服务失败，请检查 API Key 配置和网络连接。错误详情: {error_msg}")
    
    # 2. 解析模型输出
    try:
        # 清理可能的 markdown 代码块标记
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()
        
        data_cn = json.loads(result)
    except json.JSONDecodeError as e:
        logger.error(f"模型输出解析失败: {e}, 原始输出: {result}")
        raise ValueError(f"模型输出格式错误，无法解析为 JSON。原始输出: {result}")
    except Exception as e:
        logger.error(f"解析模型输出时发生错误: {e}, 原始输出: {result}")
        raise ValueError(f"解析模型输出失败: {e}, 原始输出: {result}")
    
    # 3. 中文键转英文键
    data_en = {CN2EN[k]: v for k, v in data_cn.items() if k in CN2EN}
    
    # 4. 返回 Drug 实例
    return Drug(**data_en)

def enrich_drug_info_mock(drug_name: str) -> Drug:
    return get_mock_drug_info(drug_name)