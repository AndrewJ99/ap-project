import json
import random
from datetime import datetime, timedelta

card_brands = ["Visa", "Mastercard", "Amex", "Discover"]
statuses = ["Approved", "Declined"]
decline_codes = ["01", "02", "03"]

transactions = []

#function to generate random transactionId
def generate_transaction_id():
    p1 = random.randint(1000,9999)
    p2 = random.randint(1000,9999)
    p3 = random.randint(1000000, 9999999)
    return f"T{p1}-{p2}-{p3}"

for i in range(100):
    status = random.choice(statuses)
    transaction = {
        "transactionId": generate_transaction_id(),
        "merchantId": f"M{random.randint(1,5)}",
        "amount": round(random.uniform(10, 500), 2),
        "cardBrand": random.choice(card_brands),
        "status": status,
        "declineReasonCode": random.choice(decline_codes) if status == "Declined" else None,
        "transactionDate": (datetime.now().replace(microsecond=0) - timedelta(days=random.randint(0, 365))).isoformat()
    }
    transactions.append(transaction)


# generates json transaction file and drops in ../data/
with open("../data/transactions.json", "w") as f:
    json.dump(transactions, f, indent=2)

print("Mock transactions generated!")
