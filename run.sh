#!/bin/bash
# Touch Grass AI - Quick Start

set -e
echo ""
echo "  Touch Grass AI - Open-source Garden Planner"
echo "  ============================================"
echo ""

if ! command -v python &> /dev/null; then
    echo "  ERROR: Python not found. Install Python 3.10+"
    exit 1
fi

echo "  Checking dependencies..."
python -c "import llama_cpp" &> /dev/null || pip install -r requirements.txt

echo ""
echo "  Running garden planner for ZIP 97202 (Portland, OR)..."
echo ""
python garden_planner.py --zip 97202 --calendar

echo ""
echo "  --- Try these commands ---"
echo "  python garden_planner.py --zip 97202 --plant tomatoes"
echo "  python garden_planner.py --zip 97202 --ask 'companion for garlic'"
echo "  python garden_planner.py --zip 97202 --list --nitrogen"
echo "  python garden_planner.py --zip 97202 --chat"
echo ""