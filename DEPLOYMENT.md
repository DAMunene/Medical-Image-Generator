# Medical Image Generator - Project Structure & Deployment Guide

## 📁 Project Structure

```
dalle-3/
├── main.py                 # FastAPI backend server
├── streamlit_app.py        # Streamlit frontend interface
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
├── Procfile               # Deployment configuration
├── DEPLOYMENT.md          # This deployment guide
├── generated_images/      # Folder for saved images (auto-created)
└── venv/                  # Virtual environment (ignored by git)
```

### File Descriptions

- **`main.py`**: FastAPI backend that handles DALL-E 3 API calls and image generation
- **`streamlit_app.py`**: User-friendly web interface for the image generator
- **`requirements.txt`**: Lists all Python packages needed for the project
- **`.env`**: Contains Azure OpenAI credentials (not committed to git)
- **`Procfile`**: Tells deployment platforms how to run the FastAPI app
- **`generated_images/`**: Directory where generated images are saved

## 🚀 Current Deployment Status

- ✅ **Streamlit Frontend**: Deployed at `https://auraelabs.streamlit.app/`
- ✅ **FastAPI Backend**: Deployed at `https://wonderful-mindfulness.railway.app/`
- ✅ **GitHub Repository**: `https://github.com/DAMunene/Medical-Image-Generator.git`

## Current Issue
Your Streamlit app is deployed at `https://auraelabs.streamlit.app/` but it's trying to connect to a local FastAPI server (`127.0.0.1:8000`) which doesn't exist in production.

## Solution: Deploy FastAPI Backend

### Option 1: Deploy to Railway (Recommended - Easy)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect your GitHub repository**
3. **Add environment variables** in Railway dashboard:
   ```
   AZURE_OPENAI_ENDPOINT=https://auraemodel.cognitiveservices.azure.com/
   AZURE_OPENAI_KEY=your_api_key_here
   DEPLOYMENT_NAME=dall-e-3
   API_VERSION=2024-02-01
   ```
4. **Deploy** - Railway will automatically detect it's a Python app
5. **Get your FastAPI URL** (e.g., `https://your-app.railway.app`)

### Option 2: Deploy to Render

1. **Sign up** at [render.com](https://render.com)
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Set build command**: `pip install -r requirements.txt`
5. **Set start command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Add environment variables** (same as above)

### Option 3: Deploy to Heroku

1. **Sign up** at [heroku.com](https://heroku.com)
2. **Install Heroku CLI**
3. **Create app**: `heroku create your-app-name`
4. **Set environment variables**:
   ```bash
   heroku config:set AZURE_OPENAI_ENDPOINT=https://auraemodel.cognitiveservices.azure.com/
   heroku config:set AZURE_OPENAI_KEY=your_api_key_here
   heroku config:set DEPLOYMENT_NAME=dall-e-3
   heroku config:set API_VERSION=2024-02-01
   ```
5. **Deploy**: `git push heroku main`

## 🔧 Update Streamlit Configuration

After deploying your FastAPI backend, update your Streamlit app to use the new URL:

1. **Set environment variable** in Streamlit Cloud:
   ```
   FASTAPI_BACKEND_URL=https://your-deployed-app.railway.app/generate-image/
   ```

2. **Or update the code** in `streamlit_app.py`:
   ```python
   BACKEND_URL = "https://your-deployed-app.railway.app/generate-image/"
   ```

## 🧪 Testing Your Deployment

### Test FastAPI Backend
```bash
curl -X POST "https://your-app.railway.app/generate-image/" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "A simple medical diagram"}'
```

### Test Complete Flow
1. Go to your Streamlit app: `https://auraelabs.streamlit.app/`
2. Enter a prompt
3. Click "Generate Image"
4. Verify the image appears

## 🔒 Security Notes

- ✅ `.env` file is in `.gitignore` (credentials not in git)
- ✅ Environment variables used in production
- ✅ API keys stored securely in deployment platforms

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI resource endpoint | `https://auraemodel.cognitiveservices.azure.com/` |
| `AZURE_OPENAI_KEY` | Your Azure OpenAI API key | `your_api_key_here` |
| `DEPLOYMENT_NAME` | Your DALL-E 3 deployment name | `dall-e-3` |
| `API_VERSION` | Azure OpenAI API version | `2024-02-01` |
| `FASTAPI_BACKEND_URL` | Your deployed FastAPI URL | `https://your-app.railway.app/generate-image/` | 