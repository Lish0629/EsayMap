// src/composables/useUpload.js
import GeoJSONLayer from '@arcgis/core/layers/GeoJSONLayer';
import SimpleRenderer from '@arcgis/core/renderers/SimpleRenderer';
import SimpleMarkerSymbol from '@arcgis/core/symbols/SimpleMarkerSymbol';
import SimpleLineSymbol from '@arcgis/core/symbols/SimpleLineSymbol';
import SimpleFillSymbol from '@arcgis/core/symbols/SimpleFillSymbol';
import { useMapStore } from '@/store/mapStore'
import { markRaw, render } from 'vue'
export function useUpload() {
  const layerStore = useMapStore()
  const mutedColorPalette = [
    [102, 153, 153],   // 雾霭青
    [140, 130, 180],   // 灰紫蓝
    [160, 140, 120],   // 大地棕
    [135, 160, 130],   // 灰绿
    [170, 150, 180],   // 暮光粉
    [120, 140, 160],   // 冷灰蓝
    [150, 150, 130],   // 橄榄灰
    [130, 150, 170]    // 浅钢蓝
  ];
  let colorIndex = 0;
  async function uploadFileToServer(file) {
    // 使用 FormData 来包装文件数据，这是文件上传的标准做法
    const formData = new FormData();
    formData.append('file', file); // 'file' 必须与FastAPI中 `File(...)` 的参数名匹配

    try {
      // 假设您的FastAPI后端运行在 http://127.0.0.1:8000
      const response = await fetch('http://127.0.0.1:8000/upload-geojson/', {
        method: 'POST',
        body: formData,
        // 注意：使用 FormData 时，浏览器会自动设置正确的 Content-Type (multipart/form-data)
        // 所以不要手动设置 headers['Content-Type']
      });

      if (!response.ok) {
        // 如果服务器返回错误状态码，则抛出错误
        const errorData = await response.json();
        throw new Error(errorData.detail || '文件上传失败');
      }

      // 解析成功的JSON响应
      return await response.json();

    } catch (error) {
      console.error('上传文件时出错:', error);
      alert(`上传失败: ${error.message}`);
      // 返回一个表示失败的对象
      return { success: false };
    }
  }
  // 新增：将 GeoJSON 对象转换为文件并上传
  async function uploadGeoJsonAsFile(geojsonData, filename = 'result.geojson') {
    try {
      // 将 GeoJSON 对象转换为 JSON 字符串
      const geojsonString = JSON.stringify(geojsonData, null, 2);
      
      // 创建 Blob 对象
      const blob = new Blob([geojsonString], {
        type: 'application/geo+json'
      });
      
      // 创建 File 对象
      const file = new File([blob], filename, {
        type: 'application/geo+json'
      });
      
      // 上传文件
      const result = await uploadFileToServer(file);
      return result;
      
    } catch (error) {
      console.error('GeoJSON 转文件并上传时出错:', error);
      alert(`上传失败: ${error.message}`);
      return { success: false };
    }
  }
  async function handleFileUpload(file) {
    const name = file.name.toLowerCase()
    const uploadResult = await uploadFileToServer(file);
    
    const geometryType = await readGeoJSONAndGetGeometryType(file);
    console.log('Geometry Type:', geometryType);
    const rcolor=createRandomColor();
    const renderer = createRendererByGeometryType(rcolor,geometryType);

    if (name.endsWith('.geojson')) {
      const url = URL.createObjectURL(file)
      console.log(url)
      const layer = new GeoJSONLayer({
        url: url,
        title: file.name,
        visible: true,
        opacity:0.8,
        ...(renderer && { renderer }) 
      });
      layerStore.addLayer({
        id: file.name,
        title: file.name,
        visible: true,
        opacity: 0.8,
        color:rcolor,
        type: 'vector',
        instance: markRaw(layer)
      })
      } else {
      alert('仅支持 .geojson文件')
    }
  }
  function readGeoJSONAndGetGeometryType(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
  
      reader.onload = (event) => {
        try {
          const json = JSON.parse(event.target.result);
  
          // 提取几何类型
          let type = null;
  
          if (json.type === 'FeatureCollection' && Array.isArray(json.features) && json.features.length > 0) {
            type = json.features[0].geometry?.type;
          } else if (json.type === 'Feature') {
            type = json.geometry?.type;
          } else if (['Point', 'LineString', 'Polygon', 'MultiPoint', 'MultiLineString', 'MultiPolygon'].includes(json.type)) {
            type = json.type;
          }
  
          if (!type) {
            return resolve(null); // 无有效几何
          }
  
          // 标准化为 ArcGIS 风格的小写基础类型
          const normalizedType = type.startsWith('Multi') 
            ? type.slice(5).toLowerCase() 
            : type.toLowerCase();
  
          // 映射为 ArcGIS layer.geometryType 风格
          const arcgisTypeMap = {
            point: 'point',
            linestring: 'polyline',
            polygon: 'polygon'
          };
  
          resolve(arcgisTypeMap[normalizedType] || null);
        } catch (e) {
          console.error('解析 GeoJSON 失败', e);
          resolve(null); // 解析失败返回 null
        }
      };
  
      reader.onerror = () => {
        console.error('文件读取失败', reader.error);
        resolve(null);
      };
  
      reader.readAsText(file);
    });
  }
  function createRandomColor() {
    const color = mutedColorPalette[colorIndex];
    colorIndex = (colorIndex + 1) % mutedColorPalette.length;
    return color;
  }
  function createRendererByGeometryType(color,type) {

    let symbol;
    switch (type) {
      case 'point':
        symbol = new SimpleMarkerSymbol({
          color: color,
          size: 8,
          style: 'circle',
          outline: {
            color: [200, 200, 200],
            width: 1.5
          }
        });
        break;

      case 'polyline':
        symbol = new SimpleLineSymbol({
          color: color,
          width: 3
        });
        break;

      case 'polygon':
        symbol = new SimpleFillSymbol({
          color: [...color, 0.6], // 半透明填充
          outline: {
            color: [80, 80, 80],  // 深灰边框，清晰但不突兀
            width: 1.8
          }
        });
        break;

      default:
        return null;
    }

    return new SimpleRenderer({ symbol });
  }
  return { handleFileUpload, uploadFileToServer,uploadGeoJsonAsFile,createRendererByGeometryType,createRandomColor}
}
