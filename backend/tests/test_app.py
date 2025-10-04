"""
Unit tests for LazyRecipes Flask API.
Excludes recipe generation and shopping list tests.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock, mock_open
from app import app, load_all_promotions


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_promotions():
    """Sample promotion data for testing."""
    return [
        {
            "item": "Broccoli",
            "price": 0.55,
            "unit": "each",
            "discount": "Save 73%",
            "store": "maxi"
        },
        {
            "item": "Chicken Wings",
            "price": 6.95,
            "unit": "kg",
            "discount": "Save 50%",
            "store": "iga"
        },
        {
            "item": "Pasta",
            "price": 0.99,
            "unit": "pkg",
            "discount": "Save 60%",
            "store": "metro"
        }
    ]


@pytest.fixture
def sample_store_data(sample_promotions):
    """Sample store promotion file data."""
    return {
        "store": "maxi",
        "store_key": "maxi",
        "page_count": 2,
        "total_pages": 26,
        "promotion_count": 1,
        "promotions": [sample_promotions[0]]
    }


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_success(self, client):
        """Test that health check returns 200 and correct structure."""
        response = client.get('/api/health')

        assert response.status_code == 200

        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_health_check_has_timestamp(self, client):
        """Test that health check includes a valid timestamp."""
        response = client.get('/api/health')
        data = json.loads(response.data)

        # Basic validation that timestamp is in ISO format
        assert "timestamp" in data
        assert "T" in data["timestamp"]  # ISO format includes T separator


class TestPromotionsEndpoint:
    """Tests for the promotions endpoint."""

    @patch('app.load_all_promotions')
    def test_get_promotions_success(self, mock_load, client, sample_promotions):
        """Test that promotions endpoint returns correct data."""
        mock_load.return_value = sample_promotions

        response = client.get('/api/promotions')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert "promotions" in data
        assert "count" in data
        assert "last_updated" in data
        assert data["count"] == len(sample_promotions)
        assert len(data["promotions"]) == 3

    @patch('app.load_all_promotions')
    def test_get_promotions_empty(self, mock_load, client):
        """Test promotions endpoint with no promotions available."""
        mock_load.return_value = []

        response = client.get('/api/promotions')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data["count"] == 0
        assert data["promotions"] == []

    @patch('app.load_all_promotions')
    def test_get_promotions_structure(self, mock_load, client, sample_promotions):
        """Test that each promotion has required fields."""
        mock_load.return_value = sample_promotions

        response = client.get('/api/promotions')
        data = json.loads(response.data)

        for promo in data["promotions"]:
            assert "item" in promo
            assert "price" in promo
            assert "unit" in promo
            assert "discount" in promo
            assert "store" in promo

    @patch('app.load_all_promotions')
    def test_get_promotions_error_handling(self, mock_load, client):
        """Test promotions endpoint handles errors gracefully."""
        mock_load.side_effect = Exception("Database error")

        response = client.get('/api/promotions')

        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data


class TestLoadAllPromotions:
    """Tests for the load_all_promotions helper function."""

    @patch('os.path.exists')
    @patch('glob.glob')
    def test_load_promotions_no_directory(self, mock_glob, mock_exists):
        """Test loading promotions when directory doesn't exist."""
        mock_exists.return_value = False

        result = load_all_promotions()

        assert result == []
        mock_glob.assert_not_called()

    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_promotions_single_file(self, mock_file, mock_glob, mock_exists, sample_store_data):
        """Test loading promotions from a single file."""
        mock_exists.return_value = True
        mock_glob.return_value = ['promotion_results/maxi_promotions.json']
        mock_file.return_value.read.return_value = json.dumps(sample_store_data)

        result = load_all_promotions()

        assert len(result) == 1
        assert result[0]["item"] == "Broccoli"
        assert result[0]["store"] == "maxi"

    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_promotions_multiple_files(self, mock_file, mock_glob, mock_exists, sample_promotions):
        """Test loading promotions from multiple store files."""
        mock_exists.return_value = True
        mock_glob.return_value = [
            'promotion_results/maxi_promotions.json',
            'promotion_results/iga_promotions.json'
        ]

        # Setup different data for each file
        store1_data = {
            "store": "maxi",
            "promotions": [sample_promotions[0]]
        }
        store2_data = {
            "store": "iga",
            "promotions": [sample_promotions[1]]
        }

        def side_effect(*args, **kwargs):
            if 'maxi' in args[0]:
                m = mock_open(read_data=json.dumps(store1_data))
                return m(*args, **kwargs)
            else:
                m = mock_open(read_data=json.dumps(store2_data))
                return m(*args, **kwargs)

        mock_file.side_effect = side_effect

        result = load_all_promotions()

        assert len(result) == 2
        assert any(p["item"] == "Broccoli" for p in result)
        assert any(p["item"] == "Chicken Wings" for p in result)

    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_promotions_invalid_json(self, mock_file, mock_glob, mock_exists):
        """Test loading promotions handles invalid JSON gracefully."""
        mock_exists.return_value = True
        mock_glob.return_value = ['promotion_results/invalid_promotions.json']
        mock_file.return_value.read.return_value = "invalid json"

        # Should not raise exception, just skip the file
        result = load_all_promotions()

        assert result == []

    @patch('os.path.exists')
    @patch('glob.glob')
    @patch('builtins.open')
    def test_load_promotions_file_read_error(self, mock_file, mock_glob, mock_exists):
        """Test loading promotions handles file read errors gracefully."""
        mock_exists.return_value = True
        mock_glob.return_value = ['promotion_results/error_promotions.json']
        mock_file.side_effect = IOError("Cannot read file")

        # Should not raise exception
        result = load_all_promotions()

        assert result == []


