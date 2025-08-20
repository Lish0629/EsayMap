# main.py
from pathlib import Path  # 导入Path模块用于处理路径

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, UploadFile, File
import logging
import shutil  # 导入shutil用于文件操作
from fastapi.staticfiles import StaticFiles

# --- 配置日志 ---
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__) # 创建一个名为 __main__ 的 logger

# 导入项目内部模块
from schemas.requests import ProcessRequest
from schemas.responses import ProcessResponse, LLMOutput
from llm.processor import call_dashscope_app,generate_geojson_from_llm
from converters.geojson_to_esri import process_geojson_file_to_esri
from arcgis_utils.client import execute_geometry_operation

app = FastAPI(title="EasyMap GeoProcessor API", version="1.0.0")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True) # 确保data文件夹存在
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data_files")
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
@app.post("/upload-geojson/")
async def upload_geojson_file(file: UploadFile = File(...)):
    """
    接收前端上传的 GeoJSON 文件，并将其保存到服务器的 data 目录中。
    """
    if not file.filename.lower().endswith('.geojson'):
        raise HTTPException(status_code=400, detail="文件格式无效，仅支持 .geojson 文件。")
    
    original_filename = file.filename
    # 定义文件的保存路径
    # 为了安全，我们只使用文件名，防止路径遍历攻击
    # file_path = DATA_DIR / Path(file.filename).name
    
    logger.info(f"接收到文件: {file.filename}")
    
    import re

    filename_without_ext = Path(original_filename).stem  # 获取不带扩展名的文件名
    print(filename_without_ext)
    # 清理文件名：删除中文字符，只保留字母、数字、下划线
    clean_filename = re.sub(r'[\u4e00-\u9fa5]', '', filename_without_ext)  # 删除中文
    clean_filename = re.sub(r'[^a-zA-Z0-9_]', '', clean_filename)         # 只保留字母、数字、下划线
    
    # 转换为小写
    clean_filename = clean_filename.lower()
    
    if not clean_filename or len(clean_filename.strip()) == 0:
        clean_filename = 'uploaded_file'
    
    safe_filename = f"{clean_filename}.geojson"

    file_path = DATA_DIR / safe_filename
    
    logger.info(f"生成的安全文件名: {safe_filename}, 准备保存到: {file_path}")

    try:
        # 使用 shutil.copyfileobj 保存文件，效率更高
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"保存文件时出错: {e}")
        raise HTTPException(status_code=500, detail=f"无法保存文件: {e}")
    finally:
        file.file.close() # 确保文件句柄被关闭

    return {
        "success": True,
        "message": f"文件 '{file.filename}' 上传成功。",
        "filename": file.filename
    }
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
            data=arcgis_result,
            llm_raw_response=llm_output
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
@app.post("/generate-geojson-feature")
async def generate_geojson_feature(request: ProcessRequest):
    """
    处理添加要素的请求。
    调用大模型生成GeoJSON要素并返回。
    """
    logger.info(f"Received generate GeoJSON feature request: {request.query}")
    
    try:
        # 调用大模型生成GeoJSON要素
        geojson_result = generate_geojson_from_llm(request.query)

        if not geojson_result:
            error_msg = "无法生成要素，请检查输入或稍后重试。"
            logger.warning(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)
        
        logger.info(f"Successfully generated GeoJSON feature")
        
        # 返回成功结果，包含生成的GeoJSON
        success_msg = f"成功生成要素"
        logger.info(success_msg)
        
        return ProcessResponse(
            success=True,
            message=success_msg,
            data={"geojson": geojson_result},
            llm_raw_response="要素生成成功"
        )

    except HTTPException as he:
        logger.error(f"HTTPException occurred: {he.detail}")
        raise he
    except Exception as e:
        error_msg = f"生成要素时发生内部错误: {e}"
        logger.error(error_msg)
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
