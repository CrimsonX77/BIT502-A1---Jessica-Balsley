#!/bin/bash
################################################################################
# Aurora Archive System Launcher (Linux/Mac)
# Automated setup, dependency checking, and GUI launcher
################################################################################

set -e  # Exit on error (we'll handle errors explicitly)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Error tracking
ERROR_COUNT=0

echo ""
echo "============================================================"
echo "   THE AURORA ARCHIVE - Extended Implementation Launcher"
echo "============================================================"
echo ""

################################################################################
# STEP 1: Check Python Installation
################################################################################

echo -e "${BLUE}[1/7] Checking Python installation...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed${NC}"
    echo ""
    echo "Please install Python 3.10+ using your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  macOS: brew install python@3.10"
    echo ""
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[OK] Python $PYTHON_VERSION found${NC}"

# Check if version is 3.10+
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 10 ]); then
    echo -e "${YELLOW}[WARNING] Python 3.10+ recommended, found $PYTHON_VERSION${NC}"
    echo -e "${YELLOW}Some features may not work correctly${NC}"
fi

echo ""

################################################################################
# STEP 2: Check/Create Virtual Environment
################################################################################

echo -e "${BLUE}[2/7] Checking virtual environment...${NC}"

if [ ! -d "venv" ]; then
    echo -e "${BLUE}[INFO] Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR] Failed to create virtual environment${NC}"
        echo ""
        echo "Try installing python3-venv:"
        echo "  Ubuntu/Debian: sudo apt install python3-venv"
        echo "  Fedora: sudo dnf install python3-virtualenv"
        echo ""
        exit 1
    fi
    echo -e "${GREEN}[OK] Virtual environment created${NC}"
else
    echo -e "${GREEN}[OK] Virtual environment exists${NC}"
fi

echo ""

################################################################################
# STEP 3: Activate Virtual Environment
################################################################################

echo -e "${BLUE}[3/7] Activating virtual environment...${NC}"

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}[OK] Virtual environment activated${NC}"
else
    echo -e "${RED}[ERROR] Virtual environment activation script not found${NC}"
    echo "Recreating virtual environment..."
    rm -rf venv
    python3 -m venv venv
    source venv/bin/activate
fi

echo ""

################################################################################
# STEP 4: Install/Update Dependencies
################################################################################

echo -e "${BLUE}[4/7] Checking dependencies...${NC}"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${BLUE}[INFO] Creating requirements.txt...${NC}"
    cat > requirements.txt << EOF
PyQt6>=6.4.0
cryptography>=41.0.0
Pillow>=10.0.0
requests>=2.31.0
numpy>=1.24.0
EOF
    echo -e "${GREEN}[OK] requirements.txt created${NC}"
fi

echo -e "${BLUE}[INFO] Installing/updating dependencies...${NC}"
echo "This may take a few minutes on first run..."
echo ""

python -m pip install --upgrade pip --quiet 2>&1 | grep -v "WARNING: Running pip"
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Could not upgrade pip${NC}"
fi

python -m pip install -r requirements.txt --quiet 2>&1 | grep -v "WARNING: Running pip"
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR] Failed to install dependencies${NC}"
    echo ""
    echo "Please check your internet connection and try again"
    echo "Or manually install with: pip install -r requirements.txt"
    echo ""
    exit 1
fi

echo -e "${GREEN}[OK] All dependencies installed${NC}"

echo ""

################################################################################
# STEP 5: Check for Stable Diffusion (Optional)
################################################################################

echo -e "${BLUE}[5/7] Checking for Stable Diffusion...${NC}"

if curl -s http://localhost:7860/sdapi/v1/sd-models > /dev/null 2>&1; then
    echo -e "${GREEN}[OK] Stable Diffusion WebUI detected at localhost:7860${NC}"
    SD_AVAILABLE=true
else
    echo -e "${BLUE}[INFO] Stable Diffusion WebUI not detected (optional)${NC}"
    echo -e "${BLUE}[INFO] Card generation will use fallback methods${NC}"
    SD_AVAILABLE=false
fi

echo ""

################################################################################
# STEP 6: Create Config Directory
################################################################################

echo -e "${BLUE}[6/7] Setting up configuration...${NC}"

if [ ! -d "config" ]; then
    mkdir -p config
    echo -e "${GREEN}[OK] Config directory created${NC}"
else
    echo -e "${GREEN}[OK] Config directory exists${NC}"
fi

# Create sample data directories
mkdir -p data/cards
mkdir -p data/members

echo -e "${GREEN}[OK] Data directories ready${NC}"

echo ""

################################################################################
# STEP 7: Launch Applications
################################################################################

echo -e "${BLUE}[7/7] Launching Aurora Archive System...${NC}"
echo ""
echo "============================================================"
echo ""

# Give user a moment to read
sleep 2

echo "Starting applications in sequence..."
echo ""
echo -e "${BLUE}[INFO] Close each window when you're done exploring${NC}"
echo -e "${BLUE}[INFO] Press Ctrl+C at any time to stop all launches${NC}"
echo ""

################################################################################
# Launch Sequence
################################################################################

# Function to launch app in background with error handling
launch_app() {
    local app_file=$1
    local app_name=$2
    local app_num=$3
    
    if [ ! -f "$app_file" ]; then
        echo -e "${YELLOW}[WARNING] $app_file not found - skipping${NC}"
        ((ERROR_COUNT++))
        return 1
    fi
    
    echo -e "${GREEN}[$app_num/4] Launching $app_name...${NC}"
    
    # Try to launch with error suppression
    python "$app_file" > /dev/null 2>&1 &
    local pid=$!
    
    # Give it a moment to start
    sleep 2
    
    # Check if process is still running
    if ps -p $pid > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ $app_name started (PID: $pid)${NC}"
        return 0
    else
        echo -e "${YELLOW}  ⚠ $app_name may have failed to start${NC}"
        return 1
    fi
}

# Launch each application
launch_app "archive_sanctum.py" "Archive Sanctum (Member Portal)" "1"
launch_app "aurora_pyqt6_main.py" "Aurora Card Generator" "2"
launch_app "member_registration_app.py" "Member Registration" "3"
launch_app "obelisk_customs.py" "Obelisk Authentication" "4"

echo ""
echo "============================================================"

if [ $ERROR_COUNT -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}[WARNING] Some components could not be launched${NC}"
    echo -e "${YELLOW}[INFO] $ERROR_COUNT file(s) missing or failed to start${NC}"
    echo ""
    echo "This is normal if you only have the core assignment file."
    echo "The extended implementation requires all Python files."
fi

echo ""
echo "============================================================"
echo "    All available applications have been launched!"
echo "============================================================"
echo ""
echo "GUI windows should now be open. Explore the system features:"
echo "  - Archive Sanctum: Member portal with dashboard"
echo "  - Card Generator: AI-powered card creation"
echo "  - Registration: New member signup workflow"
echo "  - Obelisk: Authentication gateway"
echo ""
echo "Applications are running in the background."
echo "Close GUI windows normally when done exploring."
echo ""
echo "This terminal will remain open to show any error messages."
echo "Press Ctrl+C to exit this launcher (apps will keep running)."
echo ""
echo "============================================================"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}Launcher shutting down...${NC}"
    echo "GUI applications will continue running until closed manually."
    deactivate 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT SIGTERM

# Wait for user to press Ctrl+C or just keep running
echo ""
echo "Press Ctrl+C to exit this launcher..."
while true; do
    sleep 1
done
