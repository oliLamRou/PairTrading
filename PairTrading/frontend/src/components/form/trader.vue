<script setup>
    import LWChart from '@/components/charts/LWChart.vue';
    import { ref, onMounted, onBeforeMount, watch, reactive, computed, onUnmounted, onBeforeUnmount } from 'vue'
    import axios from 'axios'
    import { useIbkr } from '@/stores/ibkr';
    import { usePairForm } from '@/stores/pairs';

    const props = defineProps([
        'pair',
    ]);
    const userInput = reactive({
        orderSize: 100,
    })
    const marketData = ref("")
    const orderId = ref("")
    const orderStatus = ref("")
    const ibkr = useIbkr();
    const pairStore = usePairForm();
    

    const long = () => {
        console.log("long")
    }
    onMounted( async () => {
        console.log("trader")
        //marketData.value = ibkr.liveData
    })

    const placeOrder = async () => {
        response = await ibkr.placeOrder('AAPL', 10, 30, 'BUY', 'LMT')
        orderId.value = response
        console.log(response)
    }

    const getOrderStatus = async () => {
        response = await ibkr.getOrderStatus(orderId.value)
        console.log(response)
    }

    const getLiveData = (ticker, key) => {
        if (!Object.keys(ibkr.liveData).length){
            return ""
        }
        try {
            return ibkr.liveData[ticker][key];
        } catch (error) {
            //console.log(error);
        }
        return ""
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
                <div class="col"><h4>{{ pairStore.A+' - '+pairStore.B }}</h4></div>
                <div class="col"><span class="bold">Position: </span> -150</div>
            </div>
            <div class="row">
                
            </div>
            <div class="row">
                <div class="col">
                    <li><span class="bold">Pair Price: </span> {{ ibkr.pairPrice }}$ </li>
                    <li><span class="bold">Hedge Ratio </span> {{ pairStore.hedgeRatio }}</li>
                    <li><span class="bold">Reverse: </span> {{ pairStore.reverse }}</li>
                </div>
            </div>
            <hr>
            <div>  
                <!-- <button @click="getMarketData()">Get mkt Data</button> -->
                
                <div class="row" v-if="pairStore">
                    <div class="col">
                        <h5>{{ pairStore.A }}</h5>
                        <li><span class="bold">Last: </span> {{ getLiveData(pairStore.A, "LAST") }} </li>
                        <li><span class="bold">Bid: </span> {{ getLiveData(pairStore.A, "BID") }} </li>
                        <li><span class="bold">Ask: </span> {{ getLiveData(pairStore.A, "ASK") }} </li>
                    </div>
                    <div class="col">
                        <h5>{{ pairStore.B }}</h5>
                        <li><span class="bold">Last: </span> {{ getLiveData(pairStore.B, "LAST") }} </li>
                        <li><span class="bold">Bid: </span> {{ getLiveData(pairStore.B, "BID") }} </li>
                        <li><span class="bold">Ask: </span> {{ getLiveData(pairStore.B, "ASK") }} </li>
                    </div>
                </div>

            </div>
            <hr>
            <div class="row">
                <div class="col">
                    <h5>Place Order</h5>
                </div>
            </div>

            <div class="row">
                <div class="col">
                    <span class="input-group-text" id="inputGroup-sizing-sm">Shares</span>
                    <input type="number" class="form-control" step="1" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" value=1 v-model="userInput.orderSize">
                </div>
                <div class="col">
                    <li><span class="bold">{{ pairStore.A }} amount: </span> {{ userInput.orderSize }}</li>
                    <li><span class="bold">{{ pairStore.B }} amount: </span> {{ Math.round(userInput.orderSize * pairStore.hedgeRatio) }}</li>
                </div>
                
            </div>
            <div class="row">
                <div class="col">
                    <li><span class="bold">Cost A: </span> {{ getLiveData(pairStore.A, "LAST") * userInput.orderSize }}$</li>
                    <li><span class="bold">Cost B: </span> {{ getLiveData(pairStore.B, "LAST") * userInput.orderSize }}$</li>
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