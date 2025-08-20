# Deployment Guide for Vercel

## 📋 Pre-deployment Checklist

✅ **Project Structure Fixed**: 
- Updated `vercel.json` with correct configuration
- Created `api/index.py` as entry point
- Updated `requirements.txt` with Mangum adapter
- Set environment to production

## 🚀 Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Set Environment Variables in Vercel
You need to set these environment variables in your Vercel project dashboard:

```
MONGODB_CONNECT_URI=mongodb+srv://fabinnerself:qnYpJAhS4sJSSAQQ@mymongodb.aofqgrl.mongodb.net/?retryWrites=true&w=majority&appName=mymongodb
SECRET_KEY=qnYpJAhS4sJSSAQQ
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_PREFIX=/api/v1
PROJECT_NAME=Ultimate Library API
VERSION=1.0.0
DESCRIPTION=A FastAPI application for managing books and users
ENVIRONMENT=production
PORT=8000
DATABASE_NAME=ultimate_library
```

### 4. Deploy to Vercel
From your project directory:
```bash
vercel --prod
```

Or deploy using Git (recommended):
1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Vercel will automatically deploy

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
```

### api/index.py (Entry Point)
```python
from .main import app
from mangum import Mangum

# Create the Mangum handler for Vercel
handler = Mangum(app, lifespan="off")
```

## 🌐 After Deployment

Your API will be available at:
- Main URL: `https://your-project-name.vercel.app/`
- Health Check: `https://your-project-name.vercel.app/health`
- API endpoints: `https://your-project-name.vercel.app/api/v1/...`

## 🔍 Troubleshooting

### Common Issues:

1. **Function Invocation Failed**
   - Check that all environment variables are set in Vercel dashboard
   - Verify MongoDB connection string is correct
   - Check function timeout limits

2. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility (using 3.9)

3. **Database Connection Issues**
   - Verify MongoDB Atlas allows connections from anywhere (0.0.0.0/0)
   - Check that the connection string includes proper authentication

### Debug Steps:
1. Check Vercel function logs
2. Test endpoints locally first
3. Verify environment variables are properly set
4. Check MongoDB Atlas network access settings

## 📦 Project Structure
```
userBE/
├── api/
│   ├── __init__.py
│   ├── index.py          # Vercel entry point
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── database.py       # MongoDB connection
│   ├── models/
│   ├── routers/
│   └── auth/
├── requirements.txt
├── vercel.json          # Vercel configuration
└── .env                 # Local environment (don't commit this)
```

## 🔒 Security Notes
- Never commit `.env` file to git
- Use strong, unique SECRET_KEY for production
- Configure proper CORS origins for your frontend
- Set up proper MongoDB user permissions
