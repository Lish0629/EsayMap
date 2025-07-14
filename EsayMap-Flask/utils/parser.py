def parse_response_to_instruction(text):
    """
    假设返回的格式为：
    执行缓冲分析，半径为 1000 米。
    """
    if "缓冲" in text:
        radius = 1000
        if "半径" in text:
            import re
            match = re.search(r"(\d+)", text)
            if match:
                radius = int(match.group(1))
        return {
            "endpoint": "/api/gp/buffer",
            "params": {
                "radius": radius
            }
        }
    elif "相交" in text:
        return {
            "endpoint": "/api/gp/intersect",
            "params": {}
        }

    return {"error": "无法解析分析类型"}
