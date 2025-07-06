<!-- src/components/ChatBox.vue -->
<template>
  <v-card class="pa-4 rounded-xl" elevation="3" height="100%">
    <v-card-title class="text-h6">大模型对话框</v-card-title>
    <v-divider class="my-2" />
    <v-card-text style="flex: 1; overflow-y: auto;">
      <!-- 未来放消息列表 -->
      <div v-for="(msg, index) in messages" :key="index" class="my-2">
        <strong>{{ msg.sender }}:</strong> {{ msg.text }}
      </div>
    </v-card-text>
    <v-text-field
      v-model="input"
      label="输入您的问题"
      variant="outlined"
      class="mt-2 rounded-xl"
      @keydown.enter="send"
    />
  </v-card>
</template>

<script setup>
import { ref } from 'vue'

const input = ref('')
const messages = ref([{ sender: '系统', text: '您好，请提问' }])

function send() {
  if (!input.value.trim()) return
  messages.value.push({ sender: '用户', text: input.value })
  // TODO: 调用大模型 API
  input.value = ''
}
</script>
