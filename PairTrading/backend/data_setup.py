from PairTrading.src import _constant
from PairTrading.backend import _db_constant
from PairTrading.backend.database import DataBase

class DataSetup:
    def __init__(self):
        self.__polygon_db = DataBase(_db_constant.POLYGON_DB)
        self.__yfinance_db = DataBase(_db_constant.YFINANCE_DB)
        self.__user_db = DataBase(_db_constant.USER_DB)

        self.setup_polygon()
        self.setup_yfinance()
        self.setup_user()


    def setup_user(self):
        self.__user_db.setup_table(
            _db_constant.TICKER_RANK_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_RANK_COLUMNS)
        )

        self.__user_db.setup_table(
            _db_constant.PAIR_INFO_TABLE_NAME,
            self._renamed_columns(_constant.PAIR_INFO_COLUMNS)
        )

        self.__user_db.setup_table(
            _db_constant.WATCHLIST_TABLE_NAME,
            self._renamed_columns(_constant.WATCHLIST_COLUMNS)
        )

        self.__user_db.setup_table(
            _db_constant.TRADES_TABLE_NAME,
            self._renamed_columns(_constant.TRADES_COLUMNS)
        )

    def setup_yfinance(self):
        #market_data
        self.__yfinance_db.setup_table(
            _db_constant.MARKET_DATA_TABLE_NAME,
            self._renamed_columns(_constant.MARKET_DATA_COLUMNS)
        )

        self.__yfinance_db.setup_table(
            _db_constant.FAILED_TICKER_TABLE_NAME,
            self._renamed_columns(_constant.FAILED_TICKER_COLUMNS)
        )

    def setup_polygon(self):
        #ticker_details
        self.__polygon_db.setup_table(
            _db_constant.TICKER_INFO_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_DETAILS_COLUMNS)
        )

        #ticker_types
        self.__polygon_db.setup_table(
            _db_constant.TICKER_TYPES_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_TYPES_COLUMNS)
        )

        #grouped_daily
        self.__polygon_db.setup_table(
            _db_constant.MARKET_SNAPSHOT_TABLE_NAME,
            self._renamed_columns(_constant.GROUPED_DAILY_COLUMNS)
        )

    def _renamed_columns(self, columns: dict) -> dict:
         return {v[0]: v[1] for v in columns.values()}

if __name__ == '__main__':
    DataSetup()
