import os
import requests
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from uuid import uuid4
from PIL import Image
import io
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configuration
IMAGE_SAVE_FOLDER = "generated_images"
os.makedirs(IMAGE_SAVE_FOLDER, exist_ok=True)

AZURE_OPENAI_ENDPOINT = "https://auraemodel.cognitiveservices.azure.com/"
AZURE_OPENAI_KEY = "8G7OQeuO5JSuG1sLALSvyWpNwEk82O7FyyA8gfRoDFTfKH2qBX4MJQQJ99BGACYeBjFXJ3w3AAAAACOGWivX"
DEPLOYMENT_NAME = "dall-e-3"
API_VERSION = "2024-02-01"

class PromptRequest(BaseModel):
    prompt: str

def call_azure_openai(prompt: str):
    url = (
        f"{AZURE_OPENAI_ENDPOINT}openai/deployments/"
        f"{DEPLOYMENT_NAME}/images/generations?api-version={API_VERSION}"
    )
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to generate image: {response.text}")
    return response.json()

def save_image_from_url(image_url: str, folder: str) -> str:
    response = requests.get(image_url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to download image")
    image = Image.open(io.BytesIO(response.content))
    filename = f"{uuid4().hex}.png"
    filepath = os.path.join(folder, filename)
    image.save(filepath)
    return filepath

app.mount("/images", StaticFiles(directory=IMAGE_SAVE_FOLDER), name="images")

@app.post("/generate-image/")
async def generate_image(request: PromptRequest, req: Request):
    result = call_azure_openai(request.prompt)
    image_url = result["data"][0]["url"]  # Adjust if the response structure is different
    filepath = save_image_from_url(image_url, IMAGE_SAVE_FOLDER)
    filename = os.path.basename(filepath)
    base_url = str(req.base_url).rstrip("/")
    image_access_url = f"{base_url}/images/{filename}"
    return {"image_url": image_access_url} 