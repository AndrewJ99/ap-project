import json
import random
from datetime import datetime, timedelta

card_brands = ["Visa", "Mastercard", "Amex", "Discover"]
statuses = ["Approved", "Declined"]
decline_codes = ["01", "02", "03"]

transactions = []

for i in range(50):
    status = random.choice(statuses)
    transaction = {
        "transactionId": f"T{i+1000}",
        "merchantId": f"M{random.randint(1,5)}",
        "amount": round(random.uniform(10, 500), 2),
        "cardBrand": random.choice(card_brands),
        "status": status,
        "declineReasonCode": random.choice(decline_codes) if status == "Declined" else None,
        "transactionDate": (datetime.now() - timedelta(days=random.randint(0, 60))).isoformat()
    }
    transactions.append(transaction)

with open("../data/transactions.json", "w") as f:
    json.dump(transactions, f, indent=2)

print("Mock transactions generated!")
