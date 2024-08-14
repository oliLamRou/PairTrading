<script setup>
	import {ref, reactive, onMounted } from 'vue';
	import pair_trade from '@/components/form/pair_trade.vue';
	import pair_details from '@/components/charts/pair_details.vue';
	import { useRoute } from 'vue-router'
	import { usePairForm } from '@/stores/pairs';

	const route = useRoute();
  	const store = usePairForm();

	onMounted( ()=> {
		store.add(route.params.pair)
	})

</script>

<template>
	<div class="card m-3">
		<div class="card-header">
			<h3>Title</h3>
		</div>
		<div class="card-body">
			<div class="row">
				<div class="col chart_col">
					<pair_details/>
				</div>
				<div class="col trade_col">
					<pair_trade/>			
				</div>		
			</div>
		</div>
	</div>
</template>

<style>
	.compare_page {
		min-width: 1902px;
	}
	.trade_col {
		max-width: 30%;
	}
	.chart_col {
		max-width: 70%;
	}
</style>