class TestScrapeEndpoint:
    """Tests for the scrape endpoint."""

    @patch('app.run_weekly_scrape_and_analysis')
    @patch('app.load_all_promotions')
    def test_scrape_endpoint_success(self, mock_load, mock_scrape, client, sample_promotions):
        """Test manual scrape trigger returns success."""
        mock_scrape.return_value = None  # Scraping completed
        mock_load.return_value = sample_promotions

        response = client.post('/api/scrape')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert data["status"] == "success"
        assert "message" in data
        assert "promotions" in data
        assert data["count"] == 3

    @patch('app.run_weekly_scrape_and_analysis')
    @patch('app.load_all_promotions')
    def test_scrape_endpoint_calls_scraper(self, mock_load, mock_scrape, client):
        """Test scrape endpoint actually calls the scraping function."""
        mock_load.return_value = []

        response = client.post('/api/scrape')

        mock_scrape.assert_called_once()
        assert response.status_code == 200

    @patch('app.run_weekly_scrape_and_analysis')
    def test_scrape_endpoint_error_handling(self, mock_scrape, client):
        """Test scrape endpoint handles errors gracefully."""
        mock_scrape.side_effect = Exception("Scraping failed")

        response = client.post('/api/scrape')

        assert response.status_code == 500
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert "message" in data


class TestAPIIntegration:
    """Integration tests for API endpoints."""

    def test_health_endpoint_available(self, client):
        """Test that health endpoint is accessible."""
        response = client.get('/api/health')
        assert response.status_code == 200

    @patch('app.load_all_promotions')
    def test_promotions_endpoint_available(self, mock_load, client):
        """Test that promotions endpoint is accessible."""
        mock_load.return_value = []
        response = client.get('/api/promotions')
        assert response.status_code == 200

    @patch('app.run_weekly_scrape_and_analysis')
    @patch('app.load_all_promotions')
    def test_scrape_endpoint_available(self, mock_load, mock_scrape, client):
        """Test that scrape endpoint is accessible."""
        mock_load.return_value = []
        response = client.post('/api/scrape')
        assert response.status_code == 200

    def test_invalid_endpoint_returns_404(self, client):
        """Test that invalid endpoints return 404."""
        response = client.get('/api/invalid')
        assert response.status_code == 404

    def test_wrong_method_returns_405(self, client):
        """Test that wrong HTTP methods return 405."""
        response = client.post('/api/health')
        assert response.status_code == 405


class TestDataValidation:
    """Tests for data validation and structure."""

    @patch('app.load_all_promotions')
    def test_promotion_price_is_numeric(self, mock_load, client, sample_promotions):
        """Test that promotion prices are numeric."""
        mock_load.return_value = sample_promotions

        response = client.get('/api/promotions')
        data = json.loads(response.data)

        for promo in data["promotions"]:
            assert isinstance(promo["price"], (int, float))
            assert promo["price"] >= 0

    @patch('app.load_all_promotions')
    def test_promotion_fields_not_empty(self, mock_load, client, sample_promotions):
        """Test that required promotion fields are not empty."""
        mock_load.return_value = sample_promotions

        response = client.get('/api/promotions')
        data = json.loads(response.data)

        for promo in data["promotions"]:
            assert promo["item"]  # Not empty
            assert promo["store"]  # Not empty
            assert promo["unit"]  # Not empty


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
