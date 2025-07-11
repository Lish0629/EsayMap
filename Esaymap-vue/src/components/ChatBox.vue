<template>
  <v-card class="chat-card rounded-xl d-flex flex-column pa-4" elevation="2">
    <!-- 聊天记录区域 -->
    <div ref="scrollContainer" class="chat-messages flex-grow-1 overflow-y-auto pr-1">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-bubble', msg.role === 'system' ? 'left-bubble' : 'right-bubble']"
      >
        {{ msg.text }}
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
      />

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
      />

      <!-- 发送按钮 -->
      <v-btn icon class="rounded-circle ml-2" variant="tonal" size="small" @click="sendMessage">
        <v-icon>mdi-send</v-icon>
      </v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useUpload } from '@/utils/useUpload'

const input = ref('')
const messages = ref([
  {
    role: 'system',
    text: '你好，欢迎使用EsayMap文言易图！'
  }
])

const scrollContainer = ref(null)
const fileInput = ref(null)
const { handleFileUpload } = useUpload()

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

const sendMessage = () => {
  if (!input.value.trim()) return
  messages.value.push({
    role: 'user',
    text: input.value.trim()
  })
  input.value = ''
  scrollToBottom()
}

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

.left-bubble {
  max-width: 85%;
  padding: 10px 14px;
  margin: 8px 0;
  background-color: #b0bed9;
  color: #333;
  align-self: flex-start;
  border-radius: 0px 16px 16px 16px;
  word-break: break-word;
  white-space: pre-wrap;
}

.right-bubble {
  max-width: 85%;
  padding: 10px 14px;
  margin: 8px 0;
  background-color: #394b63;
  color: #fff;
  align-self: flex-end;
  border-radius: 16px 0px 16px 16px;
  word-break: break-word;
  white-space: pre-wrap;
}

.chat-input-row {
  border-top: 1px solid #eee;
  padding-top: 10px;
}

.rounded-pill {
  border-radius: 999px !important;
}
</style>