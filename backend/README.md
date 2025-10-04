# LazyRecipes Backend

Flask API backend for LazyRecipes - automated grocery promotion scraping and recipe generation.

## 🏗️ Project Structure

```
backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── .env                        # Environment variables (not in git)
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
│
├── scripts/                   # Scraping and analysis scripts
│   ├── __init__.py
│   ├── discover_flyers.py            # Discover latest flyers from RedFlagDeals
│   ├── extract_flyer_urls.py         # Extract image URLs from flyer pages
│   ├── download_all_flyers.py        # Download flyer images
│   ├── analyze_flyers.py             # Analyze flyers with OpenAI Vision
│   ├── analyze_all_stores_partial.py # Batch analysis with page limits
│   ├── analyze_store_partial.py      # Single store analysis utility
│   ├── analyze_flyers_sample.py      # Sample mode analysis
│   └── scrape_all_flyers.py          # Main orchestration script
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   └── test_app.py                   # API endpoint tests
│
├── docs/                      # Documentation
│   ├── API_DOCS.md                   # API documentation
│   ├── TEST_README.md                # Testing documentation
│   └── api_spec.yaml                 # OpenAPI specification
│
├── data/                      # Data directories (gitignored)
│   ├── flyer_images/                 # Downloaded flyer images by store
│   └── promotion_results/            # Analyzed promotions JSON files
│
└── deprecated/                # Old/test files (gitignored)
    └── ...                           # Legacy scripts and test data
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Create .env file
cp .env.example .env
# Add your OpenAI API key to .env
```

### 2. Run the API

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### 3. Test the API

```bash
# Health check
curl http://localhost:5000/api/health

# Get promotions
curl http://localhost:5000/api/promotions

# Generate recipes
curl -X POST http://localhost:5000/api/recipes/generate \
  -H "Content-Type: application/json" \
  -d '{"num_recipes": 3}'
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/promotions` | Get all current promotions |
| POST | `/api/scrape` | Manually trigger scraping & analysis |
| POST | `/api/recipes/generate` | Generate recipes from promotions |
| POST | `/api/shopping-list` | Create shopping list from recipes |

See [docs/API_DOCS.md](docs/API_DOCS.md) for detailed API documentation.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_app.py -v
```

**Test Coverage:** 21 tests, 33% code coverage

See [docs/TEST_README.md](docs/TEST_README.md) for testing documentation.

## 🔄 Background Scheduler

The API includes a background scheduler that automatically runs the scraping and analysis pipeline:

- **Schedule:** Every Monday at 1:00 AM
- **Task:** Discover → Extract → Download → Analyze flyers
- **Processing:** First 2 pages per store (configurable)
- **Stores:** All grocery stores except excluded ones

## 📦 Dependencies

### Core
- **Flask 3.0.0** - Web framework
- **Flask-CORS 4.0.0** - CORS support
- **APScheduler 3.10.4** - Background task scheduling

### Scraping & Analysis
- **Playwright 1.40.0** - Browser automation
- **OpenAI 2.1.0** - Vision API for flyer analysis
- **Requests 2.31.0** - HTTP client

### Development
- **pytest 7.4.3** - Testing framework
- **pytest-mock 3.12.0** - Mocking utilities
- **pytest-cov 7.0.0** - Coverage reporting

## 🔧 Configuration

### Environment Variables (.env)

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
```

### App Configuration (app.py)

```python
PROMOTIONS_DIR = "data/promotion_results"
FLYER_IMAGES_DIR = "data/flyer_images"
NUM_PAGES_PER_STORE = 2
EXCLUDE_STORES = ['super-c-direct']
```

## 📝 Scripts

### Main Scripts

**`scripts/scrape_all_flyers.py`** - Complete pipeline orchestration
```bash
python scripts/scrape_all_flyers.py
```

**`scripts/analyze_all_stores_partial.py`** - Batch analysis with limits
```bash
python scripts/analyze_all_stores_partial.py
```

### Utility Scripts

- `discover_flyers.py` - Find latest flyers
- `extract_flyer_urls.py` - Extract image URLs
- `download_all_flyers.py` - Download images
- `analyze_store_partial.py` - Analyze single store

## 🗃️ Data Storage

### Flyer Images
`data/flyer_images/{store_name}/`
- Images named: `{store}_page_{num}.jpg`
- Example: `data/flyer_images/maxi/maxi_page_001.jpg`

### Promotions
`data/promotion_results/{store}_promotions.json`
- Structure:
```json
{
  "store": "maxi",
  "store_key": "maxi",
  "page_count": 2,
  "total_pages": 26,
  "promotion_count": 23,
  "promotions": [...]
}
```

## 🎯 Workflow

### Automated Weekly Flow

1. **Discover** - Find latest flyers from RedFlagDeals
2. **Extract** - Parse HTML to find image URLs
3. **Download** - Download flyer images (first 2 pages/store)
4. **Analyze** - Use OpenAI Vision API to extract promotions
5. **Store** - Save results to `data/promotion_results/`

### Manual API Flow

1. User calls `/api/recipes/generate`
2. Load promotions from `data/promotion_results/`
3. Generate recipes using GPT-3.5-turbo
4. Cache recipes in memory
5. User creates shopping list from selected recipes

## 🔍 Monitoring

### Logs
- Flask debug logs show request/response info
- Scraping progress printed to stdout
- OpenAI API calls logged

### Status Files
- `data/promotion_results/_summary.json` - Processing statistics

## 🛠️ Development

### Adding New Endpoints

1. Add route handler in `app.py`
2. Update `docs/API_DOCS.md`
3. Add tests in `tests/test_app.py`
4. Run tests: `pytest`

### Adding New Scripts

1. Create script in `scripts/`
2. Import from scripts package: `from scripts.module import function`
3. Update this README

### Code Style

- Follow PEP 8
- Use docstrings for functions
- Add type hints where helpful
- Keep functions focused and testable

## 🐛 Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'scripts'`

**Solution:** Make sure you're running from the backend directory:
```bash
cd backend
python app.py
```

**Issue:** OpenAI API errors

**Solution:** Check your API key in `.env` file and ensure you have credits

**Issue:** Playwright timeout errors

**Solution:**
```bash
playwright install chromium
# Or increase timeout in scripts
```

**Issue:** Tests failing

**Solution:**
```bash
# Ensure you're in backend directory
cd backend
# Reinstall dependencies
pip install -r requirements.txt
# Run tests
pytest
```

## 📄 License

This project is part of a hackathon demonstration.

## 👥 Contributors

Generated with [Claude Code](https://claude.com/claude-code)
