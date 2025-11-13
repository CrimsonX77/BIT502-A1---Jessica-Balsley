#!/bin/bash
# Aurora Archive - Quick Start Script

echo "🌅 Aurora Archive - Card Generation System"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if dependencies are installed
echo "📦 Checking dependencies..."
python -c "import aiohttp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing missing dependencies..."
    pip install -q aiohttp python-dotenv
fi

# Check if Stable Diffusion is running
echo "🔍 Checking Stable Diffusion status..."
curl -s http://localhost:7860/sdapi/v1/sd-models > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Stable Diffusion is running"
else
    echo "⚠️  Stable Diffusion is not running"
    echo "   Start it with: cd stable-diffusion-webui && ./webui.sh --api"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Launch the app
echo ""
echo "🚀 Launching Aurora Archive..."
echo ""
python aurora_pyqt6_main.py

echo ""
echo "👋 Aurora Archive closed"
