<script setup lang="ts">
import { ref, Ref } from 'vue'

import { Synset } from './model/Synset'
import { DefaultVisualizationOptions, VisualizationOptions } from './model/VisualizationOptions'

import VisualizationControls from './components/VisualizationControls.vue'
import SynsetEditor from './components/SynsetEditor.vue'
import DependencyChart from './components/DependencyChart.vue'

const options: Ref<VisualizationOptions> = ref(DefaultVisualizationOptions);
let selectedSynset: Ref<Synset | undefined> = ref();

</script>

<template>
  <main class="page">
    <h1>Word Decomposition Visualization Tool</h1>
    <div class="body">
      <div class="side-panel">
        <visualization-controls v-model="options" />
        <synset-editor v-model="selectedSynset" />
      </div>
      <dependency-chart v-model:selected-synset="selectedSynset" v-bind:visualization-options="options"/>
    </div>
  </main>
</template>

<style lang="css" scoped>
.body {
  display: flex;
  gap: 8px;
}

.side-panel {
  display: flex;
  flex-direction: column;
  width: 20%;
  gap: 8px;
}
</style>