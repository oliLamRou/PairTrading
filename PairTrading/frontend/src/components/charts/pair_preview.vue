<script setup>
  import { ref, watch, onMounted, computed } from 'vue';
  import { usePairForm } from '@/stores/pairs';
  import LWChart from '@/components/charts/LWChart.vue';
  
  const props = defineProps([
    'pairProp'
  ]);

  const isDataLoaded = ref(false);
  const pair = ref(props.pairProp)
  const store = usePairForm();
  const data = computed(() => store.pairs[store.pair].data);
  const chartData = computed(() => getPairPrice());
  
  onMounted( async () => {

  })

  watch(() => props.pairProp, (newPair) => {
    if (newPair) {
      isDataLoaded.value = false;
      console.log('Changed Pair: ', newPair)
      updatePair(newPair)
    }
  });

  const updatePair = async (newPair) => {
    store.pair = newPair;
    await store.load();
    console.log("loaded")
    isDataLoaded.value = true;
  }

  const getPairPrice = () => {
    const hedge_ratio = store.pairs[store.pair]?.hedge_ratio;
    const reverse = store.pairs[store.pair]?.reverse;
    if (!data.value || !data.value.length) return [];
    const result = Object.values(
      data.value.reduce((acc, { date, close, open, high, low, ticker }) => {
      if (!acc[date]) {
        acc[date] = { date, closeA: null, closeB: null };
      }

      if (ticker === store.A) {
        acc[date].openA = open;
        acc[date].highA = high;
        acc[date].lowA = low;
        acc[date].closeA = close;
      } else if (ticker === store.B) {
        acc[date].openB = open;
        acc[date].highB = high;
        acc[date].lowB = low;
        acc[date].closeB = close;
      }

      if (acc[date].closeA !== null && acc[date].closeB !== null) {
        if (reverse) {
          acc[date].open = acc[date].openB - (acc[date].openA * hedge_ratio);
          acc[date].high = acc[date].highB - (acc[date].highA * hedge_ratio);
          acc[date].low = acc[date].lowB - (acc[date].lowA * hedge_ratio);
          acc[date].close = acc[date].closeB - (acc[date].closeA * hedge_ratio);
        } else {
          acc[date].open = acc[date].openA - (acc[date].openB * hedge_ratio);
          acc[date].high = acc[date].highA - (acc[date].highB * hedge_ratio);
          acc[date].low = acc[date].lowA - (acc[date].lowB * hedge_ratio);
          acc[date].close = acc[date].closeA - (acc[date].closeB * hedge_ratio);
        }
      }

      return acc;
      }, {})
    ).map(
      item => ({
        time: item.date / 1000,
        value: item.close,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
      })
    );
    return result;
  };

  

</script>

<template>
  <div>
    <div class="row">
      <div class="col">
        <div class="card">
          <!-- Candle -->
          <LWChart :A="getPairPrice()" :type="'candle'" :watermark="store.pair" v-if="isDataLoaded"/>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
  .chart-row {
    min-width: 1000px;
  }
</style>