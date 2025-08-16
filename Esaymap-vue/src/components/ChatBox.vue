<template>
  <v-card class="chat-card rounded-xl d-flex flex-column pa-4" elevation="2">
    <!-- 聊天记录区域 -->
    <div ref="scrollContainer" class="chat-messages flex-grow-1 overflow-y-auto pr-1">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-bubble', msg.role === 'system' || msg.role === 'bot' ? 'left-bubble' : 'right-bubble']"
      >
        {{ msg.text }}
        <!-- 如果有错误信息，也显示出来 -->
        <div v-if="msg.error" class="error-details mt-1">
          <strong>错误详情:</strong> {{ msg.error }}
        </div>
        <!-- 如果有数据（例如 GeoJSON 结果），可以考虑在这里渲染或提供下载链接 -->
        <!-- <pre v-if="msg.data">{{ JSON.stringify(msg.data, null, 2) }}</pre> -->
      </div>
      <!-- 显示加载指示器 -->
      <div v-if="isLoading" class="message-bubble left-bubble">
        <v-progress-circular indeterminate size="20" width="2"></v-progress-circular>
        处理中...
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input-row d-flex align-center mt-2">
      <!-- 上传按钮 -->
      <v-btn
        icon
        class="rounded-circle mr-2"
        variant="tonal"
        size="small"
        @click="triggerFileInput"
        :disabled="isLoading" 
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>

      <!-- 隐藏文件上传输入框 -->
      <input
        ref="fileInput"
        type="file"
        accept=".geojson,.zip,.csv"
        style="display: none"
        @change="onFileChange"
        :disabled="isLoading" 
      ></input>

      <!-- 文本输入框 -->
      <v-text-field
        v-model="input"
        variant="outlined"
        placeholder="请输入内容..."
        hide-details
        density="compact"
        class="rounded-pill flex-grow-1"
        bg-color="#f5f5f5"
        @keydown.enter="sendMessage"
        :disabled="isLoading" 
        :loading="isLoading" 
      />

      <!-- 发送按钮 -->
      <v-btn
        icon
        class="rounded-circle ml-2"
        variant="tonal"
        size="small"
        @click="sendMessage"
        :disabled="isLoading || !input.trim()" 
        :loading="isLoading" 
      >
        <v-icon v-if="!isLoading">mdi-send</v-icon>
        <!-- loading 为 true 时，v-btn 会自动显示 spinner -->
      </v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref, onMounted, nextTick,markRaw } from 'vue'
import { useUpload } from '@/utils/useUpload'
import Graphic from '@arcgis/core/Graphic'

import FeatureLayer from '@arcgis/core/layers/FeatureLayer';
import { useMapStore } from '@/store/mapStore'; 
import { useChatStore } from '@/store/chatStore'
import { arcgisToGeoJSON } from '@esri/arcgis-to-geojson-utils';
import { toGeoJson } from '@/utils/toGeoJson'
const mapStore = useMapStore();
const chatStore = useChatStore();
const input = ref('')

const isLoading = ref(false)
const messages = chatStore.messages // 引用 Store 中的 messages

const scrollContainer = ref(null)
const fileInput = ref(null)
const { handleFileUpload,uploadGeoJsonAsFile } = useUpload()

// --- 后端 API 地址 ---
// 请根据您的 FastAPI 服务实际运行地址修改
const API_BASE_URL = 'http://127.0.0.1:8000'

function triggerFileInput() {
  fileInput.value.click()
}

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    handleFileUpload(file)
    chatStore.addMessage({ role: 'system', text:  `已成功上传图层：${file.name}`})
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
    }
  })
}

