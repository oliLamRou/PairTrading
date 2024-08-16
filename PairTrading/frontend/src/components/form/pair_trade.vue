<script setup>
  import { reactive, ref, watch, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router'
  import { usePairForm } from '@/stores/pairs';
  
  const store = usePairForm();
  const route = useRoute();

  const userInput = reactive({
    reverse: store.pairs[store.pair].reverse,
    watchlist: store.pairs[store.pair].watchlist,
    hedge_ratio: store.pairs[store.pair].hedge_ratio,
    notes: store.pairs[store.pair].notes,
  });

  const pair_price = computed(()=> {
    const data = store.pairs[store.pair].data
    if (!data) {
      return -1
    }
    let pair_price;
    const last = Math.max.apply(Math, data.map(function(d) { return d.date; }))
    const A_ = data.filter((d) => d.ticker === store.A && d.date === last)[0]
    const B_ = data.filter((d) => d.ticker === store.B && d.date === last)[0]
    if (userInput.reverse) {
      pair_price = B_.close - (A_.close * userInput.hedge_ratio)
    } else {
      pair_price = A_.close - (B_.close * userInput.hedge_ratio)
    }
    return round_to_two(pair_price)
  });

  const round_to_two = ((number) => {
    return Math.round(number * 100) / 100
  })

  const average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;
  
  const avg_vol_A = computed(()=> {
    const data = store.pairs[store.pair].data
    if (!data || !data.length > 0) {
      return -1
    }  
    
    const avg_vol = average( data.filter((d) => d.ticker === store.A).map(item => item.volume) )
    return Math.round(avg_vol)
  });  

  const avg_vol_B = computed(()=> {
    const data = store.pairs[store.pair].data
    if (!data || !data.length > 0) {
      return -1
    }  
    
    const avg_vol = average( data.filter((d) => d.ticker === store.B).map(item => item.volume) )
    return Math.round(avg_vol)
  });

  watch(() => userInput.hedge_ratio, (newData) => {
    store.update_hedge_ratio(newData)
  });

  watch(() => userInput.reverse, (newData) => {
    store.update_reverse(newData)
  });

</script>

<template>
  <form>
    <h3>{{store.A}} - {{store.B}}</h3>
    <h5 class="mt-3">Pair Price: ${{pair_price}}</h5>
    <ul>
      <li>{{store.A}} Dollar volume Average: {{avg_vol_A}}</li>
      <li>{{store.B}} Dollar volume Average: {{avg_vol_B}}</li>
    </ul>
    <hr/>
    <div class="form-check form-switch">
      <input class="form-check-input" type="checkbox" id="flexSwitchCheckChecked" v-model="userInput.watchlist">
      <label class="form-check-label" for="flexSwitchCheckChecked">Watchlist</label>
    </div>
    <div class="form-check form-switch">
      <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault" v-model="userInput.reverse">
      <label class="form-check-label" for="flexSwitchCheckDefault">Reverse Order</label>
    </div>
    <div class="input-group input-group-sm mt-1">
      <span class="input-group-text" id="inputGroup-sizing-sm">Hedge Ratio</span>
      <input type="number" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" step="0.01" v-model.number="userInput.hedge_ratio" @change="update_hedge_ratio"
      >
    </div>    
    <div class="input-group input-group-sm mt-1">
      <span class="input-group-text" id="inputGroup-sizing-sm">Notes</span>
      <textarea class="form-control" id="exampleFormControlTextarea1" rows="2" v-model.string="userInput.notes" placeholder="Take note here"></textarea>
    </div>
    <!-- <button type="button" class="btn btn-primary mt-3" @click="save()">Save</button> -->
  </form>
</template>