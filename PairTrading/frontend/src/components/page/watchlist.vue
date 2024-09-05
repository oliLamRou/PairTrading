<script setup>
	import {ref, reactive, onMounted } from 'vue';
	import axios from 'axios'
	//import pair_trade from '@/components/form/pair_trade.vue';
	//import pair_details from '@/components/charts/pair_details.vue';
	import pair_preview from '../charts/pair_preview.vue';
	import trader from '@/components/form/trader.vue'

	import { useRoute } from 'vue-router'
	import { useIbkr } from '@/stores/ibkr';

    //import { ref, onMounted, onBeforeMount, watch, reactive, computed } from 'vue'

    import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
    import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
    import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

	const route = useRoute();
	const ibkr = useIbkr();
	const rowData = ref(null);
	const rowSelection = ref(null);
	const selectedPair = ref(null);
	
	const colDefs = ref([
		{ field: "pair", flex: 1 },
		{ headerName: "Current Position", field: "position", flex: 1 },
  	]);

	onMounted( ()=> {
		getWatchlist();
		console.log(route)
		ibkr.startLiveStream()
	})

    const onRowClicked = async (value) => {
		selectedPair.value = value.data.pair
		await ibkr.cancelAllLiveData()
		ibkr.liveMarketData(selectedPair.value.split('__')[0])
		ibkr.liveMarketData(selectedPair.value.split('__')[1])
    }

	const connectIbkr = () => {
		ibkr.connect()
	}

	const getWatchlist = async () => {
		try {
			const response = await axios.get('http://localhost:5002/get_watchlist');
			rowData.value = response.data;
			console.log('get watchlist')
		} catch (error) {
			console.error(error);
		}
	}
	const cancelStream = () => {
		ibkr.cancelAllLiveData()
	}


</script>

<template>
	<div class="row">
		<div class="col-md-2">

		</div>
		<div class="col-md-7">
			<button @click="cancelStream()">cancel streams</button>
			<button @click="connectIbkr()">connect IBKR</button>
		</div>
		<div class="col-md-2">

		</div>
		
	</div>
	<div class="row">
		<div class="col-md-2">
			<div class="row">
				<div>
					<div class="dropdown">
						<button @click="toggleDropdown" class="dropdown-toggle">Select Watchlist
						<!-- {{ selectedItem ? selectedItem : 'Watchlist' }} -->
						</button>
					</div>
				</div>
			</div>
			<div class="row">
				<ag-grid-vue
                    :rowData="rowData"
                    :columnDefs="colDefs"
                    style="height: 720px"
                    class="ag-theme-quartz"
                    @rowClicked="onRowClicked"
                    :rowSelection="rowSelection"
                    :suppressRowClickSelection="true"
					>
					</ag-grid-vue>
			</div>  
			<div class="row">
				<!-- {{ ibkr.liveData }} -->
			</div> 
										
		</div>
			<div class="col-md-7">
				<pair_preview :pair="selectedPair"/>
			</div>
			<div class="col-md-3">
				<trader :pair="selectedPair"/>
			</div>

		
		</div>
</template>

<style>
	.trade_col {
		width: 500px;
	}
</style>