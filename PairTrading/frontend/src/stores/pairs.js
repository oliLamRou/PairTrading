import { defineStore } from "pinia";

export const usePairForm = defineStore('pairForm',{
  state:()=>({
    pairs:{},
  }),
  actions:{
      add(pair){
    	  this.pairs[pair] = {'hedge_ratio': 70}
	  },
    	get_hedge_ratio(pair){
				return this.pairs[pair].get(hedge_ratio)
  	}
	}
})