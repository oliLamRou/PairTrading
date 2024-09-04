from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from PairTrading.backend.scanner import Scanner
from PairTrading.backend.data_wrangler import DataWrangler

app = Flask(__name__)
CORS(app)

api = Api(app)
api.add_resource(Scanner, '/pairs', '/potential_pair')
api.add_resource(DataWrangler, '/pair_info', '/market_data', '/company_info')

app.run(debug=True,  port='5002')