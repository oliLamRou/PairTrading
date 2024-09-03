import { defineStore } from "pinia";
import axios from 'axios';
import qs from 'qs';

export const useIbkr = defineStore('ibkr',{
  state:()=>({
    connectionId: 0,
    liveData: {},
    chartData: {},
    reqIds: {}, //{reqId: ticker}
    barSize: "",
    chartLength: "",
    pairStore: null,
    pairInfo: {A: "", B: "", hedgeRatio: 1, reverse: false},

  }),
  getters: {
    //A() { return this.pair.split('__')[0] },
  },
  actions:{
    async connect(){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_connect');
            return response.data
        } catch (error) {
        console.error(error);
        }
    },
    async liveMarketData(ticker){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_live_market_data', {
                params: {ticker: ticker}
            });
            let reqId = response.data
            this.reqIds[reqId] = ticker
            return reqId
        } catch (error) {
        console.error(error);
        }
    },
    async getMarketData(ticker){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_get_market_data', {
                params: {ticker: ticker}
            });
            console.log(response.data)
            return response.data
        } catch (error) {
        console.error(error);
        }
    },
    async getHistoricalData(ticker, size, length){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_get_historical_data', {
                params: {
                    ticker: ticker,
                    size: size,
                    length: length
                }
            });
            return response.data
        } catch (error) {
        console.error(error);
        }
    },
    async placeOrder(ticker, quantity, price, action, orderType){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_place_order', {
                params: {
                    ticker: ticker,
                    quantity: quantity,
                    price: price,
                    action: action,
                    orderType: orderType
                }
            });
            return response.data
        } catch (error) {
        console.error(error);
        }
    },
    async disconnect(){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_disconnect');
        } catch (error) {
        console.error(error);
        }
    },
    async updatePairData(){
        let dataA = await this.getHistoricalData(this.pairStore.A, this.barSize, this.chartLength)
        let dataB = await this.getHistoricalData(this.pairStore.B, this.barSize, this.chartLength)
        if (dataA.length > 0){ this.chartData["A"] = dataA };
        if (dataB.length > 0){ this.chartData["B"] = dataB };
        await this.calculatePairPrice()
        //console.log(this.chartData)
    },
    async updateLastBar(){
        const currentBar = this.chartData.A[this.chartData.A.length -1]
        const newClose = this.liveData[this.pairStore.B]["LAST"]

        console.log("newCLose:", newClose)
        console.log("old CLose:", this.chartData.A[this.chartData.A.length -1]["close"])

        this.chartData.B[this.chartData.B.length -1]["close"] = newClose
        //this.chartData.B[this.chartData.B.length -1]["time"] = Date.now() / 1000
        this.calculatePairPrice()
    },
    async appendMarketData(data){
        let reqId = data["req_id"]
        
        //console.log('APPEND MKT DATA: ', data)
        //console.log('reqIds: ', this.reqIds)

        const ticker = this.reqIds[reqId]
        if (typeof ticker === 'undefined') { 
            console.log('Undefined ticker')
            return 
        }
        
        let value = -1
        if ('size' in data){
            value = data["size"]
        } else if('price' in data){
            value = data["price"]
        }
        
        if (typeof(this.liveData[ticker]) === 'undefined'){
            this.liveData[ticker] = {}
        }

        let key = data["tickType"]
        this.liveData[ticker][key] = value

        await this.updateLastBar()

    },
    async startLiveStream(){
        const eventSource = new EventSource('http://127.0.0.1:5002/ibkr_stream/market_data');
        eventSource.onmessage = (event) => {
            //console.log(typeof(event.data))
            //console.log("Received data: ", JSON.parse(event.data))
            this.appendMarketData(JSON.parse(event.data))
        }
    },
    async cancelAllLiveData(){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_cancel_live_data');
        } catch (error) {
        console.error(error);
        }
    },
    async calculatePairPrice(){
        let data = this.chartData["A"].map(obj => ({ ...obj, ticker: this.pairStore.A })).concat(this.chartData["B"].map(obj => ({ ...obj, ticker: this.pairStore.B })))
        const hedge_ratio = this.pairStore.pairs[this.pairStore.pair]?.hedge_ratio;
        const reverse = this.pairStore.pairs[this.pairStore.pair]?.reverse;
        //if (!data.value || !data.value.length) return [];
        console.log('data')
        const result = Object.values(
        data.reduce((acc, { time, close, open, high, low, ticker }) => {
        if (!acc[time]) {
            acc[time] = { time, closeA: null, closeB: null };
        }

        if (ticker === this.pairStore.A) {
            acc[time].openA = open;
            acc[time].highA = high;
            acc[time].lowA = low;
            acc[time].closeA = close;
        } else if (ticker === this.pairStore.B) {
            acc[time].openB = open;
            acc[time].highB = high;
            acc[time].lowB = low;
            acc[time].closeB = close;
        }

        if (acc[time].closeA !== null && acc[time].closeB !== null) {
            if (reverse) {
            acc[time].open = acc[time].openB - (acc[time].openA * hedge_ratio);
            acc[time].high = acc[time].highB - (acc[time].highA * hedge_ratio);
            acc[time].low = acc[time].lowB - (acc[time].lowA * hedge_ratio);
            acc[time].close = acc[time].closeB - (acc[time].closeA * hedge_ratio);
            } else {
            acc[time].open = acc[time].openA - (acc[time].openB * hedge_ratio);
            acc[time].high = acc[time].highA - (acc[time].highB * hedge_ratio);
            acc[time].low = acc[time].lowA - (acc[time].lowB * hedge_ratio);
            acc[time].close = acc[time].closeA - (acc[time].closeB * hedge_ratio);
            }
        }

        return acc;
        }, {})
        ).map(
            item => ({
                time: item.time,
                //value: item.close,
                open: item.open,
                high: item.high,
                low: item.low,
                close: item.close,
            })
            );
            //return dataA.value;
            this.chartData["pairPrice"] = result
            return result;
        }
    }
})