<script setup>
	import {ref, reactive, onMounted } from 'vue';
	import pair_trade from '@/components/form/pair_trade.vue';
	//import pair_details from '@/components/charts/pair_details.vue';
	import { useRoute } from 'vue-router'

    //import { ref, onMounted, onBeforeMount, watch, reactive, computed } from 'vue'

    import "ag-grid-community/styles/ag-grid.css"; // Mandatory CSS required by the Data Grid
    import "ag-grid-community/styles/ag-theme-quartz.css"; // Optional Theme applied to the Data Grid
    import { AgGridVue } from "ag-grid-vue3"; // Vue Data Grid Component

	const route = useRoute();
	
	onMounted( ()=> {
		console.log(route)
	})

    const onRowClicked = (value) => {
        if(!loading.value){
        selectedIndustry.value = value.data.industry
        loading.value = true;
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
				<div class="col">
					<pair_details/>
				</div>
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