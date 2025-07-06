<!-- src/components/ChatBox.vue -->
<template>
  <v-card class="chat-card rounded-xl d-flex flex-column pa-4" elevation="2">
    <!-- 消息展示区域 -->
    <div class="chat-messages flex-grow-1 overflow-y-auto mb-2">
      <div
        v-for="(msg, index) in mockMessages"
        :key="index"
        class="my-2"
      >
        <strong>{{ msg.sender }}:</strong> {{ msg.text }}
      </div>
    </div>

    <!-- 底部输入区域 -->
    <div class="chat-input-row d-flex align-center">
      <!-- 加号按钮 -->
      <v-btn icon class="rounded-circle mr-2" variant="tonal" size="small">
        <v-icon icon="mdi-plus"></v-icon>
      </v-btn>

      <!-- 输入框 -->
      <v-text-field
        variant="outlined"
        placeholder="请输入内容..."
        hide-details
        density="compact"
        class="rounded-pill flex-grow-1"
        rounded
        bg-color="#f5f5f5"
        v-model="input"
      />
      <!-- 发送按钮 -->
      <v-btn icon class="rounded-circle ml-2" variant="tonal" size="small">
        <v-icon icon="mdi-send">mdi-send</v-icon>
      </v-btn>
    </div>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'

const input = ref('')
const mockMessages = ref([
  { sender: '系统', text: '您好，请输入您的请求' },
  { sender: '用户', text: '帮我生成缓冲区' }
])
</script>

<style scoped>
.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 20px;
  overflow: hidden;
}

.chat-input-row {
  padding-top: 8px;
  border-top: 1px solid #eee;
}

.rounded-pill {
  border-radius: 999px !important;
}
</style>
