import os
import time
import pandas as pd
import numpy as np
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.backend.scanner import Scanner
import math
import matplotlib.pyplot as plt
import itertools
import yfinance as yf


s = Scanner()
s.min_price = 2
s.max_price = 200
s.min_vol = 100
tickers = s.snapshot_filter
for ticker in tickers:
	if (ticker+'.csv') in os.listdir('../data/yfinance'):
		continue

	data = yf.download(ticker, start="2023-07-09", end="2024-07-09")
	if data.empty:
		continue

	print(ticker)
	data.reset_index().to_csv(f'../data/yfinance/{ticker}.csv', index=False)
	time.sleep(0.1)



# sbux = yf.Ticker("SBUX")
# x = sbux.info
# print(x)
# a = {'address1': '2401 Utah Avenue South', 'city': 'Seattle', 'state': 'WA', 'zip': '98134', 'country': 'United States', 'phone': '206 447 1575', 'website': 'https://www.starbucks.com', 'industry': 'Restaurants', 'industryKey': 'restaurants', 'industryDisp': 'Restaurants', 'sector': 'Consumer Cyclical', 'sectorKey': 'consumer-cyclical', 'sectorDisp': 'Consumer Cyclical', 'longBusinessSummary': "Starbucks Corporation, together with its subsidiaries, operates as a roaster, marketer, and retailer of coffee worldwide. The company operates through three segments: North America, International, and Channel Development. Its stores offer coffee and tea beverages, roasted whole beans and ground coffees, single serve products, and ready-to-drink beverages; and various food products, such as pastries, breakfast sandwiches, and lunch items. The company also licenses its trademarks through licensed stores, and grocery and foodservice accounts. The company offers its products under the Starbucks Coffee, Teavana, Seattle's Best Coffee, Ethos, Starbucks Reserve, and Princi brands. Starbucks Corporation was founded in 1971 and is based in Seattle, Washington.", 'fullTimeEmployees': 381000, 'companyOfficers': [{'maxAge': 1, 'name': 'Mr. Laxman  Narasimhan', 'age': 55, 'title': 'CEO & Director', 'yearBorn': 1968, 'fiscalYear': 2023, 'totalPay': 4886577, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Rachel  Ruggeri', 'age': 53, 'title': 'Executive VP, CFO & Principal Accounting Officer', 'yearBorn': 1970, 'fiscalYear': 2023, 'totalPay': 2166091, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Bradley E. Lerman', 'age': 66, 'title': 'Executive VP & Chief Legal Officer', 'yearBorn': 1957, 'fiscalYear': 2023, 'totalPay': 1080829, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Michael A. Conway', 'age': 56, 'title': 'Chief Executive Officer of North America', 'yearBorn': 1967, 'fiscalYear': 2023, 'totalPay': 2636118, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Sara  Kelly', 'age': 43, 'title': 'Executive VP & Chief Partner Officer', 'yearBorn': 1980, 'fiscalYear': 2023, 'totalPay': 1993152, 'exercisedValue': 726408, 'unexercisedValue': 379987}, {'maxAge': 1, 'name': 'Mr. Bao Giang Val Bauduin', 'age': 47, 'title': 'Senior VP of Corporate Finance', 'yearBorn': 1976, 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Deborah L. Hall Lefevre', 'age': 55, 'title': 'Executive VP & CTO', 'yearBorn': 1968, 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Tiffany  Willis', 'title': 'Vice President of Investor Relations & ESG Engagement', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Ashish  Mishra', 'title': 'Senior VP, Deputy General Counsel and Chief Ethics & Compliance Officer', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Dominic  Carr', 'title': 'Executive VP & Chief Communications Officer', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}], 'auditRisk': 4, 'boardRisk': 1, 'compensationRisk': 2, 'shareHolderRightsRisk': 2, 'overallRisk': 1, 'governanceEpochDate': 1719792000, 'compensationAsOfEpochDate': 1703980800, 'irWebsite': 'http://investor.starbucks.com/phoenix.zhtml?c=99518&p=irol-IRHome', 'maxAge': 86400, 'priceHint': 2, 'previousClose': 74.57, 'open': 74.63, 'dayLow': 72.73, 'dayHigh': 74.64, 'regularMarketPreviousClose': 74.57, 'regularMarketOpen': 74.63, 'regularMarketDayLow': 72.73, 'regularMarketDayHigh': 74.64, 'dividendRate': 2.28, 'dividendYield': 0.0313, 'exDividendDate': 1723766400, 'payoutRatio': 0.6061, 'fiveYearAvgDividendYield': 1.99, 'beta': 0.935, 'trailingPE': 20.04132, 'forwardPE': 17.874693, 'volume': 11760954, 'regularMarketVolume': 11760954, 'averageVolume': 12588570, 'averageVolume10days': 10126180, 'averageDailyVolume10Day': 10126180, 'bid': 72.7, 'ask': 77.05, 'bidSize': 1400, 'askSize': 100, 'marketCap': 84465664000, 'fiftyTwoWeekLow': 71.8, 'fiftyTwoWeekHigh': 107.66, 'priceToSalesTrailing12Months': 2.312221, 'fiftyDayAverage': 78.5014, 'twoHundredDayAverage': 90.1765, 'trailingAnnualDividendRate': 2.24, 'trailingAnnualDividendYield': 0.03003889, 'currency': 'USD', 'enterpriseValue': 104493924352, 'profitMargins': 0.11382, 'floatShares': 1108222353, 'sharesOutstanding': 1132700032, 'sharesShort': 22770629, 'sharesShortPriorMonth': 19471451, 'sharesShortPreviousMonthDate': 1715731200, 'dateShortInterest': 1718323200, 'sharesPercentSharesOut': 0.0201, 'heldPercentInsiders': 0.02039, 'heldPercentInstitutions': 0.76097, 'shortRatio': 2.03, 'shortPercentOfFloat': 0.0201, 'impliedSharesOutstanding': 1161040000, 'bookValue': -7.46, 'lastFiscalYearEnd': 1696118400, 'nextFiscalYearEnd': 1727740800, 'mostRecentQuarter': 1711843200, 'earningsQuarterlyGrowth': -0.15, 'netIncomeToCommon': 4157700096, 'trailingEps': 3.63, 'forwardEps': 4.07, 'pegRatio': 2.55, 'lastSplitFactor': '2:1', 'lastSplitDate': 1428537600, 'enterpriseToRevenue': 2.86, 'enterpriseToEbitda': 14.684, '52WeekChange': -0.28070003, 'SandP52WeekChange': 0.24704397, 'lastDividendValue': 0.57, 'lastDividendDate': 1715817600, 'exchange': 'NMS', 'quoteType': 'EQUITY', 'symbol': 'SBUX', 'underlyingSymbol': 'SBUX', 'shortName': 'Starbucks Corporation', 'longName': 'Starbucks Corporation', 'firstTradeDateEpochUtc': 709565400, 'timeZoneFullName': 'America/New_York', 'timeZoneShortName': 'EDT', 'uuid': '008ad8c5-a728-3e78-9380-bba1f5a13a9e', 'messageBoardId': 'finmb_34745', 'gmtOffSetMilliseconds': -14400000, 'currentPrice': 72.75, 'targetHighPrice': 120.0, 'targetLowPrice': 75.0, 'targetMeanPrice': 89.39, 'targetMedianPrice': 85.0, 'recommendationMean': 2.6, 'recommendationKey': 'hold', 'numberOfAnalystOpinions': 29, 'totalCash': 3126599936, 'totalCashPerShare': 2.76, 'ebitda': 7116299776, 'totalDebt': 25209399296, 'quickRatio': 0.563, 'currentRatio': 0.859, 'totalRevenue': 36530098176, 'revenuePerShare': 32.048, 'returnOnAssets': 0.120570004, 'freeCashflow': 2832212480, 'operatingCashflow': 6537800192, 'earningsGrowth': -0.139, 'revenueGrowth': -0.018, 'grossMargins': 0.27737, 'ebitdaMargins': 0.19481, 'operatingMargins': 0.12039, 'financialCurrency': 'USD', 'trailingPegRatio': 1.2518}

# from pprint import pprint
# pprint(a)

# dw = DataWrangler()
# sector = dw.sic_code()
# print(sector[sector.industry_title == 'Consumer Cyclical'.upper()])

# pprint(sector.office.sort_values().unique())
# pprint(sector.industry_title.sort_values().unique())