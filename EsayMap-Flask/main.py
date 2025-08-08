from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import os
import json

from config import GEOJSON_DATA_PATH
from nlp_processor import get_gis_analysis_from_qwen
from gptool_handler import execute_arcgis_gp_task

# --- FastAPI 应用实例 ---
app = FastAPI(
    title="Qwen-ArcGIS地理分析桥接服务",
    description="利用Qwen模型解析自然语言，并调用ArcGIS Server REST API执行地理分析。",
    version="1.0.0"
)

# --- 请求体模型 (Pydantic) ---
class AnalysisRequest(BaseModel):
    query: str
    geojson_filename: str

# --- API 端点 ---
@app.post("/analyze", tags=["GIS Analysis"])
async def perform_gis_analysis(request: AnalysisRequest = Body(...)):
    """
    接收用户地理分析请求，执行并返回结果。

    - **query**: 用户的自然语言请求 (例如: "帮我对这些学校做1公里的缓冲区")
    - **geojson_filename**: 存放在服务器`data`目录下的GeoJSON文件名 (例如: "schools.geojson")
    """
    # 1. 定位并读取本地GeoJSON文件
    geojson_path = os.path.join(GEOJSON_DATA_PATH, request.geojson_filename)
    if not os.path.exists(geojson_path):
        raise HTTPException(status_code=404, detail=f"GeoJSON文件未找到: {request.geojson_filename}")

    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"读取或解析GeoJSON文件失败: {e}")

    # 2. 调用Qwen NLP模块进行意图识别
    try:
        gis_instruction = get_gis_analysis_from_qwen(request.query)
        tool_name = gis_instruction.get("tool_name")
        parameters = gis_instruction.get("parameters")

        if not tool_name or not parameters:
            raise ValueError("NLP模型未能正确解析出tool_name或parameters。")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"调用Qwen模型或解析其响应时出错: {e}")

    # 3. 调用通用的ArcGIS GP服务执行函数
    try:
        arcgis_result = execute_arcgis_gp_task(
            tool_name=tool_name,
            parameters=parameters,
            input_data=geojson_data # <--- 修改这里
        )
        return arcgis_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行ArcGIS地理处理任务时出错: {e}")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "欢迎使用 Qwen-ArcGIS 地理分析桥接服务"}