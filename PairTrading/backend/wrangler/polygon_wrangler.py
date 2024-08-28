import pandas as pd

from PairTrading.backend import polygon_session, polygon_engine
from PairTrading.backend.models import SicCode, TickerDetails, MarketSnapshot
from PairTrading.backend.polygon import Polygon

class PolygonWrangler(Polygon):
    def __init__(self):
        Polygon.__init__(self)

        #Properties
        self._all_ticker_info = pd.DataFrame()
        self._sic_code = pd.DataFrame()
        self._market_snapshot = pd.DataFrame()

    @property
    def sic_code(self) -> pd.DataFrame():
        if self._sic_code.empty:
            query = polygon_session.query(SicCode)
            self._sic_code = pd.read_sql_query(query.statement, polygon_engine)
        
        return self._sic_code

    @property
    def all_ticker_info(self) -> pd.DataFrame():
        if self._all_ticker_info.empty:
            query = polygon_session.query(TickerDetails)
            self._all_ticker_info = pd.read_sql_query(query.statement, polygon_engine)

        return self._all_ticker_info
        
    def market_snapshot(self, update: bool = False) -> pd.DataFrame():
        if update:
            polygon_session.query(MarketSnapshot).delete()
            print(self._grouped_daily())
            polygon_session.bulk_insert_mappings(MarketSnapshot, self._grouped_daily())
            polygon_session.commit()

        if self._market_snapshot.empty:
            query = polygon_session.query(MarketSnapshot)
            self._market_snapshot = pd.read_sql_query(query.statement, polygon_engine)

        return self._market_snapshot

    def ticker_info(self, ticker: str, update: bool = False) -> pd.DataFrame():
        #Check if ticker is in TickerDetails table
        has_value = polygon_session.query(
            polygon_session.query(TickerDetails).filter_by(ticker=ticker).exists()
            ).scalar()

        if update or not has_value:
            results = self._ticker_details(ticker)
            if not results:
                return

            if update:
                polygon_session.query(TickerDetails).filter_by(ticker=ticker).update(results)
            else:
                polygon_session.query(TickerDetails).add(results)

            polygon_session.commit()

            query = polygon_session.query(TickerDetails)
            self._all_ticker_info = pd.read_sql_query(query.statement, polygon_engine)

        #TODO: this could be done with filter instead of calling the whole table
        return self.all_ticker_info[self.all_ticker_info.ticker == ticker]

if __name__ == '__main__':
    pw = PolygonWrangler()
    # rows = polygon_session.query(MarketSnapshot)
    df = pw.ticker_info('MSTR')
    print(df)