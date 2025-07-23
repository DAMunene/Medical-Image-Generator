import streamlit as st
import requests
import os

# Set FastAPI backend URL - use environment variable or fallback to Railway deployment
BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "https://wonderful-mindfulness.railway.app/generate-image/")

st.title("Medical Image Generator with Azure DALL·E 3")
st.write("Enter a medical prompt to generate a labeled training image using Azure DALL·E 3")

# Prompt input
prompt = st.text_area("Enter your image prompt:", height=150, placeholder="e.g. A simplified anatomical diagram...")

if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            try:
                # Send POST request to FastAPI
                response = requests.post(BACKEND_URL, json={"prompt": prompt})
                response.raise_for_status()
                image_url = response.json().get("image_url")

                # Display image
                if image_url:
                    st.success("Image generated successfully!")
                    st.image(image_url, caption="Generated Medical Training Image")
                else:
                    st.error("No image URL returned from the API.")

            except requests.exceptions.RequestException as e:
                st.error(f"API error: {e}")
                st.info("Make sure your FastAPI backend is running and accessible.")
