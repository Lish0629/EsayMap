<template>
  <v-container fluid class="home-container pa-2">
    <v-row no-gutters class="fill-remaining-height">
      <!-- 左侧地图，占8/12宽 -->
      <v-col cols="9" class="pa-2 fill-height">
        <MapView />
      </v-col>

      <!-- 右侧对话框，占4/12宽 -->
      <v-col cols="3" class="pa-2 fill-height">
        <PanelWrapper />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import MapView from '@/components/MapView.vue'
import PanelWrapper from '@/components/PanelWrapper.vue'
import { onMounted } from 'vue'

onMounted(() => {

  
});
</script>

<style scoped>
.home-container {
  /*height: calc(100vh - 64px);*/ /* 减去顶部导航栏高度64px（默认v-app-bar高度） */
  height: calc(100vh); /* 减去顶部导航栏高度64px（默认v-app-bar高度） */
  /*max-height: calc(100vh - 64px);*/
  max-height: calc(100vh);
  display: flex;
  flex-direction: column;
  overflow: hidden;

}

/* 让 v-row 填满剩余高度 */
.fill-remaining-height {
  height: 100%;
  max-height: 100%;
  overflow: hidden;
  display: flex;
}

/* 让左右两列撑满高度 */
.fill-height {
  height: 100%;
  max-height: 100%;
  overflow: hidden;
}
</style>
