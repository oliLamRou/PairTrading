<script setup>
  import { ref, computed, watch, defineProps } from 'vue';
  import axios from 'axios';
  import LWChart from '@/components/charts/LWChart.vue';
  import info from '@/components/form/info.vue';
  import qs from 'qs';

  const data = ref([]);
  const props = defineProps({
    pairs: {
      type: Array,
      required: true,
    },
    info: {
      type: Array,
      required: true,
    }
  });

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5002/get_df', {
        params: { tickers: uniqueTicker.value },
        paramsSerializer: params => {
         return qs.stringify(params, { arrayFormat: 'repeat' });
        }
      });
      data.value = response.data;
    } catch (error) {
      console.log(error);
    }
  };

  function getTicker(ticker) {
    const result = data.value.filter(item => item.ticker === ticker).map(
      item => ({
        time: item.date / 1000,
        value: item.close,
        ticker: item.ticker
      })
    );
    return result
  }

  const uniqueTicker = computed(()=>{
    return [
        ...new Set([
            ...props.pairs.map(item => item.A), 
            ...props.pairs.map(item => item.B)
          ])
      ];
  })

  const pairData = computed(()=>{
    const pair_data = props.pairs.map(item => ({
        pair: [item.A, item.B],
        A: getTicker(item.A),
        B: getTicker(item.B),
      })
    )
    console.log(pair_data)
    return pair_data
  })

  function pairInfo(pair) {
    //Forcing data to be in the right order
    return [
      ...props.info.filter(item => item.ticker === pair[0]),
      ...props.info.filter(item => item.ticker === pair[1])
    ]
  }

  watch(
    () => props.pairs,
    (newTickers) => {
      fetchData()      
    }
  )

</script>
<template>
  <div class="card d-flex mt-2" v-for="data in pairData">
    <!-- Header -->
    <div class="card-header">
      <h4>
        {{data.pair[0]}} - {{data.pair[1]}}
      </h4>
    </div>    
    <div class="row m-3">
      <!-- Chart -->
      <div class="col-8">
        <div>
          <LWChart :A="data.A" :B="data.B"/>
        </div>
      </div>
      <!-- Info -->
      <div class="col-4" style="min-width: 100px;">
        <info :info="pairInfo(data.pair)"/>
      </div>
    </div>
  </div>
</template>