<script setup>
  import { ref, watch, onMounted, computed } from 'vue';
  import { usePairForm } from '@/stores/pairs';
  import { useIbkr } from '@/stores/ibkr';
  import LWChart from '@/components/charts/LWChart.vue';
  
  const props = defineProps([
    'pair',
    'data'
  ]);

  const candleSize = ref("1 min");
  const chartLength = ref("1 D")
  const isDataLoaded = ref(false);
  const store = usePairForm();
  const ibkr = useIbkr();
  ibkr.pairStore = store;

  const dataA = ref()
  const dataB = ref()
  const chartData = ref(null)
  const testRatio = ref(1)
  let interval = null;
  
  onMounted( async () => {
    // await ibkr.connect();
  })

  const test = () => {
    console.log("TEST")
    isDataLoaded.value = false

    testRatio.value += 1;
    console.log(testRatio.value)
    chartData.value = accPairPrice()
    isDataLoaded.value = true
  }

  watch(() => props.pair, (newPair) => {
    if (newPair) {
      isDataLoaded.value = false;
      console.log('Changed Pair: ', newPair)
      updatePair(newPair)
    }
  });

  const setCandleSize = (size) => {
    stopInterval()
    candleSize.value = size
    switch(size){
        case "1 day":
          chartLength.value = "1 Y";
          break;
        case "1 min":
          chartLength.value = "1 D";
          break;
        case "15 mins":
          chartLength.value = "15 D";
          break;
        case "1 hour":
          chartLength.value = "90 D";
          break;
        default:
          chartLength.value = "1 D";
          break;
      }

      relaodData()
      //startInterval();

  }

  const relaodData = async () => {
    //const newDataA = await ibkr.getHistoricalData(store.A, candleSize.value, chartLength.value)
    //const newDataB = await ibkr.getHistoricalData(store.B, candleSize.value, chartLength.value)
    //if (newDataA.length > 0){ dataA.value = newDataA };
    //if (newDataB.length > 0){ dataB.value = newDataB };
    ibkr.barSize = candleSize.value
    ibkr.chartLength = chartLength.value
    await ibkr.updatePairData()
    //console.log('data loaded, length: ', newDataA.length, newDataB.length)
    //chartData.value = ibkr.calculatePairPrice()

    //chartData.value = accPairPrice()
    //chartData.value = pairPrice()
    //console.log(dataA.value)
  }

  const updatePair = async (newPair) => {
    isDataLoaded.value = false
    store.pair = newPair;
    await store.load();
    //ibkr.pairInfo[A] = store.A
    //ibkr.pairInfo[B] = store.B
    await relaodData()
    isDataLoaded.value = true;
  }

  const accPairPrice = () => {
    let data = dataA.value.map(obj => ({ ...obj, ticker: store.A })).concat(dataB.value.map(obj => ({ ...obj, ticker: store.B })))
    const hedge_ratio = store.pairs[store.pair]?.hedge_ratio;
    const reverse = store.pairs[store.pair]?.reverse;
    //if (!data.value || !data.value.length) return [];
    console.log('data')
    const result = Object.values(
      data.reduce((acc, { time, close, open, high, low, ticker }) => {
      if (!acc[time]) {
        acc[time] = { time, closeA: null, closeB: null };
      }

      if (ticker === store.A) {
        acc[time].openA = open;
        acc[time].highA = high;
        acc[time].lowA = low;
        acc[time].closeA = close;
      } else if (ticker === store.B) {
        acc[time].openB = open;
        acc[time].highB = high;
        acc[time].lowB = low;
        acc[time].closeB = close;
      }

      if (acc[time].closeA !== null && acc[time].closeB !== null) {
        if (reverse) {
          acc[time].open = acc[time].openB - (acc[time].openA * hedge_ratio);
          acc[time].high = acc[time].highB - (acc[time].highA * hedge_ratio);
          acc[time].low = acc[time].lowB - (acc[time].lowA * hedge_ratio);
          acc[time].close = acc[time].closeB - (acc[time].closeA * hedge_ratio);
        } else {
          acc[time].open = acc[time].openA - (acc[time].openB * hedge_ratio);
          acc[time].high = acc[time].highA - (acc[time].highB * hedge_ratio);
          acc[time].low = acc[time].lowA - (acc[time].lowB * hedge_ratio);
          acc[time].close = acc[time].closeA - (acc[time].closeB * hedge_ratio);
        }
      }

      return acc;
      }, {})
    ).map(
      item => ({
        time: item.time,
        //value: item.close,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
      })
    );
    //return dataA.value;
    return result;
  };

  function startInterval(){
    clearInterval(interval)
    interval = setInterval(() => {
      relaodData();
    }, 5000)
  }

  function stopInterval(){
    clearInterval(interval)
    interval = null
  }

</script>

<template>
  <div>
    <div class="row">
      <div class="col" v-if="isDataLoaded">
        <button @click="setCandleSize('1 day')">1 d</button>
        <button @click="setCandleSize('1 min')">1 m</button>
        <button @click="setCandleSize('15 mins')">15 m</button>
        <button @click="setCandleSize('1 hour')">1 h</button>
        <button @click="stopInterval()">Stop Interval</button>
        <button @click="startInterval()">Start Interval</button>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="card">
          <!-- Candle -->
          <LWChart :A="ibkr.chartData['pairPrice']" :type="'candle'" :watermark="pair" v-if="isDataLoaded"/>

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