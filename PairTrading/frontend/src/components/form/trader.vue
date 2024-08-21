<script setup>
    import {ref, reactive, onMounted, computed } from 'vue';

    const props = defineProps([
        'pair'
    ]);

    // const pair = computed( () => {
    //     return pa;
    // })
    const long = () => {
        console.log("long")
    }
    onMounted( async () => {

    })
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
                    <button @click="long">Long</button>
                    <button @click="short">Short</button>
                    <button @click="closePosition">Close Position</button>
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