<script setup>
  import {ref, reactive, onMounted, computed } from 'vue';
  import pair_trade from '@/components/form/pair_trade.vue';
  import pair_details from '@/components/charts/pair_details.vue';
  import { useRoute } from 'vue-router'
  import { usePairForm } from '@/stores/pairs';

  const route = useRoute();
  const store = usePairForm();
  const isDataLoaded = ref(false);

  const pair = computed( () => {
    return route.params.pair;
  })

  onMounted( async () => {
    await store.load();
    isDataLoaded.value = true;
  })

</script>

<template>
  <div class="card m-3">
    <div class="card-header">
      <h3>Title</h3>
    </div>
    <div class="card-body" v-if="isDataLoaded">
      <div class="row">
        <div class="col chart_col">
          <pair_details/>
        </div>
        <div class="col trade_col">
          <pair_trade/>
        </div>    
      </div>
    </div>
  </div>
</template>

<style>
  .compare_page {
    min-width: 1902px;
  }
  .trade_col {
    max-width: 30%;
  }
  .chart_col {
    max-width: 70%;
  }
</style>