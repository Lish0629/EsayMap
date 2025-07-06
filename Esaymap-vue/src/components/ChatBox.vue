<template>
  <v-card class="chat-card rounded-xl d-flex flex-column pa-4" elevation="2">
    <div ref="scrollContainer" class="chat-messages flex-grow-1 overflow-y-auto pr-1">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="[
          'message-bubble',
          msg.role === 'system' ? 'left-bubble' : 'right-bubble'
        ]"
      >
        {{ msg.text }}
      </div>
    </div>

    <div class="chat-input-row d-flex align-center mt-2">
      <v-btn icon class="rounded-circle mr-2" variant="tonal" size="small">
        <v-icon>mdi-plus</v-icon>
      </v-btn>

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

      <v-btn icon class="rounded-circle ml-2" variant="tonal" size="small" @click="sendMessage">
        <v-icon>mdi-send</v-icon>
      </v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'

const input = ref('')
const messages = ref([  {    role: 'system',    text: '你好，欢迎使用EsayMap文言易图！你好，欢迎使用EsayMap文言易图！你好，欢迎使用EsayMap文言易图！你好，欢迎使用EsayMap文言易图！你好，欢迎使用EsayMap文言易图！你好，欢迎使用EsayMap文言易图！你好，欢迎使用EsayMap文言易图！s'  }])

const scrollContainer = ref(null)

// 自动滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (scrollContainer.value) {
      scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
    }
  })
}

// 发送消息函数（模拟用户）
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
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
  background-color: white;
}

.chat-messages {
  max-height: 100%;
  padding-bottom: 10px;
  display: flex;
  flex-direction: column;
  /* 确保这里没有 justify-content: stretch 或 align-items: stretch，它们会拉伸子元素 */
  /* 如果你的气泡还是占据整个宽度，尝试明确设置 align-items: flex-start; 或 align-items: flex-end; */
}

/* 系统消息左侧圆角框 */
.left-bubble {
  /* 这里的关键是：在 flex 容器中（flex-direction: column），子元素默认宽度是自适应内容的，
     除非有其他属性如 flex-grow 或 align-items: stretch 干扰。
     你已经有了 max-width，这就很好地限制了最大宽度。
  */
  max-width: 85%; /* 限制最大宽度 */
  padding: 10px 14px;
  margin: 8px 0;
  background-color: #b0bed9;
  color: #333;
  align-self: flex-start; /* 将气泡自身对齐到左侧 */
  border-radius: 0px 16px 16px 16px;
  word-break: break-word;
  white-space: pre-wrap;
}

/* 用户消息右侧圆角框 */
.right-bubble {
  /* 同理，宽度会自适应内容 */
  max-width: 85%; /* 限制最大宽度 */
  padding: 10px 14px;
  margin: 8px 0;
  background-color: #394b63;
  color: #fff;
  align-self: flex-end; /* 将气泡自身对齐到右侧 */
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