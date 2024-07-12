import os
import time
import pandas as pd
import numpy as np
# from PairTrading.backend.data_wrangler import DataWrangler
# from PairTrading.backend.scanner import Scanner
import math
import matplotlib.pyplot as plt
import itertools
import yfinance as yf
import pandas_ta

# s = Scanner()
# tickers = s.all_ticker_info.ticker
# print(tickers[-50:].to_list())
# x = ['HLX', 'RENT', 'WEBL', 'CYD', 'ETR', 'DTD', 'MC', 'BALT', 'BBW', 'DFEN', 'CREX', 'ELME', 'EIPI', 'AISP', 'SCO', 'HDGE', 'PTLC', 'CVV', 'DLN', 'IGTA', 'DXJ', 'ERC', 'BCDA', 'BB', 'DXC', 'TTSH', 'VIASP', 'NTCT', 'RFAIU', 'DBI', 'MZZ', 'CFRpB', 'VIOG', 'MMIN', 'BBUC', 'CALX', 'CHSCO', 'IRMD', 'LC', 'HYGH', 'FI', 'DXJS', 'ARLP', 'AWP', 'UROY', 'EWTX', 'BATT', 'OAKpA', 'CCD', 'AIRL']
# data = yf.download(" ".join(x), period="5d").reset_index()
# print(data.columns)
# print(data.Close)
# print(data[data.Ticker == 'SPY'])

# msft = yf.Ticker("MSFT")

