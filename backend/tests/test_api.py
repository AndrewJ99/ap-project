"""Integration tests for API endpoints using Flask test client."""
import pytest
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for /api/health endpoint."""

    def test_health_returns_ok(self, client):
        """Health endpoint should return status ok."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"status": "ok"}


class TestTransactionsEndpoint:
    """Tests for /api/transactions endpoint."""

    def test_get_transactions_returns_list(self, client):
        """GET /api/transactions should return a list."""
        response = client.get("/api/transactions")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)

    def test_get_transactions_with_card_brand_filter(self, client):
        """Filter by cardBrand should return only matching transactions."""
        response = client.get("/api/transactions?cardBrand=Visa")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        # All returned transactions should be Visa
        for txn in data:
            assert txn["cardBrand"] == "Visa"

    def test_get_transactions_with_status_filter(self, client):
        """Filter by status should return only matching transactions."""
        response = client.get("/api/transactions?status=Approved")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        for txn in data:
            assert txn["status"] == "Approved"

    def test_get_transactions_with_combined_filters(self, client):
        """Combined filters should work together."""
        response = client.get("/api/transactions?cardBrand=Visa&status=Declined")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        for txn in data:
            assert txn["cardBrand"] == "Visa"
            assert txn["status"] == "Declined"


class TestMTDSummaryEndpoint:
    """Tests for /api/summary/mtd endpoint."""

    def test_mtd_summary_returns_expected_structure(self, client):
        """MTD summary should return expected fields."""
        response = client.get("/api/summary/mtd")
        assert response.status_code == 200
        data = response.get_json()

        # Check expected fields exist
        assert "totalTransactions" in data
        assert "totalApproved" in data
        assert "totalDeclined" in data
        assert "totalAmount" in data
        assert "approvedAmount" in data
        assert "declinedAmount" in data
        assert "byCardBrand" in data
        assert "byDeclineReason" in data

        # Check types
        assert isinstance(data["totalTransactions"], int)
        assert isinstance(data["totalApproved"], int)
        assert isinstance(data["totalDeclined"], int)
        assert isinstance(data["totalAmount"], (int, float))
        assert isinstance(data["byCardBrand"], dict)
        assert isinstance(data["byDeclineReason"], dict)

    def test_mtd_summary_with_filter(self, client):
        """MTD summary should accept filter parameters."""
        response = client.get("/api/summary/mtd?cardBrand=Visa")
        assert response.status_code == 200
        data = response.get_json()
        assert "totalTransactions" in data


class TestMonthlySummaryEndpoint:
    """Tests for /api/summary/monthly endpoint."""

    def test_monthly_summary_returns_expected_structure(self, client):
        """Monthly summary should return dict of months."""
        response = client.get("/api/summary/monthly")
        assert response.status_code == 200
        data = response.get_json()

        assert isinstance(data, dict)

        # Each month should have expected structure
        for month_key, month_data in data.items():
            assert "totalTransactions" in month_data
            assert "totalApproved" in month_data
            assert "totalDeclined" in month_data
            assert "totalAmount" in month_data
            assert "approvedAmount" in month_data
            assert "declinedAmount" in month_data
            assert "byCardBrand" in month_data
            assert "byDeclineReason" in month_data

    def test_monthly_summary_with_filter(self, client):
        """Monthly summary should accept filter parameters."""
        response = client.get("/api/summary/monthly?status=Declined")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
