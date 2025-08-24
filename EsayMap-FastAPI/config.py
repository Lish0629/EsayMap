# config.py

import os
from dotenv import load_dotenv # 导入 dotenv

# 加载 .env 文件中的环境变量
# load_dotenv() 会自动查找项目根目录下的 .env 文件
load_dotenv()

# --- 百炼大模型配置 ---
# 从环境变量或 .env 文件获取
# API Key
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
# 模型/应用 ID
DASHSCOPE_MODEL_ID = os.getenv("DASHSCOPE_MODEL_ID")
DASHSCOPE_MODEL_ID_ADD = os.getenv("DASHSCOPE_MODEL_ID_ADD")

# --- 修改：使用静态 Token ---
ARCGIS_STATIC_TOKEN = os.getenv("ARCGIS_STATIC_TOKEN") # 从环境变量获取静态 token

# --- 其他配置 ---
# 优先从环境变量获取，如果没有则使用默认值
DATA_DIRECTORY = os.getenv("DATA_DIRECTORY", ".\data")
GEOMETRY_SERVICE_URL = os.getenv("GEOMETRY_SERVICE_URL", "https://gis.dev.local:6443/geoscene/rest/services/Utilities/Geometry/GeometryServer")

# --- 强制要求关键配置 ---
if not DASHSCOPE_API_KEY:
    raise ValueError("未在 .env 文件中设置 DASHSCOPE_API_KEY")

if not DASHSCOPE_MODEL_ID:
    raise ValueError("未在 .env 文件中设置 DASHSCOPE_MODEL_ID")
