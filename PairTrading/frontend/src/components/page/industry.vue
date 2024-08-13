<script setup>
  import { ref, onMounted, watch, reactive, computed } from 'vue'
  import axios from 'axios'
  import charts from '@/components/charts/chart_list.vue';

  const industries = ref(null);
  const min_price = ref(5);
  const max_price = ref(100);
  const min_volume = ref(1000);
  const max_volume = ref(100000000);

  const selectedIndustry = ref('Choose...');
  const pairs = ref([]);
  const company_info = ref([]);
  const ratio = ref(0.15);

  const fetchIndustries = async () => {
    try {
      const response = await axios.get('http://localhost:5002/get_potential_pair');
      industries.value = response.data;
    } catch (error) {
      console.error(error);
    }
  };

  const fetchPairs = async (industry) => {
    try {
      const response = await axios.get('http://localhost:5002/get_pairs', {
        params: {
          industry: industry, 
          min_price: min_price.value,
          max_price: max_price.value,
          min_volume: min_volume.value,
          max_volume: max_volume.value,
        }
      });
      pairs.value = response.data;
    } catch (error) {
      console.error(error);
    }
  };

  const fetch_company_info = async (industry) => {
    try {
      const response = await axios.get('http://localhost:5002/company_info', {
        params: {industry: industry}
      });
      company_info.value = response.data;
    } catch (error) {
      console.error(error);
    }
  };  

  onMounted(() => {
    fetchIndustries();
  });

  watch(selectedIndustry, (newIndustry) => {
    if (newIndustry) {
      console.log('CHANGE')
      fetchPairs(newIndustry)
      fetch_company_info(newIndustry)
    }
  });

  const filter_diff = computed(()=>{
    return pairs.value.filter(item => item.avg_diff < ratio.value)
  })

</script>

<template>
  <div class="d-flex flex-column bd-highlight m-3" style="min-width: 1200px;">
    <div class="row">
      <div class="col">
        <div class="input-group mb-1">
          <span class="input-group-text">Price</span>
          <span class="input-group-text">Min</span>
          <input type="number" class="form-control" aria-label="min price" value=5>
          <span class="input-group-text">Max</span>
          <input type="number" class="form-control" aria-label="max price" value=100>
          <span class="input-group-text">Volume</span>
          <span class="input-group-text">Min</span>
          <input type="number" class="form-control" aria-label="min volume" value=1000>
          <span class="input-group-text">Max</span>
          <input type="number" class="form-control" aria-label="max volume" value=10000000>
        </div>

        <div class="input-group mb-1" v-if="industries">
          <label class="input-group-text" for="inputGroupSelect01">Industry</label>
          <select class="form-select" id="inputGroupSelect01" v-model="selectedIndustry">
            <option selected >Choose...</option>
            <option v-for="(industry, index) in industries" :key="industry" :value="industry.industry">
              {{industry.potential_pair}} - {{industry.industry}}
            </option>
          </select>
          <button type="button" class="btn btn-primary">Submit</button>
          <button type="button" class="btn btn-secondary">Reset</button>
        </div>
        <div class="input-group mb-1">
          <span class="input-group-text">Ratio</span>
          <input type="number" class="form-control" aria-label="ratio" step="0.01" min="0" value=0.15 v-model="ratio">
        </div>

      </div>
    </div>

    <hr/>
  
    <div class="row">
      <div>
        <charts :pairs="filter_diff" :company_info="company_info"/>
      </div>
    </div>
  </div>
</template>

<style>
  
</style>