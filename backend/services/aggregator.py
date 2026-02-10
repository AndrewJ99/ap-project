from datetime import datetime
from collections import defaultdict

def filter_transactions(transactions, cardBrand=None, status=None, declineReasonCode=None):
    result = []

    for t in transactions:
        if cardBrand and t["cardBrand"] != cardBrand:
            continue
        if status and t["status"] != status:
            continue
        if status == "Declined" and declineReasonCode:
            if t["declineReasonCode"] != declineReasonCode:
                continue
        result.append(t)

    return result


def mtd_summary(transactions):
    now = datetime.now()
    month_txns = []

    for t in transactions:
        dt = datetime.fromisoformat(t["transactionDate"])
        if dt.year == now.year and dt.month == now.month:
            month_txns.append(t)

    summary = {
        "totalTransactions": len(month_txns),
        "totalApproved": 0,
        "totalDeclined": 0,
        "byCardBrand": {},
        "byDeclineReason": {}
    }

    for t in month_txns:
        brand = t["cardBrand"]
        summary["byCardBrand"][brand] = summary["byCardBrand"].get(brand, 0) + 1

        if t["status"] == "Approved":
            summary["totalApproved"] += 1
        else:
            summary["totalDeclined"] += 1
            code = t["declineReasonCode"]
            summary["byDeclineReason"][code] = summary["byDeclineReason"].get(code, 0) + 1

    return summary


def month_by_month_summary(transactions):
    grouped = defaultdict(list)

    for t in transactions:
        dt = datetime.fromisoformat(t["transactionDate"])
        key = dt.strftime("%b %Y")
        grouped[key].append(t)

    summary = {}

    for month, txns in grouped.items():
        summary[month] = {
            "totalTransactions": len(txns),
            "totalApproved": 0,
            "totalDeclined": 0,
            "byCardBrand": {},
            "byDeclineReason": {}
        }

        for t in txns:
            brand = t["cardBrand"]
            summary[month]["byCardBrand"][brand] = summary[month]["byCardBrand"].get(brand, 0) + 1

            if t["status"] == "Approved":
                summary[month]["totalApproved"] += 1
            else:
                summary[month]["totalDeclined"] += 1
                code = t["declineReasonCode"]
                summary[month]["byDeclineReason"][code] = summary[month]["byDeclineReason"].get(code, 0) + 1

    return summary
