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
    <div class="d-flex justify-space-between align-center">
  <v-btn
    icon="mdi-download"
    variant="text"
    size="small"
    class="mx-1 custom-btn-margin"
    @click="exportGeoJsonFile"
  ></v-btn>

  <v-btn
    icon="mdi-delete"
    variant="text"
    size="small"
    class="mx-1 custom-btn-margin mr-4"
    color="error"
    @click="dialog = true"
  ></v-btn>
  <v-dialog v-model="dialog" max-width="400">
  <v-card>
    <v-card-title class="text-h6"> 删除图层？ </v-card-title>
    <v-card-text>
      你确定要删除图层 "<strong>{{ layerTitle }}</strong>" 吗？
      <br /><br />
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn variant="text" @click="dialog = false">取消</v-btn>
      <v-btn color="error" variant="flat" @click="onConfirmDelete">确定删除</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
</div>
  </div>
</template>

<script setup>
import { defineProps, onMounted,ref,computed} from 'vue'
import { ColorAdapter } from '@/utils/color';
const props = defineProps({ 
  layer: {
    type: Object,
    required: true
  } 
});
import { useMapStore } from '@/store/mapStore'
import { useChatStore } from '@/store/chatStore'
const chatStore = useChatStore ()
const mapStore = useMapStore ()
const ccolor = ref(ColorAdapter.arrayToObj(props.layer.color))
const dialog = ref(false)
const layerTitle = computed(() => props.layer.title || `图层 ${props.layer.id}`)
const onConfirmDelete = () => {
  console.log("用户确认删除图层:", props.layer.id)
  chatStore.addMessage({
    role: 'system',
    text: `用户确认删除图层 "${layerTitle.value}"（暂未执行真实删除）。`
  })
  // mapStore.removeLayer(props.layer.id)

  // 关闭弹窗
  dialog.value = false
}
// 颜色变化处理
const handleColorUpdate = (colorObj) => {
  const rgbArray = ColorAdapter.objToArray(colorObj)
  mapStore.updateColor(props.layer.id, rgbArray)
}

const exportGeoJsonFile = async() => {
  try {
    // 1. 获取图层的标识符
    // 确保文件名以 .geojson 结尾
    let filename = props.layer.title || props.layer.id;
    if (!filename) {
      throw new Error("图层缺少标题或ID，无法确定文件名。");
    }
    if (!filename.toLowerCase().endsWith('.geojson')) {
      filename += '.geojson';
    }

    const backendBaseUrl = 'http://127.0.0.1:8000';
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

    const blob = await response.blob();

    const downloadUrl = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = filename;
    link.style.display = 'none';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(downloadUrl);

    console.log(`GeoJSON 文件下载成功: ${filename}`);
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