# x = {'address1': 'One Microsoft Way', 'city': 'Redmond', 'state': 'WA', 'zip': '98052-6399', 'country': 'United States', 'phone': '425 882 8080', 'website': 'https://www.microsoft.com', 'industry': 'Software - Infrastructure', 'industryKey': 'software-infrastructure', 'industryDisp': 'Software - Infrastructure', 'sector': 'Technology', 'sectorKey': 'technology', 'sectorDisp': 'Technology', 'longBusinessSummary': 'Microsoft Corporation develops and supports software, services, devices and solutions worldwide. The Productivity and Business Processes segment offers office, exchange, SharePoint, Microsoft Teams, office 365 Security and Compliance, Microsoft viva, and Microsoft 365 copilot; and office consumer services, such as Microsoft 365 consumer subscriptions, Office licensed on-premises, and other office services. This segment also provides LinkedIn; and dynamics business solutions, including Dynamics 365, a set of intelligent, cloud-based applications across ERP, CRM, power apps, and power automate; and on-premises ERP and CRM applications. The Intelligent Cloud segment offers server products and cloud services, such as azure and other cloud services; SQL and windows server, visual studio, system center, and related client access licenses, as well as nuance and GitHub; and enterprise services including enterprise support services, industry solutions, and nuance professional services. The More Personal Computing segment offers Windows, including windows OEM licensing and other non-volume licensing of the Windows operating system; Windows commercial comprising volume licensing of the Windows operating system, windows cloud services, and other Windows commercial offerings; patent licensing; and windows Internet of Things; and devices, such as surface, HoloLens, and PC accessories. Additionally, this segment provides gaming, which includes Xbox hardware and content, and first- and third-party content; Xbox game pass and other subscriptions, cloud gaming, advertising, third-party disc royalties, and other cloud services; and search and news advertising, which includes Bing, Microsoft News and Edge, and third-party affiliates. The company sells its products through OEMs, distributors, and resellers; and directly through digital marketplaces, online, and retail stores. The company was founded in 1975 and is headquartered in Redmond, Washington.', 'fullTimeEmployees': 221000, 'companyOfficers': [{'maxAge': 1, 'name': 'Mr. Satya  Nadella', 'age': 56, 'title': 'Chairman & CEO', 'yearBorn': 1967, 'fiscalYear': 2023, 'totalPay': 9276400, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Bradford L. Smith LCA', 'age': 64, 'title': 'President & Vice Chairman', 'yearBorn': 1959, 'fiscalYear': 2023, 'totalPay': 3591277, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Amy E. Hood', 'age': 51, 'title': 'Executive VP & CFO', 'yearBorn': 1972, 'fiscalYear': 2023, 'totalPay': 3452196, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Judson B. Althoff', 'age': 49, 'title': 'Executive VP & Chief Commercial Officer', 'yearBorn': 1974, 'fiscalYear': 2023, 'totalPay': 3355797, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Christopher David Young', 'age': 51, 'title': 'Executive Vice President of Business Development, Strategy & Ventures', 'yearBorn': 1972, 'fiscalYear': 2023, 'totalPay': 2460507, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Alice L. Jolla', 'age': 56, 'title': 'Corporate VP & Chief Accounting Officer', 'yearBorn': 1967, 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. James Kevin Scott', 'age': 51, 'title': 'Executive VP of AI & CTO', 'yearBorn': 1972, 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Brett  Iversen', 'title': 'Vice President of Investor Relations', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Hossein  Nowbar', 'title': 'Chief Legal Officer', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Frank X. Shaw', 'title': 'Chief Communications Officer', 'fiscalYear': 2023, 'exercisedValue': 0, 'unexercisedValue': 0}], 'auditRisk': 3, 'boardRisk': 4, 'compensationRisk': 2, 'shareHolderRightsRisk': 2, 'overallRisk': 1, 'governanceEpochDate': 1719792000, 'compensationAsOfEpochDate': 1703980800, 'irWebsite': 'http://www.microsoft.com/investor/default.aspx', 'maxAge': 86400, 'priceHint': 2, 'previousClose': 459.54, 'open': 461.205, 'dayLow': 458.9, 'dayHigh': 466.46, 'regularMarketPreviousClose': 459.54, 'regularMarketOpen': 461.205, 'regularMarketDayLow': 458.9, 'regularMarketDayHigh': 466.46, 'dividendRate': 3.0, 'dividendYield': 0.0064999997, 'exDividendDate': 1723680000, 'payoutRatio': 0.24780001, 'fiveYearAvgDividendYield': 0.92, 'beta': 0.894, 'trailingPE': 39.85043, 'forwardPE': 37.968243, 'volume': 17757563, 'regularMarketVolume': 17757563, 'averageVolume': 18935201, 'averageVolume10days': 16416830, 'averageDailyVolume10Day': 16416830, 'bid': 466.04, 'ask': 466.31, 'bidSize': 200, 'askSize': 200, 'marketCap': 3465314304000, 'fiftyTwoWeekLow': 309.45, 'fiftyTwoWeekHigh': 468.35, 'priceToSalesTrailing12Months': 14.64729, 'fiftyDayAverage': 429.647, 'twoHundredDayAverage': 393.51184, 'trailingAnnualDividendRate': 2.93, 'trailingAnnualDividendYield': 0.006375941, 'currency': 'USD', 'enterpriseValue': 3491528704000, 'profitMargins': 0.36426997, 'floatShares': 7422123535, 'sharesOutstanding': 7432309760, 'sharesShort': 62396959, 'sharesShortPriorMonth': 43764126, 'sharesShortPreviousMonthDate': 1715731200, 'dateShortInterest': 1718323200, 'sharesPercentSharesOut': 0.0084, 'heldPercentInsiders': 0.00054000004, 'heldPercentInstitutions': 0.73636, 'shortRatio': 3.41, 'shortPercentOfFloat': 0.0084, 'impliedSharesOutstanding': 7432309760, 'bookValue': 34.058, 'priceToBook': 13.689882, 'lastFiscalYearEnd': 1688083200, 'nextFiscalYearEnd': 1719705600, 'mostRecentQuarter': 1711843200, 'earningsQuarterlyGrowth': 0.199, 'netIncomeToCommon': 86181003264, 'trailingEps': 11.7, 'forwardEps': 12.28, 'pegRatio': 2.81, 'lastSplitFactor': '2:1', 'lastSplitDate': 1045526400, 'enterpriseToRevenue': 14.758, 'enterpriseToEbitda': 27.715, '52WeekChange': 0.36281145, 'SandP52WeekChange': 0.24704397, 'lastDividendValue': 0.75, 'lastDividendDate': 1715731200, 'exchange': 'NMS', 'quoteType': 'EQUITY', 'symbol': 'MSFT', 'underlyingSymbol': 'MSFT', 'shortName': 'Microsoft Corporation', 'longName': 'Microsoft Corporation', 'firstTradeDateEpochUtc': 511108200, 'timeZoneFullName': 'America/New_York', 'timeZoneShortName': 'EDT', 'uuid': 'b004b3ec-de24-385e-b2c1-923f10d3fb62', 'messageBoardId': 'finmb_21835', 'gmtOffSetMilliseconds': -14400000, 'currentPrice': 466.25, 'targetHighPrice': 553.97, 'targetLowPrice': 402.55, 'targetMeanPrice': 453.27, 'targetMedianPrice': 446.3, 'recommendationMean': 1.7, 'recommendationKey': 'buy', 'numberOfAnalystOpinions': 46, 'totalCash': 80013000704, 'totalCashPerShare': 10.766, 'ebitda': 125981999104, 'totalDebt': 106228998144, 'quickRatio': 1.132, 'currentRatio': 1.242, 'totalRevenue': 236583993344, 'debtToEquity': 41.963, 'revenuePerShare': 31.834, 'returnOnAssets': 0.1541, 'returnOnEquity': 0.38487998, 'freeCashflow': 61997998080, 'operatingCashflow': 110122999808, 'earningsGrowth': 0.2, 'revenueGrowth': 0.17, 'grossMargins': 0.69894, 'ebitdaMargins': 0.5325, 'operatingMargins': 0.44588003, 'financialCurrency': 'USD', 'trailingPegRatio': 2.2658}

# from pprint import pprint
# pprint(x)

# print(help(yf.download))

#Get ticker for x industry
#Pre filter price range and 1 day volume
#Get list of ticker that need an update
#Download batch from yahoo finance
#create avg diff
#filter by avg diff

# x = "'" + "', '".join(['CFFI', 'SBSI', 'FBP', 'CVBF', 'RIV']) + "'"
x = "'" + "', '".join(['CFFI']) + "'"
print(x)
#'AAPL', 'MSTR'