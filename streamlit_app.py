# streamlit_app.py

import streamlit as st
import requests
import os
from utils import call_azure_openai, save_image_from_url

PAYSTACK_SECRET_KEY = st.secrets["PAYSTACK_SECRET_KEY"] if "PAYSTACK_SECRET_KEY" in st.secrets else os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = st.secrets["PAYSTACK_PUBLIC_KEY"] if "PAYSTACK_PUBLIC_KEY" in st.secrets else os.getenv("PAYSTACK_PUBLIC_KEY")
BACKEND_URL = "https://auraelabs.streamlit.app/"

st.set_page_config(page_title="Medical Image Generator", layout="centered")
st.title("Medical Image Generator with Azure DALL·E 3")

prompt = st.text_area("Enter your image prompt:", height=150, placeholder="e.g. A simplified anatomical diagram...")

if "show_payment" not in st.session_state:
    st.session_state.show_payment = False
if "paystack_ref" not in st.session_state:
    st.session_state.paystack_ref = None
if "free_used" not in st.session_state:
    st.session_state.free_used = False

# Determine if the Generate Image button should be enabled
generate_enabled = not st.session_state.free_used or st.session_state.paystack_ref

if not generate_enabled:
    st.warning("You have used your free image. Please support us to generate more images!")

# Only run image generation logic if allowed
if st.button("Generate Image", disabled=not generate_enabled):
    # If user has paid, allow unlimited generations
    if st.session_state.paystack_ref:
        st.session_state.show_payment = False
        # Generate image (paid)
        if prompt.strip():
            with st.spinner("Generating image..."):
                try:
                    image_url = call_azure_openai(prompt)
                    image_path = save_image_from_url(image_url)
                    st.success("Image generated successfully!")
                    st.image(image_path, caption="Generated Medical Training Image")
                except Exception as e:
                    st.error(f"Error generating image: {str(e)}")
        else:
            st.warning("Please enter a prompt above and click Generate Image.")
    # If user hasn't paid and already used free, force payment (do NOT generate image)
    elif st.session_state.free_used:
        st.session_state.show_payment = True
    else:
        # Allow one free generation
        st.session_state.show_payment = False
        st.session_state.free_used = True
        # Generate image (free)
        if prompt.strip():
            with st.spinner("Generating your free image..."):
                try:
                    image_url = call_azure_openai(prompt)
                    image_path = save_image_from_url(image_url)
                    st.success("Image generated successfully! (Free tier)")
                    st.image(image_path, caption="Generated Medical Training Image")
                except Exception as e:
                    st.error(f"Error generating image: {str(e)}")
        else:
            st.warning("Please enter a prompt above and click Generate Image.")

if st.session_state.show_payment and not st.session_state.paystack_ref:
    st.info("Support us with $1 to generate your image! Your contribution helps keep this service running.")
    email = st.text_input("Enter your email for payment receipt:")
    if st.button("Pay $1 with Paystack") and email:
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "amount": 100 * 100,  # Paystack expects amount in kobo (100 kobo = 1 NGN)
            "currency": "USD",    # Or "NGN" if you want to charge in Naira
            "callback_url": f"{BACKEND_URL}?paystack_ref={{reference}}"
        }
        resp = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
        if resp.status_code == 200 and resp.json()["status"]:
            pay_url = resp.json()["data"]["authorization_url"]
            st.markdown(f"[Click here to pay with Paystack]({pay_url})")
        else:
            st.error("Failed to initialize Paystack payment. Please try again.")
            st.write("Paystack response:", resp.json())
        st.stop()

# Handle Paystack redirect after payment
query_params = st.query_params
paystack_ref = query_params.get("paystack_ref", [None])[0]
if paystack_ref and not st.session_state.paystack_ref:
    st.session_state.paystack_ref = paystack_ref
    st.session_state.show_payment = False

# If payment is verified, allow image generation (unlimited)
if st.session_state.paystack_ref:
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"
    }
    verify_url = f"https://api.paystack.co/transaction/verify/{st.session_state.paystack_ref}"
    resp = requests.get(verify_url, headers=headers)
    if resp.status_code == 200 and resp.json()["data"]["status"] == "success":
        st.success("Thank you for your support! You can now generate unlimited images.")
    else:
        st.error("Payment not verified. Please try again.")
        st.session_state.paystack_ref = None
