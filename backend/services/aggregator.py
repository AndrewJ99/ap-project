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

    print(f"[FILTER] {len(transactions)} transactions -> {len(result)} matched")
    return result


def mtd_summary(transactions, cardBrand=None, status=None, declineReasonCode=None):
    """Calculate month-to-date summary with optional filtering."""
    now = datetime.now()
    print(f"[MTD] Calculating summary for {now.strftime('%B %Y')}")
    month_txns = []

    # Filter to current month first
    for t in transactions:
        dt = datetime.fromisoformat(t["transactionDate"])
        if dt.year == now.year and dt.month == now.month:
            month_txns.append(t)

    # Apply additional filters if provided
    if cardBrand or status or declineReasonCode:
        month_txns = filter_transactions(month_txns, cardBrand, status, declineReasonCode)

    summary = {
        "totalTransactions": len(month_txns),
        "totalApproved": 0,
        "totalDeclined": 0,
        "totalAmount": 0.0,
        "approvedAmount": 0.0,
        "declinedAmount": 0.0,
        "byCardBrand": {},
        "byDeclineReason": {}
    }

    for t in month_txns:
        brand = t["cardBrand"]
        amount = t.get("amount", 0)

        summary["totalAmount"] += amount
        summary["byCardBrand"][brand] = summary["byCardBrand"].get(brand, 0) + 1

        if t["status"] == "Approved":
            summary["totalApproved"] += 1
            summary["approvedAmount"] += amount
        else:
            summary["totalDeclined"] += 1
            summary["declinedAmount"] += amount
            code = t["declineReasonCode"]
            summary["byDeclineReason"][code] = summary["byDeclineReason"].get(code, 0) + 1

    # Round amounts to 2 decimal places
    summary["totalAmount"] = round(summary["totalAmount"], 2)
    summary["approvedAmount"] = round(summary["approvedAmount"], 2)
    summary["declinedAmount"] = round(summary["declinedAmount"], 2)

    print(f"[MTD] Result: {summary['totalTransactions']} txns, {summary['totalApproved']} approved, {summary['totalDeclined']} declined")
    return summary


def month_by_month_summary(transactions, cardBrand=None, status=None, declineReasonCode=None):
    """Calculate month-by-month summary with optional filtering."""
    print("[MONTHLY] Calculating month-by-month summary")
    # Apply filters if provided
    if cardBrand or status or declineReasonCode:
        transactions = filter_transactions(transactions, cardBrand, status, declineReasonCode)

    grouped = defaultdict(list)

    for t in transactions:
        dt = datetime.fromisoformat(t["transactionDate"])
        key = dt.strftime("%Y-%m")  # Use sortable format
        grouped[key].append(t)

    summary = {}

    for month_key in sorted(grouped.keys()):
        txns = grouped[month_key]
        # Convert to display format
        dt = datetime.strptime(month_key, "%Y-%m")
        display_key = dt.strftime("%b %Y")

        summary[display_key] = {
            "sortKey": month_key,
            "totalTransactions": len(txns),
            "totalApproved": 0,
            "totalDeclined": 0,
            "totalAmount": 0.0,
            "approvedAmount": 0.0,
            "declinedAmount": 0.0,
            "byCardBrand": {},
            "byDeclineReason": {}
        }

        for t in txns:
            brand = t["cardBrand"]
            amount = t.get("amount", 0)

            summary[display_key]["totalAmount"] += amount
            summary[display_key]["byCardBrand"][brand] = summary[display_key]["byCardBrand"].get(brand, 0) + 1

            if t["status"] == "Approved":
                summary[display_key]["totalApproved"] += 1
                summary[display_key]["approvedAmount"] += amount
            else:
                summary[display_key]["totalDeclined"] += 1
                summary[display_key]["declinedAmount"] += amount
                code = t["declineReasonCode"]
                summary[display_key]["byDeclineReason"][code] = summary[display_key]["byDeclineReason"].get(code, 0) + 1

        # Round amounts
        summary[display_key]["totalAmount"] = round(summary[display_key]["totalAmount"], 2)
        summary[display_key]["approvedAmount"] = round(summary[display_key]["approvedAmount"], 2)
        summary[display_key]["declinedAmount"] = round(summary[display_key]["declinedAmount"], 2)

    print(f"[MONTHLY] Result: {len(summary)} months of data")
    return summary
