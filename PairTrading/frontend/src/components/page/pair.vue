<script setup>
	import {ref, reactive, onMounted } from 'vue';
	import pair_trade from '@/components/form/pair_trade.vue';
	import pair_details from '@/components/charts/pair_details.vue';
	import { useRoute } from 'vue-router'

	const route = useRoute();
	
	onMounted( ()=> {
		console.log(route)
		const pair = route.params.pair.split('__')

	})

</script>

<template>
	<div class="card d-flex flex-column bd-highlight m-3" style="min-width: 1200px;">
		<div class="card-header">
			<h3>Title</h3>
		</div>
		<div class="card-body">
			<div class="row">
				<div class="col">
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
	.trade_col {
		max-width: 30%;
	}
</style>