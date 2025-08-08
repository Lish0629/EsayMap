import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# --- Qwen API 配置 ---
# 推荐使用环境变量来设置API Key
# 你可以在你的阿里云账户中获取
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "sk-your_qwen_api_key_here")
#QWEN_API_BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
QWEN_API_BASE_URL = "https://dashscope.aliyuncs.com/api/v1/apps/37d3d91185b54789b6a1de821ce72a4c/completion"

# --- ArcGIS Server 配置 ---
# 你的ArcGIS Server GP服务的基础URL
# 例如: "https://your-server.com/arcgis/rest/services/MyGPTools/GPServer"
ARCGIS_GP_SERVER_URL = os.getenv("ARCGIS_GP_SERVER_URL", "https://your-server.com/arcgis/rest/services/Utilities/PrintingTools/GPServer")

# --- 本地数据配置 ---
# GeoJSON文件存放的根目录
GEOJSON_DATA_PATH = "data"