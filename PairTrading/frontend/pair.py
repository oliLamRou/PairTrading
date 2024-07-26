from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.backend.data_wrangler import DataWrangler
import ast

class Pair():
    def __init__(self, pair: list = ["", ""], hedge_ratio=1):
        self._pair = pair
        
        if self._pair:
            self.pair_info = self.fetch_saved_info()
        else:
            self.pair_info = {}
            self.hedge_ratio = hedge_ratio
            self.reverse = 0
            self.watchlist = 0
            self.notes = ""
            self.trade_history = []
            self.position = 0

    @property
    def a(self):
        return self._pair[0]
    
    @a.setter
    def a(self, value):
        self._pair[0] = value
    
    @property
    def b(self):
        return self._pair[1]
    
    @b.setter
    def b(self, value):
        self._pair[1] = value
    
    def set_pair(self, pair):
        self._pair = pair
        self.pair_info = self.fetch_saved_info()

    def fetch_saved_info(self):
        dw = DataWrangler()
        pair_info = dw.get_pair_info([self.a, self.b]).fillna(0).to_dict()

        #Default values
        self.hedge_ratio = 1 if pair_info.get("hedge_ratio") is None else pair_info.get("hedge_ratio")
        self.reverse = 0 if pair_info.get("reverse") is None else pair_info["reverse"]
        self.watchlist = 0 if pair_info.get("watchlist") is None else pair_info["watchlist"]
        self.notes = "" if pair_info.get("notes") is None else pair_info["notes"]
        self.trade_history = [] #ast.literal_eval(pair_info.get("trade_history", "[]"))
        self.position = 0 if pair_info.get("position") is None else pair_info["position"]
        return pair_info

    def save_pair_info(self):
        dw = DataWrangler()
        info = {"hedge_ratio": self.hedge_ratio, "reverse" : self.reverse, "watchlist" : self.watchlist, 
                "notes" : self.notes, "trade_history" : str(self.trade_history), "position" : self.position}
        
        return dw.update_pair_info([self.a, self.b], info)
        
    def get_price(self):
        if self.reverse:
            pair_price = du.get_last_price(self.b) - (du.get_last_price(self.a) * self.hedge_ratio)
        else:
            pair_price = du.get_last_price(self.a) - (du.get_last_price(self.b) * self.hedge_ratio)
        return pair_price


    

    

    