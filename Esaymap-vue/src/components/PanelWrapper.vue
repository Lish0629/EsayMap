<template>
  <v-card class="d-flex flex-column h-100 rounded-xl pa-2" elevation="2">
    <!-- 当前面板主体 -->
    <div class="flex-grow-1 overflow-y-auto pr-2">
      <ChatBox v-if="activePanel === 'chat'" />
      <LayerManager v-else />
    </div>

    <!-- 面板切换按钮 -->
    <div class="d-flex justify-center pt-2">
      <v-btn-toggle v-model="activePanel" mandatory class="rounded-pill">
        <v-btn value="chat" variant="tonal">Chat</v-btn>
        <v-btn value="layer" variant="tonal">图层管理</v-btn>
      </v-btn-toggle>
    </div>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import ChatBox from './ChatBox.vue'
import LayerManager from './LayerManager.vue'

const activePanel = ref('chat') // 默认显示 ChatBox
</script>

<style scoped>

</style>
