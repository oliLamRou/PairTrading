<template>
Testing
<button @click="connect">Connect</button>
<button @click="registerLiveData">Register Live Data</button>
<button @click="disconnect">Disconnect</button>
<button @click="getHistoricalData">Get Historical Data</button>
<div>
    load
</div>
<div>
    <LWChart :A="chartData" :type="'candle'"/>
</div>
</template>

<script setup>
    import LWChart from '@/components/charts/LWChart.vue';
    import { ref, onMounted, onBeforeMount, watch, reactive, computed, onUnmounted, onBeforeUnmount } from 'vue'
    import axios from 'axios'

    const backendData = ref();

    let interval
    // const chartData = computed(() => {
    //     return getHistoricalData();
    // })

    // onBeforeMount( async () => {
    //     await connect();
    // });

    const getTicker = () => {
        if (!backendData.value || !backendData.value.length) return [];
        const result = backendData.value.map(
        item => ({
            //time: item.date / 1000,
            time: item.time,
            value: item.close,
            open: item.open,
            high: item.high,
            low: item.low,
            close: item.close,
            volume: item.volume,
        })
        );
        return result;
    };
    const chartData = ref(getTicker())

    const testBackend = async () => {
        try {
            const response = await axios.get('http://localhost:5002/ibkr_connect');
            //console.log(response.data)
            backendData.value = response.data
        } catch (error) {
        console.error(error);
        }
    };

    const connect = async () => {
        try {
            const response = await axios.get('http://localhost:5002/ibkr_connect');
            backendData.value = response.data
        } catch (error) {
        console.error(error);
        }
    };

    const registerLiveData = async () => {
        try {
            const response = await axios.get('http://localhost:5002/ibkr_register_live_data');
            backendData.value = response.data
        } catch (error) {
        console.error(error);
        }
    };

    const getHistoricalData = async () => {
        try {
            const response = await axios.get('http://localhost:5002/ibkr_get_historical_data');
            backendData.value = response.data
            chartData.value = getTicker();
        } catch (error) {
        console.error(error);
        }
    };

    const disconnect = async () => {
        try {
            const response = await axios.get('http://localhost:5002/ibkr_disconnect');
        } catch (error) {
        console.error(error);
        }
    };

    onMounted(async () => {
        //await connect()
        //await getHistoricalData()
        //testBackend();
        //startInterval()
    });

    onBeforeUnmount(async () => {

        clearInterval(interval);  // Clear interval when the component is destroyed
    });

    function startInterval(){
        interval = setInterval(() => {
            testBackend();
        }, 2000)
    }


</script>