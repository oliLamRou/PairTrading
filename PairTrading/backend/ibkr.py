import time, datetime
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.client import Contract
import pandas as pd
import queue

from threading import Thread

class IBClient(EWrapper, EClient):
    def __init__(self, host, port, client_id):
        EClient.__init__(self, self)
        self.tick_data_queue = []
        self.connect(host, port, client_id)

        thread = Thread(target=self.run)
        thread.start()

    def error(self, req_id, code, msg):
        if code in [2104, 2106, 2158]:
            print(msg)
        else:
            print(f'Error {code}: {msg}')

    def historicalData(self, req_id, bar):
        print(bar)

    # callback when all historical data has been received
    def historicalDataEnd(self, reqId, start, end):
        print('hist')
        print(f"end of data {start} {end}")

    def tickString(self, reqId, tickType, value):
        if tickType == 76:
            self.tick_data_queue.append({"reqId" : reqId, "tickType" : tickType, "value" : value})
            print(f"Short price: {value}")
        
    def tickSize(self, reqId, tickType, value):
        #Shortable shares
        if tickType == 89:
            self.tick_data_queue.append({"reqId" : reqId, "tickType" : tickType, "value" : value})
            print(f"Shortable Shares: {value}")

    def tickGeneric(self, reqId, tickType, value):
        #print("reqId: ", reqId)
        #Inventory to borrow
        # Value higher than 2.5	:       There are at least 1000 shares available for short selling.
        # Value higher than 1.5 :	    This contract will be available for short selling if shares can be located.
        # 1.5 or less:                  Contract is not available for short selling.
        
        #print(tickType, value)
        if tickType == 46:  # Inventory
            #self.tick_data_queue.put({"tickType" : tickType, "reqId" : reqId, "value" : value})
            self.tick_data_queue.append({"reqId" : reqId, "tickType" : tickType, "value" : value})
            print(f"Available to Borrow: {value}")

    def get_tick_result(self, reqId):
        results = []

        for i, r in enumerate(self.tick_data_queue):
            if r.get("reqId") == reqId:
                results.append(r)
        return results
    

if __name__ == '__main__':
    print("ib init")
    client = IBClient('127.0.0.1', 7497, 0)
    
    time.sleep(0.3)

    contract = Contract()
    contract.symbol = 'AAPL'
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    what_to_show = 'TRADES'

    client.reqMktData(3, contract, "47,236", False, False, [])
    time.sleep(0.8)
    q = client.get_tick_result(3)
    print(q)
    print(client.asynchronous)
    #print(client.tick_data_queue)

    # client.reqHistoricalData(
    #     2, contract, '', '20 Y', '1 day', what_to_show, True, 2, False, []
    # )
    
    time.sleep(3)
    client.disconnect()
