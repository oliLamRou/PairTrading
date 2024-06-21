import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
from PairTrading.polygon import Polygon
import math

class Filter(Polygon):
    def __init__(self):
        super().__init__()
        self._stocks = None

    def normalize_it(self,
            df: pd.DataFrame()
            ) -> pd.DataFrame():

        min_val = df.c.min()
        max_val = df.c.max()
        df.c = df.c.apply(
            lambda x: (x - min_val) / (max_val - min_val)
        )
        return df

    def get_pair_df(self,
            pair: tuple,
            column: str='c',
            ) -> pd.DataFrame():

        df1 = pd.read_csv(f'../data/historical/{pair[0]}.csv')[['t', column]]
        df1 = self.normalize_it(df1)

        df2 = pd.read_csv(f'../data/historical/{pair[1]}.csv')[['t', column]]
        df2 = self.normalize_it(df2)
        
        return df1.merge(df2, on='t')

    def filter(self,
            min_price: int, 
            max_price: int,
            min_avg_vol: int,
            max_avg_vol: int
            ) -> list:

        stocks = []
        for filename in os.listdir('../data/historical'):
            symbol = '.'.join(filename.split('.')[:-1])
            df = pd.read_csv(f'../data/historical/{symbol}.csv')
            if df.c.iloc[-1] < min_price or df.c.iloc[-1] > max_price:
                continue

            if df.v[-30:].mean() < min_avg_vol or df.v[-30:].mean() > max_avg_vol:
                continue

            stocks.append(symbol)

        stocks.sort()
        return stocks

    def sector(self):
        df = pd.DataFrame

    def get_mosaic(self, save: bool=False):
        filtered_stocks = self.filter(20, 120, 500000, 5000000)[:10]
        print(filtered_stocks)
        pairs = list(itertools.combinations(filtered_stocks, 2))
        num_pairs = len(pairs)

        n_col = math.ceil(math.sqrt(num_pairs))
        n_row = math.ceil(num_pairs / n_col)
        fig, axes = plt.subplots(n_row, n_col, figsize=(10, 7.5))
        xi = 0
        yi = 0
        
        for i in range(num_pairs):
            #Pairing
            pair = pairs[i]
            pair_df = self.get_pair_df(pair)

            #Line Plot
            sns.lineplot(
                pair_df[['c_x', 'c_y']], ax=axes[xi, yi], legend=False
                ).set(
                    title='-'.join(pair), xticklabels=[], yticklabels=[]
                )

            #Index
            if yi < n_col - 1:
                yi += 1
            else:
                xi += 1
                yi = 0

        if save:
            plt.savefig('./mosaic.jpeg', format='jpeg')
        plt.show()


if __name__ == '__main__':
    f = Filter()
    f.
    # f.get_mosaic()





#------------------------------------------

# def get_avg(stock):
#   close = pd.read_csv(f'../data/historical/{stock}.csv')['c']
#   min_val = close.min()
#   max_val = close.max()
#   normalized = ((close - min_val) / (max_val - min_val)).mean().round(2)
#   return normalized

# avg = [get_avg(stock) for stock in stocks]
# avg_array = np.array(avg)

# # Calculate the difference using broadcasting
# diff_matrix = avg_array[:, np.newaxis] - avg_array

# # Convert the result back to a DataFrame if desired
# df = pd.DataFrame(diff_matrix, columns=stocks, index=stocks)

# pair_df = pd.DataFrame()
# for stock in stocks:
#   close = pd.read_csv(f'../data/historical/{stock}.csv')[['t', 'c']]

#   min_val = close.c.min()
#   max_val = close.c.max()
#   close.c = close.c.apply(
#       lambda x: (x - min_val) / (max_val - min_val)
#   )

#   close = close.rename(columns={'c': stock})

#   if pair_df.empty:
#       pair_df = close.copy()
#       continue

#   pair_df = pair_df.merge(close, on='t')

# # plt.show()
# # heatmap = sns.heatmap(df, cmap='coolwarm')

# #Get recent data
# #Get sector list
# #mosaic pair chart