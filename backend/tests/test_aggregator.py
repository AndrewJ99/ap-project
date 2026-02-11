"""Unit tests for filter_transactions() in services/aggregator.py"""
import pytest
from services.aggregator import filter_transactions


# Sample test data
SAMPLE_TRANSACTIONS = [
    {
        "id": "1",
        "cardBrand": "Visa",
        "status": "Approved",
        "declineReasonCode": None,
        "amount": 100.00,
        "transactionDate": "2026-02-01T10:00:00"
    },
    {
        "id": "2",
        "cardBrand": "Mastercard",
        "status": "Approved",
        "declineReasonCode": None,
        "amount": 200.00,
        "transactionDate": "2026-02-02T11:00:00"
    },
    {
        "id": "3",
        "cardBrand": "Visa",
        "status": "Declined",
        "declineReasonCode": "INSUFFICIENT_FUNDS",
        "amount": 50.00,
        "transactionDate": "2026-02-03T12:00:00"
    },
    {
        "id": "4",
        "cardBrand": "Amex",
        "status": "Declined",
        "declineReasonCode": "CARD_EXPIRED",
        "amount": 75.00,
        "transactionDate": "2026-02-04T13:00:00"
    },
    {
        "id": "5",
        "cardBrand": "Visa",
        "status": "Declined",
        "declineReasonCode": "CARD_EXPIRED",
        "amount": 25.00,
        "transactionDate": "2026-02-05T14:00:00"
    },
]


class TestFilterTransactions:
    """Tests for filter_transactions function."""

    def test_no_filters_returns_all(self):
        """No filters should return all transactions."""
        result = filter_transactions(SAMPLE_TRANSACTIONS)
        assert len(result) == 5
        assert result == SAMPLE_TRANSACTIONS

    def test_filter_by_card_brand_visa(self):
        """Filter by Visa should return only Visa transactions."""
        result = filter_transactions(SAMPLE_TRANSACTIONS, cardBrand="Visa")
        assert len(result) == 3
        assert all(t["cardBrand"] == "Visa" for t in result)

    def test_filter_by_card_brand_mastercard(self):
        """Filter by Mastercard should return only Mastercard transactions."""
        result = filter_transactions(SAMPLE_TRANSACTIONS, cardBrand="Mastercard")
        assert len(result) == 1
        assert result[0]["id"] == "2"

    def test_filter_by_card_brand_amex(self):
        """Filter by Amex should return only Amex transactions."""
        result = filter_transactions(SAMPLE_TRANSACTIONS, cardBrand="Amex")
        assert len(result) == 1
        assert result[0]["id"] == "4"

    def test_filter_by_status_approved(self):
        """Filter by Approved status should return only approved transactions."""
        result = filter_transactions(SAMPLE_TRANSACTIONS, status="Approved")
        assert len(result) == 2
        assert all(t["status"] == "Approved" for t in result)

    def test_filter_by_status_declined(self):
        """Filter by Declined status should return only declined transactions."""
        result = filter_transactions(SAMPLE_TRANSACTIONS, status="Declined")
        assert len(result) == 3
        assert all(t["status"] == "Declined" for t in result)

    def test_filter_by_decline_reason_code(self):
        """Filter by decline reason code (with status=Declined)."""
        result = filter_transactions(
            SAMPLE_TRANSACTIONS,
            status="Declined",
            declineReasonCode="INSUFFICIENT_FUNDS"
        )
        assert len(result) == 1
        assert result[0]["id"] == "3"

    def test_filter_by_decline_reason_card_expired(self):
        """Filter by CARD_EXPIRED decline reason."""
        result = filter_transactions(
            SAMPLE_TRANSACTIONS,
            status="Declined",
            declineReasonCode="CARD_EXPIRED"
        )
        assert len(result) == 2
        assert all(t["declineReasonCode"] == "CARD_EXPIRED" for t in result)

    def test_combined_filters_card_brand_and_status(self):
        """Filter by both card brand and status."""
        result = filter_transactions(
            SAMPLE_TRANSACTIONS,
            cardBrand="Visa",
            status="Declined"
        )
        assert len(result) == 2
        assert all(t["cardBrand"] == "Visa" and t["status"] == "Declined" for t in result)

    def test_combined_filters_card_brand_status_decline_reason(self):
        """Filter by card brand, status, and decline reason."""
        result = filter_transactions(
            SAMPLE_TRANSACTIONS,
            cardBrand="Visa",
            status="Declined",
            declineReasonCode="CARD_EXPIRED"
        )
        assert len(result) == 1
        assert result[0]["id"] == "5"

    def test_empty_result_no_matches(self):
        """Filter that matches nothing should return empty list."""
        result = filter_transactions(SAMPLE_TRANSACTIONS, cardBrand="Discover")
        assert result == []
        assert len(result) == 0

    def test_empty_input_returns_empty(self):
        """Empty transaction list should return empty list."""
        result = filter_transactions([])
        assert result == []

    def test_decline_reason_without_status_filter(self):
        """Decline reason code alone (without status=Declined) should not filter."""
        # When status is not "Declined", declineReasonCode is ignored
        result = filter_transactions(
            SAMPLE_TRANSACTIONS,
            declineReasonCode="INSUFFICIENT_FUNDS"
        )
        # Should return all transactions since status != "Declined"
        assert len(result) == 5
