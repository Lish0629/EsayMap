# llm/processor.py
import os
import dashscope
from dashscope import Application
from http import HTTPStatus
import json
import logging
from typing import Dict, Any, Optional,List 
from schemas.responses import LLMOutput
import config

# 配置 DashScope API Key
dashscope.api_key = config.DASHSCOPE_API_KEY

# --- 配置日志 ---
logger = logging.getLogger(__name__)

def get_available_geojson_files() -> List[str]:
    """
    获取 data 目录下所有 .geojson 文件的文件名列表。
    Returns:
        List[str]: .geojson 文件名列表。
    """
    data_dir = config.DATA_DIRECTORY # 从 config.py 获取 data 目录路径
    try:
        if os.path.exists(data_dir) and os.path.isdir(data_dir):
            # 列出目录下所有以 .geojson 结尾的文件
            files = [f for f in os.listdir(data_dir) if f.lower().endswith('.geojson')]
            logger.debug(f"在 {data_dir} 目录下找到 GeoJSON 文件: {files}")
            return files
        else:
            logger.warning(f"Data 目录不存在或不是一个目录: {data_dir}")
            return []
    except Exception as e:
        logger.error(f"读取 data 目录文件列表时出错: {e}")
        return [] # 出错时返回空列表

def call_dashscope_app(user_query: str) -> Optional[LLMOutput]:
    """
    使用 DashScope SDK 调用阿里云百炼平台的应用处理用户查询。

    Args:
        user_query (str): 用户输入的自然语言请求。

    Returns:
        Optional[LLMOutput]: 大模型返回的结构化结果，如果失败则返回 None。
        
    Raises:
        Exception: 如果 API 调用失败或返回错误。
    """
    available_files = get_available_geojson_files()
    # --- 示例：如何设计提示词让大模型返回特定结构 ---
    system_prompt = """
    你是一个地理空间数据处理助手。用户会提供一个自然语言指令，你需要从中提取关键信息并以严格的 JSON 格式返回。

    请从用户的请求中提取以下信息：
    1. filename: 请求中提到的本地 GeoJSON 文件名（必须是 .geojson 结尾，且存在于服务器指定目录中）。
    2. operation: 要执行的 ArcGIS 几何操作名称（如 buffer, project, intersect 等）。
    3. parameters: 一个包含该操作所需参数的 JSON 对象。
    - 对于需要输入空间参考系 (inSR) 的操作（如 project），如果用户未明确指定，请自动添加 "inSR": 4326 (代表 WGS 1984)。
    - 对于其他操作，只包含其必需的参数。

    请严格按照以下 JSON Schema 返回结果，不要添加任何额外的文字或解释：
    {
    "type": "object",
    "properties": {
        "filename": { "type": "string", "description": "GeoJSON 文件名" },
        "operation": { "type": "string", "description": "ArcGIS 操作名" },
        "parameters": { "type": "object", "description": "操作参数" }
    },
    "required": ["filename", "operation", "parameters"]
    }

    示例：
    用户请求："将 data/park.geojson 文件投影到 Web Mercator 坐标系"
    你的回复应为：
    {
    "filename": "park.geojson",
    "operation": "project",
    "parameters": {
        "inSR": 4326,
        "outSR": 3857
    }
    }

    用户请求："对 data/lines.geojson 文件进行 100 米的缓冲区分析"
    你的回复应为：
    {
    "filename": "lines.geojson",
    "operation": "buffer",
    "parameters": {
        "distances": 100,
        "unit": 9001,
        "outSR": 4326,
        "bufferSR": 3857,
        "inSR": 4326
    }
    }
    对于缓冲区分析一定要规定bufferSR参数为投影坐标系的代码，否则会报错。
    """
    system_prompt+=f"""    当前服务器 data 目录下可用的 GeoJSON 文件列表:
    {json.dumps(available_files, ensure_ascii=False, indent=2)}"""
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_query}
    ]
    
    logger.info(f"Calling DashScope app with query: {user_query}")

    try:
        # 调用 DashScope Generation API
        
        response = Application.call(
            # 若没有配置环境变量，可用百炼API Key将下行替换为：api_key="sk-xxx"。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            api_key=config.DASHSCOPE_API_KEY,
            app_id=config.DASHSCOPE_MODEL_ID,# 替换为实际的应用 ID
            prompt=messages)
        # 检查响应状态
        if response.status_code == HTTPStatus.OK:
            logger.debug(f"DashScope response: {response.output}")
            print(response.output)
            model_output_text = response.output.text
            logger.debug(f"Raw LLM output: {model_output_text}")
            
            try:
                # 尝试直接解析 JSON
                parsed_output = json.loads(model_output_text)
                logger.info("LLM output parsed successfully from direct JSON.")
                # 使用 Pydantic 模型验证并返回
                return LLMOutput(**parsed_output)
            except json.JSONDecodeError as je:
                logger.warning(f"Direct JSON parsing failed: {je}")
                # 尝试提取代码块中的 JSON
                import re
                json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', model_output_text, re.DOTALL)
                if json_match:
                    try:
                        extracted_json_str = json_match.group(1)
                        parsed_output = json.loads(extracted_json_str)
                        logger.info("LLM output parsed successfully from code block.")
                        return LLMOutput(**parsed_output)
                    except json.JSONDecodeError as je2:
                        error_msg = f"Failed to parse JSON from code block: {je2}. Raw output: {model_output_text}"
                        logger.error(error_msg)
                        raise Exception(error_msg)
                else:
                     error_msg = f"无法从模型输出中解析出有效的 JSON: {model_output_text}"
                     logger.error(error_msg)
                     raise Exception(error_msg)

        else:
            error_message = f'调用 DashScope 失败: {response.code}, {response.message}'
            logger.error(error_message)
            if response.code == 'Throttling':
                logger.warning("Request rate limit exceeded.")
            raise Exception(error_message)

    except Exception as e:
        logger.error(f"Error calling DashScope SDK: {e}")
        raise e
