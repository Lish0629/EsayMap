import requests
import json
from config import QWEN_API_KEY
import os
from dashscope import Generation,Application
def get_gis_analysis_from_qwen(user_query: str) -> dict:
    """
    将用户的自然语言查询发送给Qwen模型，解析为GIS分析指令。

    Args:
        user_query: 用户的自然语言请求，例如 "帮我对输入要素创建一个1公里的缓冲区"。

    Returns:
        一个包含 'tool_name' 和 'parameters' 的字典，其中距离和单位是分开的。
        例如:
        {
            "tool_name": "Buffer",
            "parameters": {
                "geometries": "__GEOJSON_INPUT__",
                "distance": 1,
                "unit": "Kilometers",
                "unionResults": true
            }
        }
    """
    if not QWEN_API_KEY or "your_qwen_api_key" in QWEN_API_KEY:
        raise ValueError("Qwen API密钥未在config.py或.env文件中正确配置。")

    headers = {
        'Authorization': f'Bearer {QWEN_API_KEY}',
        'Content-Type': 'application/json'
    }

    # --- 关键的Prompt工程 ---
    # 我们引导模型它的角色、任务、以及严格的、结构化的输出格式。
    # 特别强调了需要将距离和单位拆分为独立的字段。
    prompt = f"""
    你是一个专业的GIS分析助手。你的任务是解析用户的自然语言地理分析请求，
    并将其转换为ArcGIS Server REST API地理处理（GP）服务能理解的JSON格式。

    你必须只输出一个JSON对象，不要包含任何解释性文字或代码块标记。
    这个JSON对象必须包含两个键： "tool_name" 和 "parameters"。

    - "tool_name": 必须是ArcGIS GP工具的精确名称（区分大小写），例如 'Buffer', 'Clip', 'Intersect'。
    - "parameters": 一个JSON对象，包含调用该工具所需的所有参数。
      - 如果用户的请求提到了一个需要进行分析的输入图层或要素，请使用 "__GEOJSON_INPUT__" 作为该参数的值。对应的参数键通常是 "geometries" 或 "in_features"。
      - 对于距离相关的参数，你必须将其拆分为 "distance" (一个数字) 和 "unit" (一个字符串，例如 'Meters', 'Kilometers', 'Miles', 'Feet') 这两个独立的键。
      - 其他参数如 "unionResults" (布尔值) 如果在请求中被提及（例如“融合结果”、“合并结果”），也应正确提取。

    下面是一些示例：

    用户请求: "给我对输入要素创建一个500米的缓冲区，并融合结果"
    你的回答:
    {{
        "tool_name": "Buffer",
        "parameters": {{
            "geometries": "__GEOJSON_INPUT__",
            "distance": 500,
            "unit": "Meters",
            "unionResults": true
        }}
    }}

    用户请求: "我想对这些点做个10英里的缓冲分析，不用合并。"
    你的回答:
    {{
        "tool_name": "Buffer",
        "parameters": {{
            "geometries": "__GEOJSON_INPUT__",
            "distance": 10,
            "unit": "Miles",
            "unionResults": false
        }}
    }}
    
    用户请求: "计算输入图层的几何中心点"
    你的回答:
    {{
        "tool_name": "Centroids",
        "parameters": {{
            "in_features": "__GEOJSON_INPUT__"
        }}
    }}

    现在，请根据以下用户请求生成对应的JSON：

    用户请求: "{user_query}"
    你的回答:
    """

    body = {
        'model': 'qwen-turbo', # 或使用更强大的模型如 qwen-plus, qwen-max
        'input': {
            'prompt': prompt
        },
        'parameters': {
            'result_format': 'text'
        }
    }

    try:
        #response = requests.post(QWEN_API_BASE_URL, headers=headers, json=body, timeout=20)
        #response.raise_for_status()  # 如果请求失败(如4xx, 5xx)则抛出HTTPError

        #raw_response = response.json()

        response = Application.call(
            api_key=os.getenv("QWEN_API_KEY"),
            app_id='37d3d91185b54789b6a1de821ce72a4c',
            prompt=prompt
        )
        #提取模型生成的文本内容
        #content = raw_response.get("output", {}).get("text", "")
        content = response.output.text

        if not content:
            raise ValueError("Qwen API返回内容为空。")

        # 清理模型可能返回的多余字符，例如代码块标记
        if content.strip().startswith("```json"):
            content = content.strip()[7:-3].strip()
        elif content.strip().startswith("```"):
            content = content.strip()[3:-3].strip()

        # 将清理后的文本内容解析为JSON字典
        return json.loads(content)

    except requests.exceptions.RequestException as e:
        print(f"请求Qwen API时出错: {e}")
        # 在实际应用中，这里应该返回一个更友好的错误或进行重试
        raise
    except (json.JSONDecodeError, ValueError) as e:
        print(f"解析Qwen API响应时出错: {e}, 原始响应内容: '{content}'")
        raise