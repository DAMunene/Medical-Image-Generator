# utils.py

import os
import requests
from uuid import uuid4
from PIL import Image
import io
from dotenv import load_dotenv

# Load env vars
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")
IMAGE_SAVE_FOLDER = "generated_images"
os.makedirs(IMAGE_SAVE_FOLDER, exist_ok=True)

def call_azure_openai(prompt: str) -> str:
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
    response.raise_for_status()
    return response.json()["data"][0]["url"]

def save_image_from_url(image_url: str) -> str:
    response = requests.get(image_url)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content))
    filename = f"{uuid4().hex}.png"
    filepath = os.path.join(IMAGE_SAVE_FOLDER, filename)
    image.save(filepath)
    return filepath
