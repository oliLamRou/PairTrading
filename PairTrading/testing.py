import configparser

from PairTrading.src.utils import PROJECT_ROOT
from PairTrading.src import _constant


AGGREGATES_COLUMNS = {
    'c': ['close', 'REAL'],
    'h': ['high', 'REAL'],
    'l': ['low', 'REAL'],
    'n': ['n_transaction', 'INTERGER'],
    'o': ['open', 'REAL'],
    't': ['timestamp', 'INTERGER'],
    'v': ['volume', 'INTERGER'],
    'vw': ['volume_weighted', 'REAL'],
    'otc': ['otc', 'INTERGER']
}


# B = ?, C = ?
# print('=?, '.join(AGGREGATES_COLUMNS.keys()) + '=?')
v = list(AGGREGATES_COLUMNS.keys())
v.append('d')
print(tuple(v))
