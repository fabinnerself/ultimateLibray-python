#!/usr/bin/env python3
"""
Quick start script for Ultimate Library API
Run this to start the development server quickly
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import fastapi
        import uvicorn
        import motor
        import pydantic
        import jose
        import passlib
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists():
        if env_example_path.exists():
            print("⚠️  .env file not found. Please copy .env.example to .env and configure it.")
            print("Example:")
            print("cp .env.example .env")
        else:
            print("❌ Neither .env nor .env.example found!")
        return False
    
    print("✅ .env file found")
    return True

def start_server():
    """Start the FastAPI development server"""
    print("🚀 Starting Ultimate Library API...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Alternative docs at: http://localhost:8000/redoc")
    print("❤️  Health check at: http://localhost:8000/health")
    print("\nPress CTRL+C to stop the server\n")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api.main:app", 
            "--reload", 
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")

def main():
    """Main function"""
    print("🚀 Ultimate Library API - Quick Start")
    print("=====================================\n")
    
    # Check requirements
    if not check_requirements():
        return
    
    # Check environment file
    if not check_env_file():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
