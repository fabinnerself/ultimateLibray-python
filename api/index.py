"""
Vercel serverless function entry point for Ultimate Library API
This file is specifically designed for Vercel deployment
"""

from .main import app
from mangum import Mangum

# Create the Mangum handler for Vercel
handler = Mangum(app, lifespan="off")

# For direct import
application = app

# This ensures the app is available for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
