import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint, adfuller

import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller

import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="whitegrid")

from PairTrading.backend.scanner import Scanner

s = Scanner()
s.min_price = 5
s.max_price = 100
s.industry = 'CRUDE PETROLEUM & NATURAL GAS'

def find_cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j]))
    return score_matrix, pvalue_matrix, pairs


# print(s.potential_pair[s.potential_pair.potential_pair < 10000])
# pairs = s.get_pairs
# # print(list(set(pairs.A.to_list())))
# tickers = ['CRC', 'EQT', 'GTE', 'SOC', 'MGY', 'BSM', 'GRNT', 'CHK', 'SD', 'CRGY', 'MTDR', 'CNX', 'VOC', 'EPM', 'AESI', 'TELZ', 'CIVI', 'OVV', 'NOG', 'STR', 'VNOM', 'MUR', 'KOS', 'CTRA', 'KRP', 'RRC', 'CRK', 'VTLE', 'MRO', 'HESM', 'MNR', 'ROCLU', 'APA', 'CKX', 'OXY', 'EP', 'SBOW', 'AR', 'SWN', 'REPX', 'MXC', 'TXO', 'PROP', 'DVN', 'EGY', 'BRY', 'MVO', 'TALO', 'PR', 'AMPY', 'DMLP', 'EPSN', 'SM', 'PARR']

# df = s.market_data(tickers)
# df = df.pivot(index='date', columns='ticker', values='close')
# print(df)

# scores, pvalues, pairs = find_cointegrated_pairs(df.fillna(0))

# fig, ax = plt.subplots(figsize=(10,10))
# sns.heatmap(pvalues, xticklabels=tickers, yticklabels=tickers, cmap='RdYlGn_r' 
#                 , mask = (pvalues >= 0.05)
#                 )
# print(pairs)
# plt.show()

# cointtt = [('AESI', 'CHK'), ('AESI', 'DVN'), ('AMPY', 'MXC'), ('APA', 'TALO'), ('AR', 'CNX'), ('BSM', 'HESM'), ('BSM', 'KOS'), ('BSM', 'SD'), ('BSM', 'VNOM'), ('BSM', 'VOC'), ('CHK', 'CTRA'), ('CHK', 'OXY'), ('CKX', 'ROCLU'), ('CNX', 'GTE'), ('CNX', 'KRP'), ('CNX', 'PARR'), ('CRC', 'EPM'), ('CRC', 'REPX'), ('CRC', 'TALO'), ('CRC', 'VOC'), ('CRGY', 'CRK'), ('CRGY', 'DMLP'), ('CRGY', 'EP'), ('CRGY', 'EPM'), ('CRGY', 'EQT'), ('CRGY', 'GRNT'), ('CRGY', 'MNR'), ('CRGY', 'MVO'), ('CRGY', 'MXC'), ('CRGY', 'REPX'), ('CRGY', 'SBOW'), ('CRGY', 'SD'), ('CRGY', 'TELZ'), ('CRGY', 'TXO'), ('CTRA', 'DVN'), ('CTRA', 'EPSN'), ('CTRA', 'MXC'), ('CTRA', 'NOG'), ('DMLP', 'KOS'), ('DVN', 'NOG'), ('DVN', 'OVV'), ('DVN', 'OXY'), ('EP', 'HESM'), ('EP', 'KOS'), ('EP', 'PR'), ('EP', 'VNOM'), ('EPSN', 'MRO'), ('EPSN', 'MXC'), ('EPSN', 'REPX'), ('EPSN', 'SBOW'), ('GRNT', 'MXC'), ('GRNT', 'SBOW'), ('GRNT', 'STR'), ('GRNT', 'TXO'), ('HESM', 'KOS'), ('HESM', 'MVO'), ('HESM', 'VNOM'), ('HESM', 'VOC'), ('KOS', 'MNR'), ('KOS', 'MVO'), ('KOS', 'VNOM'), ('KOS', 'VOC'), ('KRP', 'MVO'), ('KRP', 'PARR'), ('KRP', 'RRC'), ('MTDR', 'OVV'), ('MVO', 'VNOM'), ('MVO', 'VOC'), ('MXC', 'NOG'), ('NOG', 'STR'), ('PROP', 'RRC'), ('REPX', 'SBOW'), ('REPX', 'STR'), ('SD', 'TALO'), ('STR', 'VTLE')]

# print(pairs[pairs.avg_diff < 0.2])
# print(cointtt)

# S1 = sm.add_constant(S1)
# results = sm.OLS(S2, S1).fit()
# S1 = S1['ADBE']
# b = results.params['ADBE']


#PVALUE
S1 = s.market_data(['DRVN'], start='2019-01-01', update=False).set_index('date').close
S2 = s.market_data(['MNRO'], start='2019-01-01', update=False).set_index('date').close
S1.plot()
S2.plot()
plt.show()

score, pvalue, _ = coint(S1, S2)
print(score, pvalue)

#SPREAD
results = sm.OLS(S2, sm.add_constant(S1)).fit()
b = results.params['const']

spread = S2 - b * S1
spread.plot(figsize=(12,6))
plt.axhline(spread.mean(), color='black')
# plt.xlim('2019-01-01', '2024-07-01')
plt.legend(['Spread'])
plt.show()


ratio = S1/S2
ratio.plot(figsize=(12,6))
plt.axhline(ratio.mean(), color='black')
# plt.xlim('2013-01-01', '2018-01-01')
plt.legend(['Price Ratio'])
plt.show()

def zscore(series):
    return (series - series.mean()) / np.std(series)

zscore(ratio).plot(figsize=(12,6))
plt.axhline(zscore(ratio).mean())
plt.axhline(1.0, color='red')
plt.axhline(-1.0, color='green')
# plt.xlim('2013-01-01', '2018-01-01')
plt.show()