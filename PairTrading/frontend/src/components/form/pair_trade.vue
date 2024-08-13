<script setup>
  import { reactive, ref, watch, onMounted, onUnmounted } from 'vue';
  import axios from 'axios';
  import qs from 'qs';
  import { useRoute } from 'vue-router'

  const pairInfo = reactive({
    A: null,
    B: null,
    reverse: false,
    watchlist: false,
    hedge_ratio: 1,
    notes: '',
  });

  const route = useRoute();

  const fetchPairInfo = async () => {
    try {
      const response = await axios.get('http://localhost:5002/get_pair_info', {
        params: { tickers: [pairInfo.A, pairInfo.B] },
        paramsSerializer: params => {
         return qs.stringify(params, { arrayFormat: 'repeat' });
        }
      });
      if (response.data) {
        pairInfo.reverse = Boolean(response.data.reverse)
        pairInfo.watchlist = Boolean(response.data.watchlist)
        pairInfo.hedge_ratio = response.data.hedge_ratio
        pairInfo.notes = response.data.notes
      }
      
    } catch (error) {
      console.log(error);
    }
  };
 
  const updatePairInfo = async () => {
    try {
      const response = await axios.post('http://localhost:5002/update_pair_info', {
        tickers: [pairInfo.A, pairInfo.B],
        pairInfo: pairInfo
      });
      console.log('updated', response.data)
    } catch (error) {
      console.log(error);
    }
  };  

  onMounted(() => {
    const pair = route.params.pair.split('__')
    pairInfo.A = pair[0]
    pairInfo.B = pair[1]
    fetchPairInfo()
  })

  onUnmounted( () => {
    console.log("onUnmounted")
    save()
  })

  function save() {
    updatePairInfo()
  }

</script>

<template>
  <form>
    <h3>{{pairInfo.A}} - {{pairInfo.B}}</h3>
    <h5 class="mt-3">Pair Price: $999</h5>
    <ul>
      <li>{{pairInfo.A}} Dollar volume Average: $999,999,999</li>
      <li>{{pairInfo.B}} Dollar volume Average: $999,999,999</li>
    </ul>
    <hr/>
    <div class="form-check form-switch">
      <input class="form-check-input" type="checkbox" id="flexSwitchCheckChecked" v-model="pairInfo.watchlist">
      <label class="form-check-label" for="flexSwitchCheckChecked">Watchlist</label>
    </div>
    <div class="form-check form-switch">
      <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" v-model="pairInfo.reverse">
      <label class="form-check-label" for="flexSwitchCheckDefault">Reverse Order</label>
    </div>
    <div class="input-group input-group-sm mt-1">
      <span class="input-group-text" id="inputGroup-sizing-sm">Hedge Ratio</span>
      <input type="number" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" v-model="pairInfo.hedge_ratio" step="0.01">
    </div>    
    <div class="input-group input-group-sm mt-1">
      <span class="input-group-text" id="inputGroup-sizing-sm">Notes</span>
      <textarea class="form-control" id="exampleFormControlTextarea1" rows="2" v-model="pairInfo.notes" placeholder="Take note here"></textarea>
    </div>
    <button type="button" class="btn btn-primary mt-3" @click="save()">Save</button>
  </form>
</template>

<style>
  .custom-card {
  max-width: 600px;
  }
</style>