#!/bin/bash

# TerraPulse AI - Streamlit Frontend Launcher
# This script starts the Streamlit app on Linux/Mac

echo ""
echo "===================================="
echo " TerraPulse AI - Streamlit Frontend"
echo "===================================="
echo ""

# Check if streamlit is installed
python -m pip show streamlit >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing Streamlit and dependencies..."
    python -m pip install -r requirements_streamlit.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "✓ Starting Streamlit app on http://localhost:8501"
echo ""
echo "Make sure the backend is running on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
python -m streamlit run app_streamlit.py
