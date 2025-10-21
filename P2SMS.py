import streamlit as st
import requests

st.title("📲 Power2SMS Client")

# Load credentials from Streamlit secrets
username = st.secrets["P2SMS_USERNAME"]
secret = st.secrets["P2SMS_SECRET"]

BASE_URL = "https://www.power2sms.co.uk/api/1/v1"

# Cache authentication for 1 hour
@st.cache_data(ttl=3600)
def authenticate(username, secret):
    url = f"{BASE_URL}" 
    payload = {
        "username": username,
        "secret": secret
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

try:
    auth_data = authenticate(username, secret)
    st.success(f"Authenticated! 👋 Logged in as {username}")
except requests.RequestException as e:
    st.error(f"Authentication failed: {e}")
    st.stop()

# Function to check balance
@st.cache_data
def check_balance(username, secret, subaccount_name=None):
    url = f"{BASE_URL}/acc/balance"
    payload = {
        "username": username,
        "secret": secret
    }
    if subaccount_name:
        payload["subaccount_name"] = subaccount_name

    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

# Opitional Subaccount Name
subaccount = st.text_input("Subaccount Name (optional)")

if st.button("🔍 Check Balance"):
    try:
        balance_data = check_balance(username, secret, subaccount)
        st.json(balance_data)
    except requests.RequestException as e:
        st.error(f"Error checking balance: {e}")
