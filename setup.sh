#!/bin/bash
# Setup script for Selatek Notes
# Voice-to-Word PWA with Modal backend

echo "=== Selatek Notes Setup ==="

# Check Python
if ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed"
    exit 1
fi
echo "Python found: $(python --version)"

# Check Modal CLI
if ! command -v modal &> /dev/null; then
    echo "Installing Modal CLI..."
    pip install modal
else
    echo "Modal CLI found: $(modal --version)"
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install python-docx fastapi

# Check Modal authentication
echo "Checking Modal authentication..."
modal token show 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Please authenticate with Modal:"
    echo "  modal token new"
    exit 1
fi

# Deploy backend (exp-002)
echo ""
echo "=== Deploying Backend (voice-accumulator) ==="
cd experiments/voice-to-modal/exp-002
modal deploy app.py
cd ../../..

# Deploy frontend PWA (exp-003)
echo ""
echo "=== Deploying Frontend PWA (selatek-notes-pwa) ==="
cd experiments/voice-to-modal/exp-003
modal deploy app.py
cd ../../..

echo ""
echo "=== Setup Complete ==="
echo "Backend endpoints:"
echo "  - https://mackanh1972--voice-accumulator-accumulate.modal.run"
echo "  - https://mackanh1972--voice-accumulator-add-image.modal.run"
echo "  - https://mackanh1972--voice-accumulator-save-to-word.modal.run"
echo ""
echo "Frontend PWA:"
echo "  - https://mackanh1972--selatek-notes-pwa-web.modal.run"
