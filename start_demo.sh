#!/bin/bash
# LazyRecipes Demo Startup Script

echo "======================================================================"
echo "                     LAZYRECIPES DEMO SETUP"
echo "======================================================================"

# Check if results exist
if [ ! -f "backend/results/promotions.json" ]; then
    echo ""
    echo "⚠️  ERROR: backend/results/promotions.json not found!"
    echo "   Run the flyer processor first to generate promotion data:"
    echo "   python backend/scripts/flyer_processor.py --pages 2"
    echo ""
    exit 1
fi

# Import demo data into database
echo ""
echo "Step 1: Importing promotion data into database..."
echo "----------------------------------------------------------------------"
cd backend
python import_demo_data.py
IMPORT_STATUS=$?

if [ $IMPORT_STATUS -ne 0 ]; then
    echo ""
    echo "✗ Data import failed!"
    exit 1
fi

# Start the backend server
echo ""
echo "Step 2: Starting backend server..."
echo "----------------------------------------------------------------------"
echo ""
python app.py
