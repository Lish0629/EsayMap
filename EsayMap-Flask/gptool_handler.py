import requests
import json
from config import ARCGIS_GP_SERVER_URL

# 单位映射: 将NLP友好的单位名称映射到ArcGIS API所需的精确常量
UNIT_MAPPING = {
    "Meters": "esriSRUnit_Meter",
    "Kilometers": "esriSRUnit_Kilometer",
    "Feet": "esriSRUnit_Foot",
    "Miles": "esriSRUnit_Mile"
}

def execute_arcgis_gp_task(
        tool_name: str,
        parameters: dict,
        input_data: dict
) -> dict:
    """
    一个通用的函数，用于执行ArcGIS Server的地理处理任务。

    (最终健壮版)
    - 假定输入文件中的几何和属性已是Esri格式。
    - 自动将单个Feature包装成FeatureSet。
    - 正确处理距离和单位参数。
    """
    tool_url = f"{ARCGIS_GP_SERVER_URL}/{tool_name}/execute"
    print(f"正在向ArcGIS Server发送请求: {tool_url}")

    # --- 1. 智能构建 Esri FeatureSet ---
    arcgis_features = []
    geometry_type = ""
    spatial_reference = {"wkid": 4326} # 默认SR

    # 检查输入数据是单个Feature还是一个FeatureSet/FeatureCollection
    if "features" in input_data and isinstance(input_data["features"], list):
        # A. 输入是一个FeatureSet或类似的结构
        print("检测到输入为FeatureSet/FeatureCollection格式。")
        arcgis_features = input_data["features"]
        geometry_type = input_data.get("geometryType", "")
        if "spatialReference" in input_data:
            spatial_reference = input_data["spatialReference"]
    elif "geometry" in input_data:
        # B. 输入是单个Feature
        print("检测到输入为单个Feature格式，将自动包装为FeatureSet。")
        arcgis_features = [input_data] # 将单个feature放入数组中
        # 尝试从单个要素的几何中推断类型
        geom = input_data.get("geometry", {})
        if "rings" in geom: geometry_type = "esriGeometryPolygon"
        elif "paths" in geom: geometry_type = "esriGeometryPolyline"
        elif "x" in geom and "y" in geom: geometry_type = "esriGeometryPoint"
        if "spatialReference" in geom:
            spatial_reference = geom["spatialReference"]
    else:
        raise ValueError("输入文件内容既不是有效的Esri Feature，也不是FeatureSet。")

    if not geometry_type and arcgis_features:
        raise ValueError("无法确定FeatureSet的geometryType。")

    # 构建最终的FeatureSet
    feature_set = {
        "geometryType": geometry_type,
        "features": arcgis_features,
        "spatialReference": spatial_reference
    }

    # --- 2. 构建请求参数 ---
    request_params = {}
    for key, value in parameters.items():
        if isinstance(value, str) and value == "__GEOJSON_INPUT__":
            request_params[key] = json.dumps(feature_set)
        elif key == "distance":
            request_params["distances"] = f"[{value}]"
        elif key == "unit":
            api_unit = UNIT_MAPPING.get(value)
            if not api_unit: raise ValueError(f"不支持的单位: {value}")
            request_params["unit"] = api_unit
        else:
            request_params[key] = value

    # --- 3. 注入必要的执行参数 ---
    request_params["inSR"] = spatial_reference.get("wkid", 4326)
    request_params["bufferSR"] = 3857
    request_params["outSR"] = 3857
    request_params["f"] = 'json'

    print(f"发送到ArcGIS的最终参数: { {k: v[:200] + '...' if isinstance(v, str) and len(v) > 200 else v for k, v in request_params.items()} }")
    try:
        response = requests.post(tool_url, data=request_params, timeout=90)
        response.raise_for_status()
        result = response.json()
        if "error" in result:
            print(f"ArcGIS Server返回错误: {result['error']}")
            raise Exception(f"ArcGIS Server Error: {result['error']}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求ArcGIS Server时发生网络错误: {e}")
        raise

