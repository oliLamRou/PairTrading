<script setup>
  import { ref, onMounted, onUnmounted, watch, defineProps, computed, reactive } from 'vue';
  import { Indicators, IndicatorStyle } from '@/utils/indicators.js'

  import { createChart, LineStyle, LineType, CrosshairMode} from 'lightweight-charts';

  const props = defineProps({
    // data: {
    //   type: Object,
    //   required: true,
    // },
    A: {
      type: Array,
      required: true,
    },
    B: {
      type: Array
    },    
    type: {
      type: String,
      default: 'line',
    },
  });

  let chart;
  let seriesA;
  let seriesB;
  const chartContainer = ref();
  const userInput = reactive({
    normalize: false,
    scale: 1,
    offset: 0,
  });

  const resizeHandler = () => {
    if (!chart || !chartContainer.value) return;
    const dimensions = chartContainer.value.getBoundingClientRect();
    chart.resize(dimensions.width, dimensions.height);
  };

  onUnmounted(() => {
    if (chart) {
      chart.remove();
      chart = null;
    }
    if (seriesA) {
      seriesA = null;
    }
    if (seriesB) {
      seriesB = null;
    }
    window.removeEventListener('resize', resizeHandler);
  });  

  onMounted(() => {
    chart = createChart(chartContainer.value, { width: 400, height: 400});
    chart.applyOptions({
      crosshair: {
        mode: CrosshairMode.Normal, // Keep crosshair in normal mode
      },
    });

    
    if (props.type === 'candle') {
      seriesA = chart.addCandlestickSeries()
      addSMA()
      addBB()
      addVWAP();
      addTripleEMA();
    } else {
      seriesA = chart.addLineSeries();
      if (props.B) {
        seriesB = chart.addLineSeries({ color: 'rgb(225, 87, 90)' });
      }
    }
    
    seriesA.setData(props.A);
    if (seriesB) {
      seriesB.setData(props.B);
    }
    
    window.addEventListener('resize', resizeHandler);
    resizeHandler(); // Initial resize to fit the container
  });

  watch(
    () => [props, userInput],
    newData => {
      if (seriesA) {
          seriesA.setData(computed_A.value)
          addSMA()
          addBB()
          addVWAP();
          addTripleEMA();
      };
      if (seriesB) {
          seriesB.setData(computed_B.value);
      }
    },
    { deep: true }
  );

  const computed_A = computed( ()=> {
    if (userInput.normalize) {
      return normalizeIt(props.A)
    }
    return props.A
  })

  const computed_B = computed( ()=> {
    if (userInput.normalize) {
      return normalizeIt(props.B)
    }
    if (userInput.scale === "" || userInput.scale === 0) { 
      return props.B
    }
    return scaleOffsetIt(props.B)    
  })  

  function scaleOffsetIt(data) {
    const data_ = structuredClone(data)
    data_.forEach((row, index) => {
        data_[index].value = (row.value * userInput.scale) + userInput.offset
    })

    return data_
  }

  function normalizeIt(data) {
    const data_ = structuredClone(data)
    const value = data_.map(item => item.value);
    const min = Math.min(...value);
    const max = Math.max(...value);
    data_.forEach((row, index) => {
      data_[index].value = (row.value - min) / (max - min);
    })

    return data_
  }

  function triggerNormalize() {
    userInput.normalize = !userInput.normalize
  }

  const addSMA = () => {
    const sma = Indicators.LW_SMA({period: 30, values: computed_A.value})
    let smaA = chart.addLineSeries(IndicatorStyle.SMA);
    smaA.setData(sma)
  }

  const addVWAP = () => {
    const vwap = Indicators.LW_VWAP({values: computed_A.value})
    let vwapA = chart.addLineSeries(IndicatorStyle.VWAP);
    vwapA.setData(vwap)
  }

  const addBB = () => {
    const bbands = Indicators.LW_BollingerBands({period: 18, values: computed_A.value, stdDev: 2})
    let bbUpper = chart.addLineSeries(IndicatorStyle.BollingerBands.upper);
    let bbLower = chart.addLineSeries(IndicatorStyle.BollingerBands.lower);
    let bbMiddle = chart.addLineSeries(IndicatorStyle.BollingerBands.middle);
    
    bbUpper.setData(bbands.upper)
    bbMiddle.setData(bbands.middle)
    bbLower.setData(bbands.lower)
  }

  const addTripleEMA = () => {
    const tripleEMA = Indicators.LW_TripleEMA({first: 10, second: 50, third: 200, values: computed_A.value})
    let firstEMA = chart.addLineSeries(IndicatorStyle.TripleEMA.first);
    let secondEMA = chart.addLineSeries(IndicatorStyle.TripleEMA.second);
    let thirdEMA = chart.addLineSeries(IndicatorStyle.TripleEMA.third);
    
    firstEMA.setData(tripleEMA.first)
    secondEMA.setData(tripleEMA.second)
    thirdEMA.setData(tripleEMA.third)
  }

</script>

<template>
  <!-- Chart -->
  <div ref="chartContainer" class="chart"></div>
  <hr/>
  
  <!-- Line -->
  <div class="input-group input-group-sm mb-3 options" v-if="props.type === 'line'">
    <!-- Normalize -->
    <button 
      :class="userInput.normalize ? 'btn btn-success' : 'btn btn-outline-secondary'" 
      type="button" 
      id="button-addon1" 
      @click="triggerNormalize"
    >Normalize</button>

    <!-- Scale -->
    <span class="input-group-text" id="inputGroup-sizing-sm">Scale</span>
    <input type="number" class="form-control" step="0.1" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" value=1 v-model="userInput.scale" :disabled="userInput.normalize">

    <!-- Offset -->
    <span class="input-group-text" id="inputGroup-sizing-sm">Offset</span>
    <input type="number" class="form-control" step="0.1" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" value=0 v-model="userInput.offset" :disabled="userInput.normalize">
  </div>

  <!-- Candle  or Single -->
  <div class="input-group input-group-sm mb-3 options" v-if="props.type === 'candle' || props.type === 'single'">
    <!-- BB -->
    <div class="form-check form-switch">
      <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault">
      <label class="form-check-label" for="flexSwitchCheckDefault">Bollinger Bands</label>
    </div>
  </div>  
</template>

<style scoped>
.chart {
  height: 100%;
}
.options {
  max-width: 500px;
}
</style>
