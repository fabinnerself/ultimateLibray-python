#!/usr/bin/env python3
"""
Vercel entry point for FastAPI application
"""
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

# This is the entry point for Vercel
handler = app
