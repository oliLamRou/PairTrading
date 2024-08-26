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

    def next_id(self):
        self.current_id += 1
        return self.current_id

    def error(self, req_id, code, msg):
        if code in [2104, 2106, 2158]:
            print(msg)
        else:
            print(f'Error {code}: {msg}')

    def tickPrice(self, req_id, tickType, price, attrib):
        self.add_to_data(req_id, {'tickType' : TickTypeEnum.to_str(tickType), 'price': price})
        print(f"Tick Price. Request Id: {req_id}, tickType: {TickTypeEnum.to_str(tickType)}, Price: {price}")

    def tickSize(self, reqId, tickType, size):
        print(f"Tick Size. Ticker Id: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, Size: {size}")

    def historicalData(self, req_id, bar):
        if len(bar.date.split("  ")) == 2:
            format = "%Y%m%d %H:%M:%S"
        else:
            format = "%Y%m%d"
        try:
            data = {
                'time': int(datetime.datetime.strptime(bar.date, format).timestamp()),
                'open': bar.open,
                'high': bar.high,
                'low': bar.low,
                'close': bar.close,
                'volume': bar.volume,
            }
        except:
            data = {'time': 0, 'open': 0,'high': 0,'low': 0,'close': 0,'volume': 0}
            
        self.add_to_buffer(req_id, data)

    # callback when all historical data has been received
    def historicalDataEnd(self, req_id, start, end):
        self.buffer_to_data(req_id)
        print(f"end of data {start} {end}")

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        data = {'status': status, 'filled': filled, 'remaining': remaining, 'avgFillPrice': avgFillPrice}
        self.add_to_data(orderId, data)
        print(f"Order Status - ID: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}, AvgFillPrice: {avgFillPrice}")
    
    def openOrder(self, orderId, contract, order, orderState):
        data = {'orderId': orderId, 
                'ticker': contract.symbol, 
                'exchange': contract.exchange,
                'action':order.action,
                'orderType': order.orderType,
                'quantity': order.totalQuantity,
                'status': orderState.status
                }
        self.add_to_data(orderId, data)
        print(f"Open Order - ID: {orderId}, Symbol: {contract.symbol}, SecType: {contract.secType}, Exchange: {contract.exchange}, Action: {order.action}, OrderType: {order.orderType}, TotalQty: {order.totalQuantity}, Status: {orderState.status}")

    def execDetails(self, req_id, contract, execution):
        print(f"Execution Details - ID: {req_id}, Symbol: {contract.symbol}, SecType: {contract.secType}, Exchange: {contract.exchange}, Action: {execution.side}, Shares: {execution.shares}, Price: {execution.price}")

    #Data handling, will need to use proper queue
    def add_to_buffer(self, req_id, data):
        if not self._data_buffer.get(req_id):
            print('create id buffer')
            self._data_buffer[req_id] = [data]
        else:
            self._data_buffer[req_id].append(data)

    def buffer_to_data(self, req_id, clear=True):
        self._data_queue[req_id] = self._data_buffer.get(req_id, []).copy()
        if clear:
            self._data_buffer[req_id].clear()

    def add_to_data(self, req_id, data):
        if not self._data_queue.get(req_id):
            print('create id buffer')
            self._data_queue[req_id] = [data]
        else:
            self._data_queue[req_id].append(data)
    
    def get_data(self, req_id, clear = True):
        if clear:
            data = self._data_queue.pop(req_id, [])
        else:
            data = self._data_queue.get(req_id, [])
            
        return data
        
if __name__ == '__main__':
    print("ib init")
    client = IBClient('127.0.0.1', 7497, 0)
    time.sleep(2)
