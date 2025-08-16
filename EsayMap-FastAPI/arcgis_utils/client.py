# arcgis/client.py

import requests
import json
import time
import logging
from typing import Dict, Any, Optional
import config

# --- 配置日志 ---
logger = logging.getLogger(__name__)

def execute_geometry_operation(
    esri_geometries: Dict[str, Any],
    operation: str,
    operation_params: Dict[str, Any],
    common_params: Optional[Dict[str, Any]] = None,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> Dict[str, Any]:
    """
    通过 ArcGIS Server REST API 执行几何操作。

    Args:
        esri_geometries (Dict[str, Any]): 包含几何类型和几何对象数组的 Esri JSON 字典。
                                          格式: {"geometryType": "...", "geometries": [...]}.
        operation (str): 要执行的几何操作名称 (例如 'buffer', 'project', 'areasAndLengths')。
        operation_params (Dict[str, Any]): 执行操作所需的特定参数字典。
        common_params (Optional[Dict[str, Any]]): 适用于所有 REST 操作的通用参数 (例如 f=json)。
        max_retries (int): 最大重试次数。
        retry_delay (float): 重试之间的延迟（秒）。

    Returns:
        Dict[str, Any]: ArcGIS Server 返回的 JSON 响应。
        
    Raises:
        Exception: 如果 API 调用失败或返回错误。
    """
    
    if common_params is None:
        common_params = {"f": "pjson"}
        
    # 1. 动态构建端点 URL
    base_endpoint_url = f"{config.GEOMETRY_SERVICE_URL}/{operation}"
    logger.info(f"Calling ArcGIS Server endpoint: {base_endpoint_url}")
    # 2. 准备所有 URL 查询参数
    # 创建一个字典来存放所有查询参数
    query_params = {}
    

    # 添加几何数组 (需要序列化为 JSON 字符串)
    if 'geometries' in esri_geometries:
        # ArcGIS REST API 期望几何数据作为 'geometries' 参数的 JSON 字符串值
        query_params['geometries'] = json.dumps(esri_geometries, separators=(',', ':')) # 使用紧凑格式
        query_params['polygons'] = json.dumps(esri_geometries['geometries'], separators=(',', ':'))
    else:
        logger.error("Missing 'geometries' array in esri_geometries")
        raise ValueError("Missing 'geometries' array in esri_geometries")
        
    # 添加操作特定参数
    query_params.update(operation_params)
    
    # 添加通用参数 (如 f=json)
    query_params.update(common_params)
    #print(esri_geometries)
    print(query_params)
    # *** 添加 Token (如果配置了) ***
    # if config.ARCGIS_STATIC_TOKEN:
    #     query_params['token'] = config.ARCGIS_STATIC_TOKEN
    #     logger.debug("Added static token to the request parameters.")
    # else:
    #     logger.warning("No static token configured. Request might fail if authentication is required.")
    # *** 结束添加 ***
    
    # 3. 发送 POST 请求，包含重试逻辑
    for attempt in range(max_retries + 1):
        try:
            logger.debug(f"Sending POST request (Attempt {attempt + 1}/{max_retries + 1})...")
            
            response = requests.get(
                base_endpoint_url, # 基础 URL
                params=query_params, # 所有参数作为查询参数
                timeout=30,
                verify=False # 保留以处理自签名证书
            )
            logger.debug(f"Request sent. Status Code: {response.status_code}")
            
            # *** 添加调试信息：检查响应内容 ***
            logger.debug(f"Raw response text (first 500 chars): {response.text[:500]}")
            logger.debug(f"Response headers: {response.headers}")
            # *** 结束添加 ***
            
            # 检查 HTTP 状态码
            response.raise_for_status() # 如果状态码是 4xx 或 5xx，会抛出 HTTPError

            # 尝试解析 JSON
            try:
                result = response.json()
                logger.debug("Response parsed as JSON successfully.")
            except json.JSONDecodeError as je:
                # 如果解析 JSON 失败，记录详细错误和原始响应
                error_msg = f"Failed to decode response as JSON: {je}. Raw response (first 1000 chars): '{response.text[:1000]}'"
                logger.error(error_msg)
                raise requests.exceptions.JSONDecodeError(error_msg, response.text, 0) from je

            # ... (后续处理逻辑不变，检查 'error' 键等) ...
            
            # 4. 处理响应
            # 检查 result 中是否有 'error' 键
            if 'error' in result:
                error_code = result['error'].get('code', 'Unknown')
                error_message = result['error'].get('message', 'No message')
                log_msg = f"ArcGIS Server returned error (Attempt {attempt + 1}/{max_retries + 1}): Code {error_code}, Message: {error_message}"
                logger.warning(log_msg)
                
                # ... (重试逻辑不变) ...
            
            logger.info(f"Operation '{operation}' executed successfully.")
            return result
            
        except requests.exceptions.RequestException as e:
            # ... (现有的网络错误处理逻辑不变) ...
            # 但可以稍微改进一下最终的错误信息，包含状态码
            final_error = f"Network request failed (Attempt {attempt + 1}/{max_retries + 1}): {e} (Status Code: {getattr(e.response, 'status_code', 'N/A')})"
            logger.warning(final_error)
            if attempt < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Network request failed after {max_retries + 1} attempts: {e}")
                raise Exception(f"Network request failed (after {max_retries + 1} attempts): {e}")
        except json.JSONDecodeError as e:
             # 专门处理 JSON 解析错误
             logger.error(f"JSON decode error on attempt {attempt + 1}: {e}")
             if attempt < max_retries:
                 logger.info(f"Retrying in {retry_delay} seconds...")
                 time.sleep(retry_delay)
             else:
                 logger.error(f"Failed to get valid JSON response after {max_retries + 1} attempts.")
                 raise Exception(f"Failed to get valid JSON response from ArcGIS Server (after {max_retries + 1} attempts): {e}")
        except Exception as e:
            logger.exception("Unexpected error during ArcGIS operation:")
            raise e
