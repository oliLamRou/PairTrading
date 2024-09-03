<script setup>
    import LWChart from '@/components/charts/LWChart.vue';
    import { ref, onMounted, onBeforeMount, watch, reactive, computed, onUnmounted, onBeforeUnmount } from 'vue'
    import axios from 'axios'
    import { useIbkr } from '@/stores/ibkr';

    const props = defineProps([
        'pair'
    ]);
    const marketData = ref("")
    const orderId = ref("")
    const orderStatus = ref("")
    const ibkr = useIbkr();

    const long = () => {
        console.log("long")
    }
    onMounted( async () => {
        console.log("trader")
        marketData.value = ibkr.liveData
        //marketData.value = ibkr.getMarketData("AAPL")
        // const eventSource = new EventSource('http://127.0.0.1:5002/ibkr_stream/market_data');
        // eventSource.onmessage = (event) => {
        //     console.log(event.data)
        //     marketData.value = event.data
        // }
    })

    const getMarketData = async () => {
        //marketData.value = await ibkr.liveMarketData("AAPL")
        console.log(marketData.value)
    }

    const placeOrder = async () => {
        response = await ibkr.placeOrder('AAPL', 10, 30, 'BUY', 'LMT')
        orderId.value = response
        console.log(response)
    }

    const getOrderStatus = async () => {
        response = await ibkr.getOrderStatus(orderId.value)
        console.log(response)
    }
</script>

<template>
    <div class="card">
        <div class="card-header">
            <div class="row">
                <div class="col"><h5>Trader</h5></div>
                <div class="col"><span class="bold">Balance: </span>5 piasse</div>
            </div>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col"><h4>{{ pair }}</h4></div>
                <div class="col"><span class="bold">Position: </span> -150</div>
            </div>
            <div class="row">
                
            </div>
            <div class="row">
                <div class="col">
                    <li><span class="bold">Pair Price: </span> 2$</li>
                    <li><span class="bold">Hedge Ratio </span> 0.94</li>
                    <li><span class="bold">Reverse: </span> False</li>
                </div>
            </div>
            <hr>
            <div>  
                <button @click="getMarketData()">Get mkt Data</button>

                {{ ibkr.liveData }}
            </div>
            <hr>
            <div class="row">
                <div class="col">
                    <h5>Place Order</h5>
                </div>
            </div>

            <div class="row">
                <div class="col">
                    <span class="bold">Shares </span><input width="2">
                </div>
                <div class="col">
                    <span class="bold">Amount: </span>0$
                </div>
            </div>

            <div class="row">
                <div class="col">
                    <br>
                    <button @click="placeOrder()">Long</button>
                    <button @click="short">Short</button>
                    <button @click="closePosition">Close Position</button>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <br>
                    <button @click="getOrderStatus()">Order Status</button>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    {{ orderStatus }}
                    
                </div>
            </div>
        </div>
        
        
    </div>

</template>

<style>
.bold {
  font-weight: bold;
}
.bold {
  font-weight: bold;
}
</style>