# streamlit_app.py

import streamlit as st
from utils import call_azure_openai, save_image_from_url
import os

st.set_page_config(page_title="Medical Image Generator", layout="centered")

st.title("Medical Image Generator with Azure DALL·E 3")
st.write("Enter a medical prompt to generate a labeled training image.")

# Prompt input
prompt = st.text_area("Enter your image prompt:", height=150, placeholder="e.g. A simplified anatomical diagram...")

if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            try:
                image_url = call_azure_openai(prompt)
                image_path = save_image_from_url(image_url)

                st.success("Image generated successfully!")
                st.image(image_path, caption="Generated Medical Training Image")

            except Exception as e:
                st.error(f"Error generating image: {str(e)}")
