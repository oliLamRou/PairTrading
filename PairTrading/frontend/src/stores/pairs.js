import { defineStore } from "pinia";
import { useRoute } from 'vue-router'
import axios from 'axios';
import qs from 'qs';

export const usePairForm = defineStore('pairForm',{
  state:()=>({
    route: useRoute(),
    pairs:{},
  }),
  getters: {
    pair() { return this.route.params.pair },
    A() { return this.pair.split('__')[0] },      
    B() { return this.pair.split('__')[1] },
  },
  actions:{
    async fetch_market_data(){
      try {
        const response = await axios.get('http://localhost:5002/get_market_data', {
          params: { tickers: [this.A,this.B] },
          paramsSerializer: params => {
            return qs.stringify(params, { arrayFormat: 'repeat' });
          }
        });
        this.pairs[this.pair].data = response.data;
      } catch (error) {
        console.log(error);
      }
    },

    async load(){
    	  this.pairs[this.pair] = {A: this.A, B: this.B};
        const data = await this.fetchPairInfo(this.pairs[this.pair].A, this.pairs[this.pair].B);
        this.pairs[this.pair] = {
          A:            data.A            ? data.A                    : this.A,
          B:            data.B            ? data.B                    : this.B,
          watchlist:    data.watchlist    ? data.watchlist !== null   : false,
          reverse:      data.reverse      ? data.reverse !== null     : false,
          hedge_ratio:  data.hedge_ratio  ? data.hedge_ratio          : 1,
          notes:        data.notes,
          period:       data.period       ? data.period               : 20,
          std_dev:      data.std_dev      ? data.std_dev              : 2,
        }
        this.fetch_market_data()
	  },
    async fetchPairInfo(A, B) {
      try {
        const response = await axios.get('http://localhost:5002/get_pair_info', {
          params: { tickers: this.pair.split('__') },
          paramsSerializer: params => {
            return qs.stringify(params, { arrayFormat: 'repeat' });
          }
        });
        return response.data
      } catch (error) {
        console.log(error);
      }
    },

    async save(){
      console.log('HERE', this.pairs[this.pair])
      try {
        const response = await axios.post('http://localhost:5002/update_pair_info', {
          pairInfo: this.pairs[this.pair]
        });
        console.log('updated', response.data)
      } catch (error) {
        console.log(error);
      }
    },

    update_hedge_ratio(hedge_ratio) {
      this.pairs[this.pair].hedge_ratio = hedge_ratio
    },
    update_reverse(reverse) {
      this.pairs[this.pair].reverse = reverse
    },
    update_watchlist(watchlist) {
      this.pairs[this.pair].watchlist = watchlist
    },    
    update_notes(notes) {
      this.pairs[this.pair].notes = notes
    },    
    update_period(period) {
      this.pairs[this.pair].period = period
    },
    update_std_dev(std_dev) {
      this.pairs[this.pair].std_dev = std_dev
    },
  }
})