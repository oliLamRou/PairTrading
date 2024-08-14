<script setup>
  import { reactive, ref, watch, onMounted, onUnmounted, computed } from 'vue';
  import axios from 'axios';
  import qs from 'qs';
  import { useRoute } from 'vue-router'
  import { usePairForm } from '@/stores/pairs';
  
  const store = usePairForm();

  const pairInfo = reactive({
    pair: null,
    A: null,
    B: null,
    reverse: false,
    watchlist: false,
    hedge_ratio: 1,
    notes: '',
  });

  const route = useRoute();

  //Computed
  const pair_price = computed(()=> {
    return 100 * pairInfo.hedge_ratio
  });

  //backend
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
    pairInfo.pair = route.params.pair
    pairInfo.A = pairInfo.pair.split('__')[0]
    pairInfo.B = pairInfo.pair.split('__')[1]
    fetchPairInfo()
  })

  function save() {
    console.log('saving', pairInfo)
    updatePairInfo()
  }

  const hedge_ratio = computed( () => {
    return store.get_hedge_ratio(pairInfo.pair)
    // return 1
  })

</script>

<template>
  <form>
    <h3>{{pairInfo.A}} - {{pairInfo.B}}</h3>
    <h5 class="mt-3">Pair Price: ${{pair_price}}</h5>
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
      <input type="number" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" :value="store.get_hedge_ratio(pairInfo.pair)" step="0.01">
    </div>    
    <div class="input-group input-group-sm mt-1">
      <span class="input-group-text" id="inputGroup-sizing-sm">Notes</span>
      <textarea class="form-control" id="exampleFormControlTextarea1" rows="2" v-model="pairInfo.notes" placeholder="Take note here"></textarea>
    </div>
    <button type="button" class="btn btn-primary mt-3" @click="save()">Save</button>
  </form>
</template>