from PairTrading.frontend.data_utils import DataUtils

class Pair():
    def __init__(self, pair=["AA", "AU"]) -> None:
        self._pair = pair
        self._price = 0
        self.ratio = 1
        
    @property
    def price(self):
        return self._price
    
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
    
    def update_price(self):
        d = DataUtils()
        self._price = d.get_last_price(self.a) - d.get_last_price(self.b) * self.ratio
    
    def calculate_order(self):
        d = DataUtils()
        priceA = d.get_last_price(self.a)
        priceB = d.get_last_price(self.b)
        volA = d.get_average_volume(self.a, 30)
        volB = d.get_average_volume(self.b, 30)

        priceVolA = priceA * volA
        priceVolB = priceB * volB

        if priceVolA > priceVolB:
            self.invert()

    def calculate_current_ratio(self):
        d = DataUtils()
        return d.get_last_price(self.a) / d.get_last_price(self.b)

    def invert(self):
        #self.pair[0], self.pair[1] = self.pair[1], self.pair[0]
        self.a, self.b = self.b, self.a
    

    