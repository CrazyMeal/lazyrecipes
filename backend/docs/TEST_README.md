# LazyRecipes Backend Tests

Comprehensive unit tests for the Flask API endpoints and helper functions.

## Test Coverage

### ✅ Tested Components

1. **Health Check Endpoint** (`GET /api/health`)
   - Success response structure
   - Timestamp validation

2. **Promotions Endpoint** (`GET /api/promotions`)
   - Success with multiple promotions
   - Empty promotions list
   - Data structure validation
   - Error handling

3. **Scrape Endpoint** (`POST /api/scrape`)
   - Success response
   - Function invocation
   - Error handling

4. **Helper Functions**
   - `load_all_promotions()` with various scenarios:
     - No directory exists
     - Single file loading
     - Multiple files loading
     - Invalid JSON handling
     - File read error handling

5. **Integration Tests**
   - Endpoint accessibility
   - HTTP method validation
   - 404/405 error responses

6. **Data Validation**
   - Numeric price validation
   - Required field validation
   - Data type checking

### ❌ Excluded from Tests (as requested)

- Recipe generation endpoint (`POST /api/recipes/generate`)
- Shopping list endpoint (`POST /api/shopping-list`)
- Background scheduler functionality
- Weekly scraping task

## Running Tests

### Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest test_app.py
```

### Run with Verbose Output
```bash
pytest test_app.py -v
```

### Run with Coverage Report
```bash
pytest test_app.py --cov=app --cov-report=term-missing
```

### Run Specific Test Class
```bash
pytest test_app.py::TestHealthEndpoint -v
```

### Run Specific Test
```bash
pytest test_app.py::TestHealthEndpoint::test_health_check_success -v
```

## Test Results

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.3, pluggy-1.6.0
collecting ... 21 items

test_app.py::TestHealthEndpoint::test_health_check_success ................. PASSED
test_app.py::TestHealthEndpoint::test_health_check_has_timestamp ........... PASSED
test_app.py::TestPromotionsEndpoint::test_get_promotions_success ........... PASSED
test_app.py::TestPromotionsEndpoint::test_get_promotions_empty ............. PASSED
test_app.py::TestPromotionsEndpoint::test_get_promotions_structure ......... PASSED
test_app.py::TestPromotionsEndpoint::test_get_promotions_error_handling .... PASSED
test_app.py::TestLoadAllPromotions::test_load_promotions_no_directory ...... PASSED
test_app.py::TestLoadAllPromotions::test_load_promotions_single_file ....... PASSED
test_app.py::TestLoadAllPromotions::test_load_promotions_multiple_files .... PASSED
test_app.py::TestLoadAllPromotions::test_load_promotions_invalid_json ...... PASSED
test_app.py::TestLoadAllPromotions::test_load_promotions_file_read_error ... PASSED
test_app.py::TestScrapeEndpoint::test_scrape_endpoint_success .............. PASSED
test_app.py::TestScrapeEndpoint::test_scrape_endpoint_calls_scraper ........ PASSED
test_app.py::TestScrapeEndpoint::test_scrape_endpoint_error_handling ....... PASSED
test_app.py::TestAPIIntegration::test_health_endpoint_available ............ PASSED
test_app.py::TestAPIIntegration::test_promotions_endpoint_available ........ PASSED
test_app.py::TestAPIIntegration::test_scrape_endpoint_available ............ PASSED
test_app.py::TestAPIIntegration::test_invalid_endpoint_returns_404 ......... PASSED
test_app.py::TestAPIIntegration::test_wrong_method_returns_405 ............. PASSED
test_app.py::TestDataValidation::test_promotion_price_is_numeric ........... PASSED
test_app.py::TestDataValidation::test_promotion_fields_not_empty ........... PASSED

============================== 21 passed in 0.44s ==============================
```

## Test Structure

Tests are organized into logical classes:

- **`TestHealthEndpoint`**: Health check endpoint tests
- **`TestPromotionsEndpoint`**: Promotions listing tests
- **`TestLoadAllPromotions`**: Helper function tests
- **`TestScrapeEndpoint`**: Manual scrape trigger tests
- **`TestAPIIntegration`**: Cross-endpoint integration tests
- **`TestDataValidation`**: Data structure validation tests

## Fixtures

- **`client`**: Flask test client for making requests
- **`sample_promotions`**: Sample promotion data for testing
- **`sample_store_data`**: Sample store file structure

## Mocking Strategy

Tests use `unittest.mock` and `pytest-mock` to:
- Mock file system operations (`open`, `glob.glob`, `os.path.exists`)
- Mock API helper functions (`load_all_promotions`)
- Mock long-running operations (`run_weekly_scrape_and_analysis`)

This ensures tests run fast and don't depend on external resources.

## Coverage Report

Current test coverage: **33%**

Coverage is focused on:
- API endpoint handlers (health, promotions, scrape)
- Helper functions (load_all_promotions)
- Request/response validation

Uncovered code (excluded from tests as requested):
- Recipe generation logic (~40 lines)
- Shopping list creation (~50 lines)
- Background scheduler setup (~15 lines)
- Weekly task runner (~30 lines)

## Adding New Tests

To add new tests:

1. Create a new test class or add to existing one
2. Use fixtures for common test data
3. Mock external dependencies
4. Follow naming convention: `test_<what_is_tested>`
5. Run tests to ensure they pass

Example:
```python
class TestNewFeature:
    """Tests for new feature."""

    def test_feature_success(self, client):
        """Test that new feature works correctly."""
        response = client.get('/api/new-feature')
        assert response.status_code == 200
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (~0.5 seconds)
- No external dependencies required
- Comprehensive mocking
- Clear pass/fail indicators

## Troubleshooting

**Issue**: Tests fail with "ModuleNotFoundError: No module named 'app'"

**Solution**: Make sure you're in the backend directory and virtual environment is activated:
```bash
cd backend
source venv/bin/activate
pytest test_app.py
```

**Issue**: Import errors related to Flask or pytest

**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt
```
