<script setup lang="ts">
import { Synset } from '../model/Synset';
import { posToString } from '../model/POS';

const synset = defineModel<Synset>({ required: false});

</script>

<template>
  <div class="synset-editor">
    <template v-if="synset != null">
      <div class="header">
        <h2 class="synset-header">{{ synset.synset_id.split('.')[0] }}</h2>
        <i> {{ ' ' + posToString(synset.pos) 
              + ' ' + synset.synset_id.split('.')[2] }}</i>
      </div>
      
      <div>
        <i>"{{ synset.definition.definition_text }}"</i>
      </div>

      <div v-if="synset.definition.decomposition != null && Object.keys(synset.definition.decomposition).length > 0">
        <span>Disambiguation:</span>
        <ul >
          <li v-for="synset_id in synset.definition.decomposition">
            {{ synset_id }}
          </li>
        </ul>
      </div>
    </template>
    <template v-else>
      <p>Select a node on the right to view the details of the corresponding word.</p>
    </template>
  </div>
</template>

<style lang="css" scoped>

.synset-editor {
  border: 1px solid #d1d5db;
  border-radius: 12px;
  padding: 8px;
  gap: 8px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 4px;
}

.synset-header {
  margin: 0;
}

</style>