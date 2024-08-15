import { defineStore } from "pinia";
import axios from 'axios';
import qs from 'qs';

export const usePairForm = defineStore('pairForm',{
  state:()=>({
    pairs:{},
  }),
  actions:{
    async load(pair){
    	  this.pairs[pair] = {};
        this.pairs[pair].A = pair.split('__')[0]
        this.pairs[pair].B = pair.split('__')[1]

        const data = await this.fetchPairInfo(this.pairs[pair].A, this.pairs[pair].B);
        console.log("DATA")
        this.pairs[pair].reverse = Boolean(data.reverse)
        this.pairs[pair].watchlist = Boolean(data.watchlist)
        this.pairs[pair].hedge_ratio = data.hedge_ratio
        this.pairs[pair].notes = data.notes
	  },
  	get_hedge_ratio(pair){
				return this.pairs[pair]?.hedge_ratio ?? 1
  	},
    set_hedge_ratio(pair, hedge_ratio){
        return this.pairs[pair].hedge_ratio = hedge_ratio
    },
    update_hedge_ratio(pair, hedge_ratio) {
      this.pairs[pair.value].hedge_ratio = hedge_ratio
    },
    update_reverse(pair, reverse) {
      this.pairs[pair.value].reverse = reverse
    },    
    async fetchPairInfo(A, B) {
      try {
        const response = await axios.get('http://localhost:5002/get_pair_info', {
          params: { tickers: [A, B] },
          paramsSerializer: params => {
            return qs.stringify(params, { arrayFormat: 'repeat' });
          }
        });
        return response.data
      } catch (error) {
        console.log(error);
      }
    }
  }
})