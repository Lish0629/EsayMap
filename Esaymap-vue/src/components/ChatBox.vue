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
import GraphicsLayer from '@arcgis/core/layers/GraphicsLayer';
import { useMapStore } from '@/store/mapStore'; // 确保正确导入了你的地图 Store

const input = ref('')
const messages = ref([
  {
    role: 'system', // 使用 'system' 或 'bot' 来区分系统/机器人消息
    text: '你好，欢迎使用EsayMap文言易图！'
  }
])

const scrollContainer = ref(null)
const fileInput = ref(null)
const { handleFileUpload } = useUpload()

// --- 新增：加载状态 ---
const isLoading = ref(false)

// --- 新增：后端 API 地址 ---
// 请根据您的 FastAPI 服务实际运行地址修改
const API_BASE_URL = 'http://127.0.0.1:8000'

function triggerFileInput() {
  fileInput.value.click()
}

function onFileChange(e) {
  const file = e.target.files[0]
  if (file) {
    handleFileUpload(file)

    // 自动生成系统回复消息
    messages.value.push({
      role: 'system',
      text: `已成功上传图层：${file.name}`
    })
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
  const userMessage = input.value.trim()
  if (!userMessage || isLoading.value) return // 防止重复提交和空消息

  // 1. 将用户消息添加到聊天记录
  messages.value.push({
    role: 'user',
    text: userMessage
  })
  input.value = '' // 清空输入框

  // 2. 设置加载状态
  isLoading.value = true
  scrollToBottom() // 滚动到底部显示 "处理中..."

  try {
    // 3. 向后端发送 POST 请求
    const response = await fetch(`${API_BASE_URL}/process-request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ query: userMessage }) // 按照后端 schemas.requests.ProcessRequest 的结构发送
    });

    // 4. 处理响应
    const data = await response.json();

    if (data.success) {
      // 请求成功
      messages.value.push({
        role: 'bot', // 或 'system'
        text: data.message || '操作成功完成。', // 显示后端返回的成功消息
        data: data.data // 可能包含 ArcGIS 的结果数据
        // 可以在这里进一步处理 data.data，例如提取几何信息用于地图渲染
      });
      console.log("后端返回的数据:", data.data);
    } else {
      // 请求失败（后端处理出错）
      messages.value.push({
        role: 'bot', // 或 'system'
        text: data.message || '处理请求时发生错误。',
        error: data.error || '未知错误' // 显示后端返回的错误详情
      });
    }
  } catch (error) {
    // 5. 处理网络错误或解析错误
    console.error("调用后端 API 时出错:", error);
    messages.value.push({
      role: 'bot', // 或 'system'
      text: '无法连接到服务器或处理响应。',
      error: error.message || '网络错误'
    });
  } finally {
    // 6. 重置加载状态
    isLoading.value = false;
    scrollToBottom(); // 滚动到底部显示响应或错误
  }
}
// --- 结束修改 ---

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