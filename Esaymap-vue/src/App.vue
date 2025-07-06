<!-- src/App.vue -->
<template>
  <v-app>
    <!-- 可选顶部导航栏 -->
    <v-app-bar flat color="white" class="rounded-xl mx-2 mt-2" elevation="2">
      <v-toolbar-title class="text-h6">🗺️ EsayMap WebGIS 系统</v-toolbar-title>
    </v-app-bar>

    <!-- 主体内容区域 -->
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
// 无需其他脚本，逻辑由 router-view 动态渲染
</script>

<style>
html,
body,
#app {
  height: 100%;

  background-color: #f5f7fa; /* 柔和背景色 */
  font-family: 'Roboto', sans-serif;
}

.v-application {
  border-radius: 16px;
  overflow: hidden;
}
.v-main{
  padding: 2px;
  
}
</style>