// --- 修改：sendMessage 函数 ---
const sendMessage = async () => {
  const userMessage = input.value.trim() // 从 Store 的 ref 获取值
  if (!userMessage || isLoading.value) return;

  chatStore.addMessage({ role: 'user', text: userMessage })

  isLoading.value = true;
  input.value = '';
  scrollToBottom();

  try {
    const response = await fetch(`${API_BASE_URL}/process-request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: userMessage })
    });

    const data = await response.json();

    if (data.success) {
      // --- 处理后端返回的数据 ---
      let botMessage = {
        role: 'bot',
        text: data.message || '操作成功完成。'
      };

      if (data.data) {
        console.log('data.data:', data);
        // 1. 检查是否是几何数据 (ArcGIS JSON)
        // ArcGIS Server Geometry Service 通常返回 { geometries: [...] }
        if (data.data.geometries && Array.isArray(data.data.geometries)) {
          try {
            // 调用处理 ArcGIS JSON 几何的函数
            await handleArcGISGeometryResult(data.data, userMessage);
            botMessage.text += " 结果已添加到地图。";
          } catch (layerError) {
            console.error("添加图层时出错:", layerError);
            botMessage.text += ` 结果已生成，但添加到地图时出错: ${layerError.message}\n${data.llm_raw_response.replace(/\{.*?\}/g, '')}`;
            botMessage.error = layerError.message;
          }
        }
        // 2. 检查是否是数值结果 (例如 areasAndLengths)
        else if (data.data.lengths || data.data.areas) {
          let resultText = "\n计算结果:";
          if (data.data.lengths) {
            // lengths 通常是数字数组
            const lengthsStr = data.data.lengths.map(l => l.toFixed(2)).join(', ');
            resultText += `\n长度: [${lengthsStr}]`;
          }
          if (data.data.areas) {
            // areas 通常是数字数组
            const areasStr = data.data.areas.map(a => a.toFixed(2)).join(', ');
            resultText += `\n面积: [${areasStr}]`;
          }
          botMessage.text += resultText;
        }
        // 3. 其他类型的数据或无法识别的数据
        else {
          console.warn("收到未知格式的响应数据:", data.data);
          // 可以选择显示原始 JSON（调试用）
          botMessage.text += `\n${data.llm_raw_response.replace(/\{.*?\}/g, '')}`;
          botMessage.text += " (收到数据，但格式未知)";
        }
      } else {
          console.log("操作成功，但无额外数据返回。");
      }

      chatStore.addMessage(botMessage)
      // --- 结束处理 ---
    } else {
      chatStore.addMessage({
        role: 'bot',
        text: data.message || '处理请求时发生错误。',
        error: data.error || '未知错误'
      });
    }
  } catch (error) {
    console.error("调用后端 API 时出错:", error);
    chatStore.addMessage({
      role: 'bot',
      text: '无法连接到服务器或处理响应。',
      error: error.message || '网络错误'
    })
  } finally {

    input.value = ''
    isLoading.value = false;
    scrollToBottom();
  }
};
/**
 * 处理后端返回的 ArcGIS JSON 几何数据并将其作为新图层添加到地图
 * @param {Object} arcgisResultData 后端返回的 ArcGIS JSON 对象，例如 { geometries: [...], geometryType: "...", ... }
 * @param {string} userQuery 用户的原始查询，用于生成图层标题
 */
 async function handleArcGISGeometryResult(arcgisResultData, userQuery) {
  
  const geometries = arcgisResultData.geometries;
  const geometryType = arcgisResultData.geometryType;
  console.log("处理 ArcGIS JSON 响应数据:", arcgisResultData);
  if (!geometries || !Array.isArray(geometries) || geometries.length === 0) {
      console.warn("ArcGIS 几何数据为空或格式不正确:", arcgisResultData);
      throw new Error("无效的 ArcGIS 几何数据");
  }
  console.log(geometries)
  const arcgisToGeojson=toGeoJson(arcgisResultData)
  console.log("转换后的 GeoJSON:", arcgisToGeojson);
  const namePart = `Result${userQuery.substring(0, 20)}`
  .replace(/[\u4e00-\u9fa5]/g, '')  // 删除所有中文字符
  .replace(/[^a-zA-Z0-9]/g, '');    // 删除所有符号，只保留字母和数字

// 再添加扩展名
  const fileName = `${namePart}.geojson`;


  const result = await uploadGeoJsonAsFile(arcgisToGeojson, fileName);
  if (result.success) {
    console.log('上传成功:', result)
  } else {
    console.log('上传失败')
  }
  const graphics = geometries.map(geomData => {
    return Graphic.fromJSON({
      geometry: geomData,
      // symbol: { ... },
      // attributes: { id: i, ... }
    });
  })
  const featureLayer=new FeatureLayer({
    title: `Result-${userQuery.substring(0, 10)}...`,
    source:graphics,
    objectIdField: "Id", 
        fields: [
          { name: "Id", type: "oid" },
          { name: "Name", type: "string" }
        ]
  });
  if (graphics.length > 0) {
      // 3. 将 GraphicsLayer 添加到地图 Store
      mapStore.addLayer({
        id: `result_${Date.now()}`, // 生成唯一 ID
        title: featureLayer.title,
        visible: true,
        opacity: 1,
        type: 'graphics', // 定义一个类型，与你的 Store 逻辑匹配
        instance: markRaw(featureLayer) // 使用 markRaw 包装 ArcGIS 对象
      });
      console.log(`成功添加包含 ${graphics.length} 个要素的结果图层`);
  } else {
      console.warn("没有有效的要素可以添加到结果图层。");
      throw new Error("几何数据转换失败，无法创建图层要素。");
  }
};
onMounted(scrollToBottom)
</script>

<style scoped>
.chat-card {
  height: calc(100% - 8px);
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  background-color: white;
  margin: 6px -3px -2px 4px !important;
}

.chat-messages {
  max-height: 100%;
  padding-bottom: 10px;
  display: flex;
  flex-direction: column;
}

.message-bubble {
  max-width: 85%;
  padding: 10px 14px;
  margin: 8px 0;
  /* background-color will be set by class */
  color: #333; /* Default text color */
  align-self: flex-start; /* Default alignment */
  border-radius: 16px; /* Default radius, overridden by specific classes */
  word-break: break-word;
  white-space: pre-wrap;
}

.left-bubble { /* Bot/System messages */
  background-color: #b0bed9;
  color: #333;
  align-self: flex-start;
  border-radius: 0px 16px 16px 16px; /* Tail on the left */
}

.right-bubble { /* User messages */
  background-color: #394b63;
  color: #fff;
  align-self: flex-end;
  border-radius: 16px 0px 16px 16px; /* Tail on the right */
}

.error-details {
  font-size: 0.85em;
  opacity: 0.9;
}

.chat-input-row {
  border-top: 1px solid #eee;
  padding-top: 10px;
}

.rounded-pill {
  border-radius: 999px !important;
}
</style>