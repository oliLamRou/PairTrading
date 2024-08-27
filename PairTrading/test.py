from ib_insync import *
import threading
import asyncio

# Initialize the IB connection
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define the contract for Apple stock
contract = Stock('AAPL', 'SMART', 'USD')

# Function to handle market data updates
def onMarketDataUpdate(ticker):
    print(f"Market Data Updated: Last price: {ticker.last}, Bid: {ticker.bid}, Ask: {ticker.ask}")

# Request market data and subscribe to events
ticker = ib.reqMktData(contract, '', False, False)
ticker.updateEvent += onMarketDataUpdate

# Function to run the event loop in a separate thread
def run_ib_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    ib.run()

# Start the event loop in a separate thread
thread = threading.Thread(target=run_ib_loop, daemon=True)
thread.start()

# Your main application code can continue running here
print("Main application is still responsive while IB event loop is running.")

# Example: Performing some other task while the event loop is running
import time
while True:
    print("Doing other tasks...")
    time.sleep(5)