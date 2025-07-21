#!/bin/bash

# Audio file converter script runner
# This script ensures the virtual environment is activated before running the converter

echo "Activating virtual environment and running audio converter..."
source venv/bin/activate && python convert_to_mp3.py
