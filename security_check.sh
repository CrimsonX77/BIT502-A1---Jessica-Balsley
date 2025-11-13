#!/bin/bash
# Aurora Archive - Pre-Upload Security Check
# Run this before pushing to GitHub!

echo "🔒 Aurora Archive - Security Audit"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Check 1: .env files
echo "📋 Checking for secret files..."
if [ -f ".env" ]; then
    if git check-ignore -q .env; then
        echo -e "${GREEN}✓${NC} .env is properly ignored"
    else
        echo -e "${RED}✗ WARNING: .env is NOT in .gitignore!${NC}"
        ERRORS=$((ERRORS + 1))
    fi
fi

if [ -f "sd_config.env" ]; then
    if git check-ignore -q sd_config.env; then
        echo -e "${GREEN}✓${NC} sd_config.env is properly ignored"
    else
        echo -e "${RED}✗ WARNING: sd_config.env is NOT in .gitignore!${NC}"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Check 2: API keys in staged files
echo ""
echo "🔑 Scanning staged files for API keys..."
if git diff --cached --name-only | xargs grep -i "xai-" 2>/dev/null; then
    echo -e "${RED}✗ FOUND Grok API key in staged files!${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No Grok API keys found in staged files"
fi

if git diff --cached --name-only | xargs grep -i "sk_test\|sk_live" 2>/dev/null; then
    echo -e "${RED}✗ FOUND Stripe key in staged files!${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✓${NC} No Stripe keys found in staged files"
fi

# Check 3: Large files
echo ""
echo "📦 Checking for large files..."
LARGE_FILES=$(find . -type f -size +10M ! -path "*/venv/*" ! -path "*/SD15/*" ! -path "*/.git/*" 2>/dev/null)
if [ -n "$LARGE_FILES" ]; then
    echo -e "${YELLOW}⚠${NC}  Found large files (>10MB):"
    echo "$LARGE_FILES"
    echo "   Consider adding these to .gitignore"
else
    echo -e "${GREEN}✓${NC} No large files found"
fi

# Check 4: Model files
echo ""
echo "🎨 Checking for model files..."
if find . -name "*.safetensors" ! -path "*/venv/*" | grep -q .; then
    if git check-ignore -q "*.safetensors"; then
        echo -e "${GREEN}✓${NC} .safetensors files are properly ignored"
    else
        echo -e "${YELLOW}⚠${NC}  .safetensors files found but may not be ignored!"
    fi
else
    echo -e "${GREEN}✓${NC} No .safetensors files in repo"
fi

# Check 5: Template files exist
echo ""
echo "📄 Checking for template files..."
if [ -f ".env.example" ]; then
    echo -e "${GREEN}✓${NC} .env.example exists"
else
    echo -e "${RED}✗${NC} .env.example is MISSING!"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "sd_config.env.example" ]; then
    echo -e "${GREEN}✓${NC} sd_config.env.example exists"
else
    echo -e "${RED}✗${NC} sd_config.env.example is MISSING!"
    ERRORS=$((ERRORS + 1))
fi

# Check 6: Personal paths
echo ""
echo "🏠 Checking for personal paths..."
if git diff --cached --name-only | xargs grep -i "/home/crimson" 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC}  Found personal paths in staged files"
    echo "   Consider making paths relative"
else
    echo -e "${GREEN}✓${NC} No personal paths found"
fi

# Summary
echo ""
echo "=================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All security checks passed!${NC}"
    echo "You're ready to push to GitHub! 🚀"
    exit 0
else
    echo -e "${RED}❌ Found $ERRORS critical issue(s)${NC}"
    echo "Please fix these before pushing!"
    exit 1
fi
