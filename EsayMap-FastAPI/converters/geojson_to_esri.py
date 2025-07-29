# converters/geojson_to_esri.py

import json
import os
from typing import Dict, Any, Optional
from arcgis.features import FeatureSet
import config


def load_geojson_file(filename: str) -> Optional[Dict[str, Any]]:
    """
    从指定目录安全地加载 GeoJSON 文件。

    Args:
        filename (str): GeoJSON 文件名 (例如 'park.geojson')。

    Returns:
        Optional[Dict[str, Any]]: 加载的 GeoJSON 数据字典，如果失败则返回 None。
        
    Raises:
        Exception: 如果文件不存在、不是 GeoJSON 格式或加载失败。
    """
    # 防止路径遍历攻击，确保文件名安全
    if '..' in filename or filename.startswith('/'):
        raise ValueError("无效的文件名。")

    # 确保文件名以 .geojson 结尾
    if not filename.lower().endswith('.geojson'):
        raise ValueError("文件名必须以 .geojson 结尾。")

    # 构建完整文件路径
    file_path = os.path.join(config.DATA_DIRECTORY, filename)

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件未找到: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
            
        # 简单验证是否为有效的 GeoJSON (FeatureCollection 或 Feature)
        if not isinstance(geojson_data, dict):
            raise ValueError("文件内容不是有效的 JSON 对象。")
            
        geojson_type = geojson_data.get('type')
        if geojson_type not in ['FeatureCollection', 'Feature']:
            raise ValueError(f"不支持的 GeoJSON 类型: {geojson_type}。期望 'FeatureCollection' 或 'Feature'。")
            
        return geojson_data

    except json.JSONDecodeError as e:
        raise ValueError(f"文件 {filename} 不是有效的 JSON 格式: {e}")
    except Exception as e:
        raise Exception(f"加载 GeoJSON 文件 {filename} 时出错: {e}")


def convert_geojson_to_esri(geojson_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    将 GeoJSON 数据转换为 Esri JSON 格式 (主要是几何部分)。
    为了兼容 arcgis.features.FeatureSet.from_geojson，会将单个 Feature 包装成 FeatureCollection。

    Args:
        geojson_data (Dict[str, Any]): 已加载的 GeoJSON 数据字典。

    Returns:
        Dict[str, Any]: 包含 Esri JSON 几何对象的字典，符合 ArcGIS REST API 要求。
        
    Raises:
        Exception: 如果转换失败。
    """
    try:
        # --- 预处理：确保输入是 FeatureCollection 格式 ---
        processed_geojson = geojson_data
        if geojson_data.get('type') == 'Feature':
            print("检测到单个 Feature，正在包装成 FeatureCollection...")
            processed_geojson = {
                "type": "FeatureCollection",
                "features": [geojson_data]
            }
        # 如果已经是 FeatureCollection，则 processed_geojson 保持不变

        # 使用 arcgis.features.FeatureSet.from_geojson 进行转换
        feature_set = FeatureSet.from_geojson(processed_geojson)
        
        # 获取 FeatureSet 的字典表示
        feature_set_dict = feature_set.to_dict()
        
        # 准备输出结构
        esri_geometries = []
        geometry_type = None
        
        # 遍历转换后的要素
        for feature_dict in feature_set_dict.get('features', []):
            # 直接从 feature_dict 中提取几何信息
            geom_dict = feature_dict.get('geometry')
            
            if geom_dict:
                esri_geometries.append(geom_dict)
                
                # 确定几何类型 (所有要素应为同一类型，取第一个即可)
                if geometry_type is None:
                    # 从 feature_dict 的顶层获取 geometryType (FeatureSet.to_dict() 通常会提供)
                    geometry_type = feature_dict.get('geometryType')
                    # 如果没有，则通过几何字典内容推断
                    if not geometry_type:
                        if 'rings' in geom_dict:
                            geometry_type = 'esriGeometryPolygon'
                        elif 'paths' in geom_dict:
                            geometry_type = 'esriGeometryPolyline'
                        elif 'x' in geom_dict and 'y' in geom_dict:
                            geometry_type = 'esriGeometryPoint'
                        elif 'points' in geom_dict:
                            geometry_type = 'esriGeometryMultipoint'
                        elif 'xmin' in geom_dict and 'ymin' in geom_dict and 'xmax' in geom_dict and 'ymax' in geom_dict:
                            geometry_type = 'esriGeometryEnvelope'
                        else:
                            geometry_type = 'esriGeometryNull'
        
        if not esri_geometries:
            raise ValueError("GeoJSON 数据中未找到有效的几何对象。")
            
        if geometry_type is None or geometry_type == 'esriGeometryNull':
             # Fallback: 尝试从 FeatureSet 本身获取类型
             fs_geom_type = getattr(feature_set, 'geometry_type', None)
             if fs_geom_type:
                 geom_type_map = {
                    'Point': 'esriGeometryPoint',
                    'MultiPoint': 'esriGeometryMultipoint',
                    'LineString': 'esriGeometryPolyline',
                    'MultiLineString': 'esriGeometryPolyline',
                    'Polygon': 'esriGeometryPolygon',
                    'MultiPolygon': 'esriGeometryPolygon'
                 }
                 geometry_type = geom_type_map.get(fs_geom_type, 'esriGeometryNull')
                 
             if geometry_type is None or geometry_type == 'esriGeometryNull':
                 raise ValueError("无法确定几何类型。")

        # 构造符合 ArcGIS REST API 覃求的输入格式
        esri_json_output = {
            "geometryType": geometry_type,
            "geometries": esri_geometries
        }
        
        print(f"成功转换 GeoJSON 到 Esri JSON。几何类型: {geometry_type}, 要素数量: {len(esri_geometries)}")
        return esri_json_output

    except Exception as e:
        # 打印原始异常信息以便调试
        import traceback
        traceback.print_exc()
        raise Exception(f"GeoJSON 转 Esri JSON 失败: {e}")


# --- 测试和组合函数 ---
def process_geojson_file_to_esri(filename: str) -> Dict[str, Any]:
    """
    加载 GeoJSON 文件并将其转换为 Esri JSON 格式。
    这是一个组合函数，方便其他模块调用。

    Args:
        filename (str): GeoJSON 文件名。

    Returns:
        Dict[str, Any]: Esri JSON 格式的几何数据。
    """
    geojson_data = load_geojson_file(filename)
    esri_json_data = convert_geojson_to_esri(geojson_data)
    return esri_json_data


# --- 测试代码 ---
if __name__ == "__main__":
    # 确保 ./data 目录存在并包含一个测试文件，例如 test.geojson
    test_filename = "test.geojson" # 使用我们创建的测试文件
    try:
        print(f"正在加载并转换文件: {test_filename}")
        esri_result = process_geojson_file_to_esri(test_filename)
        print("\n--- 转换成功的 Esri JSON ---")
        # 打印格式化后的 JSON，确保中文正常显示
        print(json.dumps(esri_result, indent=2, ensure_ascii=False))
        print("\n--- 转换完成 ---")
    except FileNotFoundError as e:
        print(f"文件未找到错误: {e}")
        print("请确保在项目根目录下创建 'data' 文件夹，并放入 'test.geojson' 文件。")
    except ValueError as e:
        print(f"数据格式错误: {e}")
    except Exception as e:
        print(f"转换过程出错: {e}")
