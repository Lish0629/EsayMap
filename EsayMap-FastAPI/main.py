# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import traceback
import logging

# --- 配置日志 ---
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__) # 创建一个名为 __main__ 的 logger

# 导入项目内部模块
from schemas.requests import ProcessRequest
from schemas.responses import ProcessResponse, LLMOutput
from llm.processor import call_dashscope_app
from converters.geojson_to_esri import process_geojson_file_to_esri
from arcgis_utils.client import execute_geometry_operation

app = FastAPI(title="EasyMap GeoProcessor API", version="1.0.0")

# --- 配置 CORS (如果前端从不同源访问) ---
# 允许所有来源 (仅用于开发，生产环境请具体配置)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 在生产中应替换为具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """
    API 根路径，用于健康检查。
    """
    logger.info("Health check endpoint accessed.")
    return {"message": "EasyMap GeoProcessor API is running!"}

@app.post("/process-request", response_model=ProcessResponse)
async def process_user_request(request: ProcessRequest):
    """
    处理用户的自然语言地理处理请求。
    1. 调用大模型解析请求。
    2. 加载并转换 GeoJSON 文件。
    3. 调用 ArcGIS Server 执行几何操作。
    4. 返回结果。
    """
    logger.info(f"Received user request: {request.query}")
    
    try:
        # --- 步骤 1: 调用大模型解析用户请求 ---
        llm_output: LLMOutput = call_dashscope_app(request.query)
        if not llm_output:
            error_msg = "无法解析用户请求，请检查输入或稍后重试。"
            logger.warning(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        logger.info(f"LLM parsed result: {llm_output}")

        # --- 步骤 2: 加载并转换 GeoJSON 文件 ---
        logger.info(f"Loading and converting GeoJSON file: {llm_output.filename}")
        esri_geometries = process_geojson_file_to_esri(llm_output.filename)
        logger.info(f"GeoJSON file loaded and converted successfully.")

        # --- 步骤 3: 调用 ArcGIS Server 执行几何操作 ---
        logger.info(f"Calling ArcGIS Server to perform operation: {llm_output.operation}")
        arcgis_result = execute_geometry_operation(
            esri_geometries=esri_geometries,
            operation=llm_output.operation,
            operation_params=llm_output.parameters
        )
        logger.info(f"ArcGIS Server operation completed successfully.")

        # --- 步骤 4: 返回成功结果 ---
        success_msg = f"成功处理请求: {request.query}"
        logger.info(success_msg)
        return ProcessResponse(
            success=True,
            message=success_msg,
            data=arcgis_result
        )

    except HTTPException as he:
        # 直接重新抛出 FastAPI 的 HTTPException
        logger.error(f"HTTPException occurred: {he.detail}")
        raise he
    except Exception as e:
        # 处理所有其他未预期的错误
        error_msg = f"处理请求时发生内部错误: {e}"
        logger.error(error_msg)
        # 打印堆栈跟踪以便调试
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=error_msg)

# --- 为了方便开发和测试，可以添加一个直接调用 ArcGIS 的端点 ---
@app.post("/arcgis-direct", response_model=ProcessResponse)
async def direct_arcgis_call(operation: str, geometries: dict, params: dict):
    """
    (可选) 直接调用 ArcGIS Server 进行测试，绕过大模型和文件加载步骤。
    方便调试 ArcGIS 连接和参数。
    """
    logger.info(f"Direct ArcGIS call: operation={operation}")
    try:
        result = execute_geometry_operation(
            esri_geometries=geometries,
            operation=operation,
            operation_params=params
        )
        success_msg = f"直接调用 ArcGIS Server '{operation}' 成功。"
        logger.info(success_msg)
        return ProcessResponse(
            success=True,
            message=success_msg,
            data=result
        )
    except Exception as e:
        error_msg = f"直接调用 ArcGIS Server 失败: {e}"
        logger.error(error_msg)
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application...")
    # 使用 Uvicorn 运行 FastAPI 应用
    # host="0.0.0.0" 允许外部访问，开发时方便，生产环境请根据需要配置
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
