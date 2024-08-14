<script setup>
  import { reactive, ref, watch, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router'
  import { usePairForm } from '@/stores/pairs';
  
  const store = usePairForm();
  const route = useRoute();

  const userInput = reactive({
    reverse: Boolean,
    watchlist: Boolean,
    hedge_ratio: Number,
    notes: String,
  });

  const pair = computed( () => {
    return route.params.pair;
  });

  const A = computed( () => {
    return pair.value.split('__')[0];
  });

  const B = computed( () => {
    return pair.value.split('__')[1];
  });

  const pair_price = computed(()=> {
    return 100 * userInput.hedge_ratio
  });  

  onMounted(() => {
    const pairInfo = store.pairs[pair.value]
    userInput.reverse = pairInfo.reverse;
    userInput.watchlist = pairInfo.watchlist;
    userInput.hedge_ratio = pairInfo.hedge_ratio;
    userInput.notes = pairInfo.notes;
  });

  watch(() => userInput.hedge_ratio, (newData) => {
    store.update_hedge_ratio(pair, newData)
  });

</script>

<template>
  <form>
    <h3>{{A}} - {{B}}</h3>
    <h5 class="mt-3">Pair Price: ${{pair_price}}</h5>
    <ul>
      <li>{{A}} Dollar volume Average: $999,999,999</li>
      <li>{{B}} Dollar volume Average: $999,999,999</li>
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
      <input type="number" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" step="0.01" v-model="userInput.hedge_ratio"
      >
    </div>    
    <div class="input-group input-group-sm mt-1">
      <span class="input-group-text" id="inputGroup-sizing-sm">Notes</span>
      <textarea class="form-control" id="exampleFormControlTextarea1" rows="2" v-model="userInput.notes" placeholder="Take note here"></textarea>
    </div>
    <!-- <button type="button" class="btn btn-primary mt-3" @click="save()">Save</button> -->
  </form>
</template>