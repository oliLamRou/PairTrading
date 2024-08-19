<script setup>
	import {ref, reactive, onMounted } from 'vue';
	import axios from 'axios'
	import pair_trade from '@/components/form/pair_trade.vue';
	//import pair_details from '@/components/charts/pair_details.vue';
	import { useRoute } from 'vue-router'

    //import { ref, onMounted, onBeforeMount, watch, reactive, computed } from 'vue'

    import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
    import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
    import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

	const route = useRoute();
	const rowData = ref(null)
	const rowSelection = ref(null);
	const watchlist = ref(null)
	
	const colDefs = ref([
		{ field: "pair", flex: 1 },
		{ headerName: "Current Position", field: "position", flex: 1 },
  	]);

	onMounted( ()=> {
		getWatchlist();
		console.log(route)
	})

    const onRowClicked = (value) => {
        if(!loading.value){
        	selectedIndustry.value = value.data.industry
        	loading.value = true;
        }
    }

	const getWatchlist = async () => {
		try {
			const response = await axios.get('http://localhost:5002/get_watchlist');
			rowData.value = response.data;
			console.log('get watchlist')
			console.log(response.data)
		} catch (error) {
			console.error(error);
		}
	}


</script>

<template>
	<div class="card d-flex flex-column bd-highlight m-3" style="min-width: 1200px;">
		<div class="card-header">
			<h3>Watchlists</h3>
		</div>
		<div class="card-body">
			<div class="row">
				<div class="col trade_col">
					<ag-grid-vue
                    :rowData="rowData"
                    :columnDefs="colDefs"
                    style="height: 250px"
                    class="ag-theme-quartz"
                    @rowClicked="onRowClicked"
                    :rowSelection="rowSelection"
                    :suppressRowClickSelection="true"
                >
                </ag-grid-vue>			
				</div>		
			</div>
		</div>
	</div>
</template>

<style>
	.trade_col {
		width: 500px;
	}
</style>