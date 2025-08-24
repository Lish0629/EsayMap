# schemas/responses.py
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class ProcessResponse(BaseModel):
    """
    后端处理完成后返回给前端的响应数据模型。
    """
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None # ArcGIS Server 返回的最终结果
    error: Optional[str] = None # 错误信息（如果有的话）
    type : str
class LLMOutput(BaseModel):
    """
    大模型解析用户请求后返回的结构化信息。
    这与 llm/processor.py 中期望的输出格式一致。
    """
    filename: str
    operation: str
    parameters: Dict[str, Any]
    
