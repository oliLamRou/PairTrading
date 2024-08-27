import { defineStore } from "pinia";
import axios from 'axios';
import qs from 'qs';

export const useIbkr = defineStore('ibkr',{
  state:()=>({
    connectionId: 0,
    marketData: []
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
            console.log("req live data, req_id: ", response.data)
            return response.data
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
  }
})