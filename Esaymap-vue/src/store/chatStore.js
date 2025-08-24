// src/store/chatStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  // 定义响应式状态
  const messages = ref([
    {
      role: 'system',
      text: '你好，欢迎使用EsayMap文言易图！'
    }
  ])
  const isLoading = ref(false)
  // 保存 input 状态
  const input = ref('') 

  function addMessage(message) {
    messages.value.push(message)
  }

  function clearMessages() {
    messages.value = [
      {
        role: 'system',
        text: '你好，欢迎使用EsayMap文言易图！'
      }
    ]
  }

  function setLoading(status) {
    isLoading.value = status
  }

  // 管理 input 的 action
  function setInput(value) {
    input.value = value
  }

  function clearInput() {
    input.value = ''
  }

  // 返回状态和方法
  return {
    messages,
    isLoading,
    input, 
    setInput,
    clearInput,
    addMessage,
    clearMessages,
    setLoading
  }
})