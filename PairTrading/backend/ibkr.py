import time, datetime
from ibapi.client import EClient
from ibapi.common import TagValueList, TickerId
from ibapi.wrapper import EWrapper
from ibapi.client import Contract
from ibapi.ticktype import TickTypeEnum
import threading
from ib_insync import *
import asyncio

class IBClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, wrapper=self)
        self.current_id = 0
        self._nextOrderId = None  # Will store the next valid order ID
        self._live_data_ids = {}
        self._data_buffer = {}
        self._data_queue = {}
        self.mktDataCallback: function = None

    @property
    def nextOrderId(self):
        self._nextOrderId += 1
        return self._nextOrderId

    def next_id(self):
        self.current_id += 1
        return self.current_id
    
    def nextValidId(self, orderId):
        #Callback function that is called with the next valid order ID
        print(f"Next valid order ID: {orderId}")
        self._nextOrderId = orderId

    def error(self, req_id, code, msg):
        if code in [2104, 2106, 2158]:
            print(msg)
        else:
            print(f'Error {code}: {msg}')

    def tickPrice(self, req_id, tickType, price, attrib):
        data = [{'req_id': req_id, 'tickType' : TickTypeEnum.to_str(tickType), 'price': price}]
        if self.mktDataCallback is not None:
            self.mktDataCallback(data)

        #self.add_to_data(req_id, {'tickType' : TickTypeEnum.to_str(tickType), 'price': price})
        #print(f"Tick Price. Request Id: {req_id}, tickType: {TickTypeEnum.to_str(tickType)}, Price: {price}")

    def tickSize(self, req_id, tickType, size):
        data = [{'req_id': req_id, 'tickType' : TickTypeEnum.to_str(tickType), 'size': size}]
        if self.mktDataCallback is not None:
            self.mktDataCallback(data)    
        #print(f"Tick Size. Ticker Id: {req_id}, tickType: {TickTypeEnum.to_str(tickType)}, Size: {size}")
    
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"Order Status - ID: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}, Avg Fill Price: {avgFillPrice}")

    def openOrder(self, orderId, contract, order, orderState):
        print(f"Open Order - ID: {orderId}, Symbol: {contract.symbol}, Action: {order.action}, OrderType: {order.orderType}, Quantity: {order.totalQuantity}")

    def execDetails(self, reqId, contract, execution):
        print(f"Execution Details - OrderID: {reqId}, Symbol: {contract.symbol}, Shares: {execution.shares}, Price: {execution.price}")


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

    def reqMktData(self, reqId: TickerId, contract: Contract, genericTickList: str, snapshot: bool, regulatorySnapshot: bool, mktDataOptions: TagValueList):
        self._live_data_ids[reqId] = contract.symbol
        print('Req market data, ', self._live_data_ids)
        return super().reqMktData(reqId, contract, genericTickList, snapshot, regulatorySnapshot, mktDataOptions)
    
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

    def cancelLiveData(self):
        for k, v in self._live_data_ids.items():
            self.cancelMktData(k)
            print(f'cancel stream {k}, ticker is {v}')
        
        time.sleep(0.05)
        self._live_data_ids.clear()

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
    ib = IBClient()
    ib.connect('127.0.0.1', 7497, 1)
    
    thread = threading.Thread(target=ib.run, daemon=True)
    thread.start()

    contract = Stock('NVDA', 'SMART', 'USD')
    time.sleep(1)
    ib.reqMktData(1, contract, '', False, False, [])
    

    #ticker.updateEvent += onMarketDataUpdate

    # def run_ib_loop():
    #     loop = util.getLoop()
    #     asyncio.set_event_loop(loop)
    
    #ib.run()

    # Keep the event loop running
    #ib.run()
    print('what')
    for i in range(0, 10):
        print(i)
        time.sleep(3)
    print(ticker.marketPrice())
