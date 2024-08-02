<script setup>
	import { ref, computed, watch, defineProps } from 'vue';
  import LWChart from '@/components/LWChart/pair.vue';
  import info from '@/components/info.vue';


</script>

<template>
	<div class="container">
		<div class="card">
			<div class="card-header">
				<h1>Title</h1>
			</div>
			<div class="card-body">
				<div class="row">
					<div class="col">
						<LWChart/>
					</div>
				</div>
				<div class="row">
					<div class="col">
						<LWChart/>
					</div>
					<div class="col">
						<LWChart/>
					</div>	
				</div>
			</div>
		</div>
	</div>
</template>