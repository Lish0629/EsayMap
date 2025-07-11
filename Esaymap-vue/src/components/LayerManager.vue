<script setup>
import { ref } from 'vue'

import LayerWrapper from './layers/LayerWrapper.vue'
import { useMapStore } from '@/store/mapStore'
const layerStore = useMapStore ()



const expanded = ref({})

function toggleExpand(id) {
  expanded.value[id] = !expanded.value[id]
}

function toggleVisible(layer) {
  layerStore.updateVisibility(layer.id, !layer.visible)
}
</script>

<template>
  <div class="pa-4">
    <v-list density="compact" class="bg-white">
      <div v-for="layer in layerStore.layers" :key="layer.id" class="list-item">
        <v-list-item class="d-flex align-center justify-space-between">
          <template #prepend>
            <v-btn
              @click.stop="toggleVisible(layer)"
              icon
              flat
              plain
              :ripple="false"
              class="no-effect"
            >
              <v-icon>{{ layer.visible ? 'mdi-eye' : 'mdi-eye-off' }}</v-icon>
            </v-btn>

          </template>

          <v-list-item-title class="text-subtitle-1">
            {{ layer.title }}
          </v-list-item-title>

          <template #append>
            <v-btn
              icon
              variant="text"
              @click.stop="toggleExpand(layer.id)"
            >
              <v-icon>{{ expanded[layer.id] ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </template>
        </v-list-item>

        <v-expand-transition>
          <div v-if="expanded[layer.id]">
            <LayerWrapper :layer="layer" />
          </div>
        </v-expand-transition>
      </div>
    </v-list>
  </div>
</template>

<style scoped>
.v-list {
  max-height: 80vh;
  overflow-y: auto;
}
.list-item {
  border: 2px solid rgba(0, 0, 0, 0.2);
  margin-top: 6px;
  border-radius: 36px;
  /*box-shadow: 0px 2px 1px -1px var(--v-shadow-key-umbra-opacity, rgba(0, 0, 0, 0.2)), 0px 1px 1px 0px var(--v-shadow-key-penumbra-opacity, rgba(0, 0, 0, 0.14)), 0px 1px 3px 0px var(--v-shadow-key-ambient-opacity, rgba(0, 0, 0, 0.12));
*/
}
.v-btn--variant-elevated{
 box-shadow: none;
}
.no-effect {
  box-shadow: none !important;
  background-color: transparent !important;
}

.no-effect:hover {
  background-color: white !important;
}

.no-effect::before {
  display: none !important; /* 取消点击涟漪效果 */
  background: none !important;
}

</style>
