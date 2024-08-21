import time, datetime
from ibapi.client import EClient
from ibapi.common import TagValueList, TickerId
from ibapi.wrapper import EWrapper
from ibapi.client import Contract
from ibapi.ticktype import TickTypeEnum


class IBClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, wrapper=self)
        self.current_id = 0
        self._data_buffer = {}
        self._data_queue = {}
        self.historical_data_buffer = []
        self.historical_data = []

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def error(self, req_id, code, msg):
        if code in [2104, 2106, 2158]:
            print(msg)
        else:
            print(f'Error {code}: {msg}')

    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. Ticker Id: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, Price: {price}")

    def tickSize(self, reqId, tickType, size):
        print(f"Tick Size. Ticker Id: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, Size: {size}")

    def historicalData(self, req_id, bar):
        data = {
            'time': int(datetime.datetime.strptime(bar.date, "%Y%m%d %H:%M:%S").timestamp()),
            'open': bar.open,
            'high': bar.high,
            'low': bar.low,
            'close': bar.close,
            'volume': bar.volume
        }
        self.historical_data_buffer.append(data)

    # callback when all historical data has been received
    def historicalDataEnd(self, req_id, start, end):
        self.historical_data = self.historical_data_buffer.copy()
        self.historical_data_buffer.clear()
        #print(self.historical_data)
        print('end of historical data')
        print(f"end of data {start} {end}")
   
    #Data handling, will need to use proper queue
    def add_to_buffer(self, req_id, data):
        if self._data_buffer.get(req_id, False):
            self._data_buffer[req_id].append(data)
        else:
            self._data_buffer[req_id] = [data]

    def buffer_to_data(self, req_id, clear=True):
        self._data_queue[req_id] = self._data_buffer.get(req_id, []).copy()
        if clear:
            self._data_buffer[req_id].clear()
        
if __name__ == '__main__':
    print("ib init")
    client = IBClient('127.0.0.1', 7497, 0)
    time.sleep(2)
