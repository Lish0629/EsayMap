<template>
  <v-container fluid class="home-container pa-2">
    <v-row no-gutters class="fill-remaining-height">
      <!-- 左侧地图，占8/12宽 -->
      <v-col cols="8" class="pa-2 fill-height">
        <MapView />
      </v-col>

      <!-- 右侧对话框，占4/12宽 -->
      <v-col cols="4" class="pa-2 fill-height">
        <PanelWrapper />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import MapView from '@/components/MapView.vue'
import PanelWrapper from '@/components/PanelWrapper.vue'

import { arcgisToGeoJSON, geojsonToArcGIS } from '@esri/arcgis-to-geojson-utils';
import { toGeoJson } from '@/utils/toGeoJson';
import { onMounted } from 'vue'

onMounted(() => {
  // 模拟 ArcGIS 数据
  const json1 = {
    "geometries": [
      { "rings": [[[0.0063060740000651094, -0.14540592099996275], [5.6843418860808015e-14, -0.14554444699996338], [0.0063060740000651094, -0.14540592099996275]]] }
      //,{ "rings": [[[20.006702008000047, 19.854763529000024], [20.000000000000057, 19.854625290000058], [20.006702008000047, 19.854763529000024]]] }
    ]
  };
  const geojson = toGeoJson(json1);
  console.log(geojson);
  
});
</script>

<style scoped>
.home-container {
  height: calc(100vh - 64px); /* 减去顶部导航栏高度64px（默认v-app-bar高度） */
  max-height: calc(100vh - 64px);
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
