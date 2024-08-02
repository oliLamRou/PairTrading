<script setup>
  import { reactive, computed, onMounted, defineProps, ref } from 'vue'
  import axios from 'axios'

  const props = defineProps({
    info: {
      type: Array,
      required: true,
      default: () => [
        {
          'name': 'Company A',
          'market_cap': 99999999,
          'share_class_shares_outstanding': 9999999
        },
        {
          'name': 'Company B',
          'market_cap': 9999999,
          'share_class_shares_outstanding': 9999999
        }
      ]
    },
  });

  const infos = ref({
      "Ticker": "ticker",
      "Name": "name",
      "Market Cap":"market_cap",
      "Share": "share_class_shares_outstanding"
    })

  onMounted(() => {
    console.log(props.info)
  })

</script>

<template>
  <div class="card p-5">
    <div class="row">
      <div class="col" v-for="index in [0,1]">
        <h4>{{props.info[index].ticker}}</h4>
        <h6 v-for="(v, k) in infos">
          <b>{{ k }}:</b> {{ props.info[index][v] }}
        </h6>
      </div>
    </div>
    <div class="row d-inline-flex mt-5">
      <button type="button" class="btn btn-primary">Pair Details</button>
    </div>
  </div>
</template>

<style>
  .custom-card {
  max-width: 600px;
  }
</style>