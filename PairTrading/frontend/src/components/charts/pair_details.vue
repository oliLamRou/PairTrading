<script setup>
  import { ref, watch, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router'
  import axios from 'axios';
  import LWChart from '@/components/charts/LWChart.vue';
  import qs from 'qs';
  import { usePairForm } from '@/stores/pairs';

  const route = useRoute();
  const store = usePairForm();

  const data = ref(null);

  const pair = computed( () => {
    return route.params.pair;
  });

  const A = computed( () => {
    return pair.value.split('__')[0];
  });

  const B = computed( () => {
    return pair.value.split('__')[1];
  });  

  const fetch_market_data = async () => {
    try {
      const response = await axios.get('http://localhost:5002/get_market_data', {
        params: { tickers: [A.value,B.value] },
        paramsSerializer: params => {
          return qs.stringify(params, { arrayFormat: 'repeat' });
        }
      });
      data.value = response.data;
    } catch (error) {
      console.log(error);
    }
  };

  const getTicker = (ticker) => {
    if (!data.value || !data.value.length) return [];
    const result = data.value.filter(item => item.ticker === ticker).map(
      item => ({
        time: item.date / 1000,
        value: item.close,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
        volume: item.volume
      })
    );
    return result;
  };

  onMounted( async () => {
    await fetch_market_data();
  });

  const getPairPrice = (ticker) => {
    const hedge_ratio = store.pairs[pair.value]?.hedge_ratio
    if (!data.value || !data.value.length) return [];

    const resultA = data.value.filter(item => item.ticker === A.value).map(
      item => ({
        time: item.date / 1000,
        value: item.close * hedge_ratio,
        open: item.open * hedge_ratio,
        high: item.high * hedge_ratio,
        low: item.low * hedge_ratio,
        close: item.close * hedge_ratio,
        volume: item.volume
      })
    );

    const resultB = data.value.filter(item => item.ticker === B.value).map(
      item => ({
        time: item.date / 1000,
        value: item.close * hedge_ratio,
        open: item.open * hedge_ratio,
        high: item.high * hedge_ratio,
        low: item.low * hedge_ratio,
        close: item.close * hedge_ratio,
        volume: item.volume
      })
    );
    return resultA;
  };

  function test() {
    const hedge_ratio = store.pairs[pair.value]?.hedge_ratio
    if (!data.value || !data.value.length) return [];
    const result = Map.groupBy(data.value, date => ({
      time: date,
      close: date[0].close - date[1].close
    }));
    console.log(result)
  }

</script>

<template>
  <div>
    <button @click="test">test</button>
    <div class="row">
      <div class="col">
        <div class="card">
          <!-- Candle -->
          <!-- <LWChart :A="getPairPrice(A)" :type="'candle'"/> -->
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="card">
          <!-- Compare -->
          <!-- <LWChart :A="getTicker(A)" :B="getTicker(B)"/>                -->
        </div>
      </div>
      <div class="col">
        <div class="card">
          <!-- Single -->
          <!-- <LWChart :A="getTicker(A)" :type="'single'"/>  -->
        </div>
      </div>
    </div>
  </div>
</template>