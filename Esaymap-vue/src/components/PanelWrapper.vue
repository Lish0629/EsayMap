<template>
  <v-card class="d-flex flex-column h-100 rounded-xl pa-2" elevation="2">
    <div class="head-container d-flex align-center justify-space-between px-4">
      <img :src="logoImage" alt="EsayMap Logo" class="logo-image" />
      <div class="d-flex align-center">
        <!-- 打印按钮 -->
        <v-btn
          icon="mdi-printer"
          variant="text"
          size="small"
          class="mx-1"
          @click="handlePrint"
          :loading="isPrinting"
        ></v-btn>
        <!-- 信息按钮 -->
        <v-btn
          icon="mdi-information"
          variant="text"
          size="small"
          class="mx-1"
          @click="isInfoDialogVisible = true"
        ></v-btn>
        <!-- 用户按钮 -->
        <v-btn icon="mdi-account" variant="text" size="small" class="mx-1"></v-btn>
      </div>
    </div>
    <!-- 面板主体 -->
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

  <!-- --- 新增：信息弹窗 --- -->
  <v-dialog v-model="isInfoDialogVisible" max-width="500px">
    <v-card>
      <v-card-title class="text-h5">关于 EsayMap</v-card-title>
      <v-card-text>
        <p><strong>作品名称:</strong> EsayMap - 文言易图</p>
        <p><strong>小组代码:</strong> C1198 </p>
        <p><strong>作者:</strong> 李晟澔 张一弘 吴锐舟 方洋洋</p>
        <p><strong>项目简介:</strong>  </p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="isInfoDialogVisible = false">关闭</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<script setup>
import { ref } from 'vue'
import ChatBox from './ChatBox.vue'
import LayerManager from './LayerManager.vue'
import logoImage from '@/assets/logo.png';
import { useChatStore } from '@/store/chatStore';

import { useMapStore } from '@/store/mapStore';
const activePanel = ref('chat')
const isInfoDialogVisible = ref(false);
const mapStore = useMapStore();
const mapView = mapStore.mapView;
const isPrinting = ref(false);
const chatStore = useChatStore();

// 打印地图
const handlePrint = async () => {
  

  isPrinting.value = true;
  console.log("开始生成地图截图...");

  try {
    const screenshotOptions = {};
    const screenshot = await mapView.takeScreenshot(screenshotOptions);
    console.log("地图截图生成成功。");

    const dataUrl = screenshot.dataUrl;
    const link = document.createElement('a');
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    link.download = `EsayMap_Screenshot_${timestamp}.png`;
    link.href = dataUrl;
    link.style.display = 'none';

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    console.log(`地图截图已下载为: ${link.download}`);
    chatStore.addMessage({ role: 'system', text: `地图已下载为: ${link.download}` });

  } catch (error) {
    console.error("生成或下载地图截图时出错:", error);
    alert(`导出地图失败: ${error.message || '未知错误'}`);
  } finally {
    isPrinting.value = false;
    console.log("截图操作结束。");
  }
};
</script>

<style scoped>
.logo-image {
  height: 68px;
  width: auto;
}
</style>