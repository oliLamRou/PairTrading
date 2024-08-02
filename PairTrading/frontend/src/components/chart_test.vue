<script setup>
  import { ref, watch, defineProps, onMounted, computed } from 'vue';
  import axios from 'axios';
  import LWChart from '@/components/LWChart.vue';
  import qs from 'qs';

  const data = ref(null);
  const pair = computed ( () => {
    return ['ARKK', 'ARKG']
  })

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5002/get_df', {
        params: { tickers: pair.value },
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
        close: item.close
      })
    );
    return result;
  };

  onMounted( async () => {
    await fetchData();
  });
</script>
<template>
  <div>
    <!-- Compare -->
    <LWChart :A="getTicker(pair[0])" :B="getTicker(pair[1])"/>
    <!-- Candle -->
    <LWChart :A="getTicker(pair[0])" :type="'candle'"/>
    <!-- Single -->
    <LWChart :A="getTicker(pair[0])" :type="'single'"/>    
  </div>
</template>