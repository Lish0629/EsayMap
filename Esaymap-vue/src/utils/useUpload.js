// src/composables/useUpload.js

import GeoJSONLayer from '@arcgis/core/layers/GeoJSONLayer'

import { useMapStore } from '@/store/mapStore'
import { markRaw } from 'vue'
export function useUpload() {
  const layerStore = useMapStore()
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

  async function handleFileUpload(file) {
    const name = file.name.toLowerCase()
    const uploadResult = await uploadFileToServer(file);
    if (name.endsWith('.geojson')) {
      const url = URL.createObjectURL(file)
      console.log(url)
      const layer = new GeoJSONLayer({ url, title: file.name, visible: true })
      layerStore.addLayer({
        id: file.name,
        title: file.name,
        visible: true,
        opacity: 1,
        type: 'vector',
        instance: markRaw(layer)
      })

      } else {
      alert('仅支持 .geojson文件')
    }
  }
  return { handleFileUpload }
}
