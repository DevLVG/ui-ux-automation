#!/bin/bash
# ========================================
# Kick Inn UX Automation - Installation Script
# ========================================
# This script sets up the complete development environment

set -e  # Exit on error

echo "🚀 Kick Inn UX Automation - Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📌 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    REQUIRED_VERSION="3.10"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
        echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
    else
        echo -e "${RED}✗ Python $REQUIRED_VERSION or higher required (found $PYTHON_VERSION)${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

# Check Node.js (for Playwright)
echo ""
echo "📌 Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
else
    echo -e "${YELLOW}⚠ Node.js not found. Installing via nvm recommended.${NC}"
fi

# Check ffmpeg
echo ""
echo "📌 Checking ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n1 | cut -d' ' -f3)
    echo -e "${GREEN}✓ ffmpeg $FFMPEG_VERSION found${NC}"
else
    echo -e "${YELLOW}⚠ ffmpeg not found${NC}"
    echo "Installing ffmpeg..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ffmpeg
        else
            echo -e "${RED}✗ Homebrew not found. Please install ffmpeg manually.${NC}"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update && sudo apt-get install -y ffmpeg
    else
        echo -e "${YELLOW}⚠ Please install ffmpeg manually for your OS${NC}"
    fi
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo ""
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install dev dependencies
echo ""
echo "📦 Installing development dependencies..."
pip install -r requirements-dev.txt

# Install Playwright browsers
echo ""
echo "🎭 Installing Playwright browsers..."
playwright install chromium

# Setup pre-commit hooks
echo ""
echo "🔧 Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo -e "${GREEN}✓ Pre-commit hooks installed${NC}"
else
    echo -e "${YELLOW}⚠ pre-commit not found, skipping hooks setup${NC}"
fi

# Create .env from template
echo ""
echo "⚙️  Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created from template${NC}"
    echo -e "${YELLOW}⚠ Please edit .env file with your API keys${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists, skipping${NC}"
fi

# Create necessary directories
echo ""
echo "📁 Creating project directories..."
mkdir -p shared/queue
mkdir -p shared/data/videos
mkdir -p shared/data/reports
mkdir -p shared/data/code
mkdir -p shared/logs
echo -e "${GREEN}✓ Directories created${NC}"

# Run tests to verify setup
echo ""
echo "🧪 Running tests to verify setup..."
pytest tests/ -v || echo -e "${YELLOW}⚠ Some tests failed, but setup is complete${NC}"

# Final message
echo ""
echo "=================================="
echo -e "${GREEN}✅ Setup complete!${NC}"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - ANTHROPIC_API_KEY"
echo "   - GITHUB_TOKEN"
echo "   - GITHUB_REPO"
echo ""
echo "2. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the system:"
echo "   python orchestrator/main.py"
echo ""
echo "📚 Read QUICKSTART.md for more information"
echo ""
