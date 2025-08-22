<template>
  <div class="pl-6 pr-2 pt-2">
    <v-text-field
      v-model="layer.title"
      label="图层名称"
      density="compact"
      @change="mapStore.updateTitle(layer.id, layer.title)"
    />
    <v-slider
      v-model="layer.opacity"
      min="0"
      max="1"
      step="0.01"
      label="透明度"
      class="mt-2"
      @update:modelValue="mapStore.updateOpacity(layer.id,$event)"
    />
    <div class="mt-3 mb-2 d-flex justify-center align-center">
      <v-color-picker 
        
        v-model="ccolor"
        mode="rgb"
        size="small"
        hide-canvas hide-inputs
        hide-mode-btn
        class="custom-color-picker"
        @update:modelValue="handleColorUpdate"
      />
    </div>
    <v-btn
      icon="mdi-download"
      variant="text"
      size="small"
      class="mx-1 custom-btn-margin"
      @click="exportGeoJsonFile"
    >
    </v-btn>
  </div>
</template>

<script setup>
import { defineProps, onMounted,ref} from 'vue'
import { ColorAdapter } from '@/utils/color';
const props = defineProps({ 
  layer: {
    type: Object,
    required: true // 明确声明 layer 是必需的 prop
  } 
});
import { useMapStore } from '@/store/mapStore'
import { useChatStore } from '@/store/chatStore'
const chatStore = useChatStore ()
const mapStore = useMapStore ()
const ccolor = ref(ColorAdapter.arrayToObj(props.layer.color))
// 颜色变化处理
const handleColorUpdate = (colorObj) => {
  const rgbArray = ColorAdapter.objToArray(colorObj)
  mapStore.updateColor(props.layer.id, rgbArray)
}

const exportGeoJsonFile = async() => {
  try {
    // 1. 获取图层的标识符（假设使用 title，您也可以用 id）
    // 确保文件名以 .geojson 结尾
    let filename = props.layer.title || props.layer.id;
    if (!filename) {
      throw new Error("图层缺少标题或ID，无法确定文件名。");
    }
    if (!filename.toLowerCase().endsWith('.geojson')) {
      filename += '.geojson';
    }

    const backendBaseUrl = 'http://127.0.0.1:8000'; // 替换为您的 FastAPI 地址
    const fileUrl = `${backendBaseUrl}/data/${encodeURIComponent(filename)}`;

    console.log(`准备下载 GeoJSON 文件: ${fileUrl}`);

    const response = await fetch(fileUrl);
    
    // 2. 检查响应是否成功
    if (!response.ok) {
      // 尝试读取错误信息
      let errorMsg = `HTTP error! status: ${response.status}`;
      try {
        const errorText = await response.text();
        errorMsg += ` - ${errorText.substring(0, 200)}...`; // 限制错误信息长度
      } catch (e) {
        // 忽略读取错误信息时的错误
      }
      throw new Error(errorMsg);
    }

    // 3. 获取响应的 Blob 对象
    const blob = await response.blob();

    // 4. 创建一个指向该 Blob 的 URL
    const downloadUrl = URL.createObjectURL(blob);

    // 5. 创建一个临时的 <a> 元素用于下载
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename; // 指定下载的文件名
    link.style.display = 'none'; // 隐藏链接

    // 6. 将链接添加到 DOM，触发点击，然后清理
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // 7. 释放之前创建的 Object URL，节省内存
    URL.revokeObjectURL(downloadUrl);

    console.log(`GeoJSON 文件下载成功: ${filename}`);
    // 可选：在聊天记录或 UI 中通知用户
    chatStore.addMessage({ role: 'system', text: `图层 "${props.layer.title}" 的 GeoJSON 文件已开始下载。` });

  } catch (error) {
    console.error("触发 GeoJSON 文件下载时出错:", error);
    alert(`导出失败: ${error.message}`);
  }
}

onMounted(()=>{
  console.log(ColorAdapter.arrayToObj(props.layer.color))
})
</script>
<style scoped>
.custom-btn-margin {
  margin-top: 0px !important;
  margin-bottom: 6px !important;
}
.custom-color-picker {
  width: 95% !important;
  
  height: 68px;
}
</style>