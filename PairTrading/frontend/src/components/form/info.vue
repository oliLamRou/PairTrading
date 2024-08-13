<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const props = defineProps({
    info: {
      type: Array,
      required: true,
    },
  });

  const infos = ref({
      "Ticker": "ticker",
      "Name": "name",
      "Market Cap":"market_cap",
      "Share": "share_class_shares_outstanding"
    })

  const router = useRouter()

  const pair_details = () => {
    const pair = [props.info[0].ticker, props.info[1].ticker].join('__')
    const url = router.resolve({ name: 'Details', params: { pair: pair } }).href
    window.open(url, '_blank')
  }

</script>

<template>
  <div class="card p-5" v-if="props.info.length > 0">
    <div class="row">
      <div class="col" v-for="index in [0,1]">
        <h4>{{props.info[index].ticker}}</h4>
        <h6 v-for="(v, k) in infos">
          <b>{{ k }}:</b> {{ props.info[index][v] }}
        </h6>
      </div>
    </div>
    <div class="row d-inline-flex mt-5">
      <button type="button" class="btn btn-primary" @click="pair_details">Pair Details</button>
    </div>
  </div>
</template>

<style>
  .custom-card {
  max-width: 600px;
  }
</style>