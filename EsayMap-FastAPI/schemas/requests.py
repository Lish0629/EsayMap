# schemas/requests.py
from pydantic import BaseModel
from typing import Dict, Any

class ProcessRequest(BaseModel):
    """
    用户向后端发送的处理请求数据模型。
    """
    query: str # 用户的自然语言请求
