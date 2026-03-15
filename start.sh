#!/bin/bash
# Quick Start Script for Smart Electricity Billing System

echo "🔌 Smart Electricity Billing System - Quick Start"
echo "=================================================="
echo ""

# Check if venv exists
if [ -d "venv" ]; then
    echo "✅ Using virtual environment (venv)"
    echo "🚀 Starting server on http://localhost:8000"
    echo "📊 GraphQL Playground: http://localhost:8000/graphql"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    venv/bin/python main.py
else
    # Fallback to system Python3
    if ! command -v python3 &> /dev/null
    then
        echo "❌ Python3 is not installed. Please install Python3 first."
        exit 1
    fi
    
    echo "✅ Python3 found: $(python3 --version)"
    echo ""
    echo "🚀 Starting server on http://localhost:8000"
    echo "📊 GraphQL Playground: http://localhost:8000/graphql"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    python3 main.py
fi
