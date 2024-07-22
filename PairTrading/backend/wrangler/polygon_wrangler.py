import pandas as pd
import warnings

from PairTrading.backend.database import DataBase
from PairTrading.src import _constant
from PairTrading.backend import _db_constant

class PolygonWrangler:
    def __init__(self):
        self.__polygon_db = DataBase(_db_constant.POLYGON_DB)

        #Properties
        self._all_ticker_info = pd.DataFrame()
        self._all_market_data = pd.DataFrame()
        self._sic_code = pd.DataFrame()
        self._ticker_types = pd.DataFrame()
        self._market_snapshot = pd.DataFrame()
        
    @property
    def sic_code(self):
        if self._sic_code.empty:
            self._sic_code = self.__polygon_db.get_table(_db_constant.SIC_CODE_TABLE_NAME)
        
        return self._sic_code

    @property
    def all_ticker_info(self):
        if self._all_ticker_info.empty:
            self._all_ticker_info = self.__polygon_db.get_table(_db_constant.TICKER_INFO_TABLE_NAME)

        return self._all_ticker_info

    #MARKET
    def market_snapshot(self,
            update: bool = False
        ) -> pd.DataFrame():

        if update:
            print(f"--> Clearing and downloading: {_db_constant.MARKET_SNAPSHOT_TABLE_NAME}\n")
            self.__polygon_db.clear_table(_db_constant.MARKET_SNAPSHOT_TABLE_NAME)
            
            results = self.grouped_daily()
            for result in results:
                self.__polygon_db.add_row(_db_constant.MARKET_SNAPSHOT_TABLE_NAME, result)

        if self._market_snapshot.empty:
            self._market_snapshot = self.__polygon_db.get_table(_db_constant.MARKET_SNAPSHOT_TABLE_NAME)

        return self._market_snapshot

    def ticker_info(self,
            ticker: str,
            update: bool = False
        ) -> pd.DataFrame():

        #Do when not exists in DB or Update is True
        if not self.__polygon_db.has_value(
                _db_constant.TICKER_INFO_TABLE_NAME, 'ticker', ticker
                ) or update:

            results = self.ticker_details(ticker)
            if not results:
                return

            print('{} --> {}: {} ...\n'.format(
                _db_constant.TICKER_INFO_TABLE_NAME, 
                "Updating" if update else "Adding", 
                " ".join(str(r) for r in results.values())[:60]
                )
            )
            if update:
                self.__polygon_db.update_row(_db_constant.TICKER_INFO_TABLE_NAME, results, 'ticker', ticker)
            else:
                self.__polygon_db.add_row(_db_constant.TICKER_INFO_TABLE_NAME, results)

            #Reload table
            self._all_ticker_info = self.__polygon_db.get_table(_db_constant.TICKER_INFO_TABLE_NAME)

        return self.all_ticker_info[self.all_ticker_info.ticker == ticker]

if __name__ == '__main__':
    pw = DataWrangler()
