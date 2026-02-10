from flask import Flask
from flask_cors import CORS
import json

from api.transactions import register_transaction_routes
from services.aggregator import (
    filter_transactions,
    mtd_summary,
    month_by_month_summary
)

app = Flask(__name__)
CORS(app)


def load_transactions():
    with open("data/transactions.json") as f:
        return json.load(f)


register_transaction_routes(
    app,
    load_transactions,
    filter_transactions,
    mtd_summary,
    month_by_month_summary
)

if __name__ == "__main__":
    app.run(debug=True)
