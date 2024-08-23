import { defineStore } from "pinia";
import axios from 'axios';
import qs from 'qs';

export const useIbkr = defineStore('ibkr',{
  state:()=>({
    connectionId: 0,
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
    async registerLiveData(){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_register_live_data');
        } catch (error) {
        console.error(error);
        }
    },
    async getMarketData(tickerArg){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_get_market_data', {
                params: {ticker: tickerArg}
            });
            console.log(response.data)
            return response.data
        } catch (error) {
        console.error(error);
        }
    },
    async getHistoricalData(tickerArg, size, length){
        try {
            const response = await axios.get('http://localhost:5002/ibkr_get_historical_data', {
                params: {
                    ticker: tickerArg,
                    size: size,
                    length: length
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