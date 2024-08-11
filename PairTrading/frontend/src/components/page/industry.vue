<script setup>
  import { ref, onMounted, onBeforeMount, watch, reactive, computed } from 'vue'
  import axios from 'axios'
  import charts from '@/components/charts/chart_list.vue';
  import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
  import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
  import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

  const industries = ref(null);
  const min_price = ref(5);
  const max_price = ref(100);
  const min_volume = ref(1000);
  const max_volume = ref(100000000);

  const selectedIndustry = ref(null);
  const pairs = ref([]);
  const info = ref([]);
  const ratio = ref(0.15);

  const rowData = ref(null);
  const rowSelection = ref(null);

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

  const fetchInfo = async (industry) => {
    try {
      const response = await axios.get('http://localhost:5002/get_info', {
        params: {industry: industry}
      });
      info.value = response.data;
    } catch (error) {
      console.error(error);
    }
  }; 

  const onRowClicked = (value) => {
    //console.log("clicked", value.data.industry)
    selectedIndustry.value = value.data.industry
  }

  onBeforeMount(() => {
    fetchIndustries();
  });

  watch(industries, (newIndustries) => {
        if (newIndustries) {
            rowData.value = newIndustries;
            console.log("fetched indu")
        }
    });

  watch(selectedIndustry, (newIndustry) => {
    if (newIndustry) {
      fetchPairs(newIndustry)
      fetchInfo(newIndustry)
    }
  });

  const filter_diff = computed(()=>{
    return pairs.value.filter(item => item.avg_diff < ratio.value)
  })

  const colDefs = ref([
    { field: "industry", flex: 1 },
    { field: "potential_pair", flex: 1 },
  ]);

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
          
        </div>
        <ag-grid-vue
            :rowData="rowData"
            :columnDefs="colDefs"
            style="height: 250px"
            class="ag-theme-quartz"
            @rowClicked="onRowClicked"
            :rowSelection="rowSelection"
            :suppressRowClickSelection="false"
          >
          </ag-grid-vue>
        <div class="input-group mb-1">
          <span class="input-group-text">Ratio</span>
          <input type="number" class="form-control" aria-label="ratio" step="0.01" min="0" value=0.15 v-model="ratio">
        </div>

      </div>
    </div>

    <hr/>
  
    <div class="row">
      <div>
        <charts :pairs="filter_diff" :info="info"/>
      </div>
    </div>
  </div>
</template>

<style>
  
</style>