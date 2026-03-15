#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}🚀 Starting GraphQL Server...${NC}"
echo ""

# Check if venv is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo -e "${YELLOW}⚠️  Virtual environment not activated!${NC}"
    echo -e "${CYAN}Activating venv...${NC}"
    source venv/bin/activate
fi

echo -e "${GREEN}✅ Virtual environment active${NC}"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  📡 Server starting...${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}  🌐 GraphQL Playground will be available at:${NC}"
echo ""
echo -e "${GREEN}  👉 http://localhost:8000/graphql${NC}"
echo -e "${GREEN}  👉 http://127.0.0.1:8000/graphql${NC}"
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}  Press Ctrl+C to stop the server${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Start the server
python main.py
