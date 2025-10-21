import streamlit as st
import requests

st.set_page_config(page_title="Dashboard")
st.title("Dashboard")

#P2SMS API Check
with st.expander("Power2SMS API Health Check", expanded=True):

  col1, col2, col3 = st.columns(3)

  username = st.secrets["P2SMS_USERNAME"]
  secret = st.secrets["P2SMS_SECRET"]

  BASE_URL = "https://www.power2sms.co.uk/api/1/v1"
  payload = {
      "username": username,
      "secret": secret
  }

  payload2 = {
      "username": username,
      "secret": secret,
      "sendIds": "3157337"
      #"messageIds": ""
  }

  try:
      response = requests.post(f"{BASE_URL}/acc/balance", data=payload)
      response.raise_for_status()
      print("✅ API is up!")
      print(response.json())
      
      with col1:
          st.subheader("API")
          st.success("✅ Up")  # Show success in dashboard
      with col2:
          st.subheader("Balance")
          st.warning(response.json()["sms_credits"])

  except requests.RequestException as e:
      print("❌ API check failed:", e)
      
      with col1:
          st.header("API")
          st.error("❌ Down")  # Use st.error() for failures
      with col2:
          st.subheader("Balance")
          st.error("❌ Down")

  try:
      response = requests.post(f"{BASE_URL}/sms/report", data=payload2)
      response.raise_for_status()
      data = response.json()
      #st.write(response.json()) Bollocks
      
      messages = data.get("result", [])  # safe access to the list

      # Filter delivered messages
      delivered = [msg for msg in messages if msg.get("status") == "Delivered"]

      with col3:
          st.subheader("Delivered")
          if delivered:
              for msg in delivered:
                  st.json(msg)  # nicely formatted JSON
          else:
              st.info("Needs V3 API.")
        
  except requests.RequestException as e:
      print("❌ API check failed:", e)
      with col3:
        st.subheader("Messages")
        st.error("❌ Down")

#Production Check
with st.expander("Production Health Check", expanded=True):

  #col1, col2, col3 = st.columns(3)
  st.subheader("secure.refer-all.net/ers-sa/")

  try:
      response = requests.get("https://secure.refer-all.net/ers-sa/", timeout=5)  # short timeout to avoid hanging
      if response.ok:  # status_code 200–299
          st.success(f"✅ Website is up! ({response.status_code})")
      else:
          st.warning(f"⚠️ Website returned status {response.status_code}")
  except requests.RequestException as e:
      st.error(f"❌ Website is down or unreachable: {e}")

#Staging Check
with st.expander("Staging Health Check", expanded=True):

  #col1, col2, col3 = st.columns(3)
  st.subheader("secure.refer-all.net/staging/sa/")

  try:
      response = requests.get("https://secure.refer-all.net/staging/sa/", timeout=5)  # short timeout to avoid hanging
      if response.ok:  # status_code 200–299
          st.success(f"✅ Website is up! ({response.status_code})")
      else:
          st.warning(f"⚠️ Website returned status {response.status_code}")
  except requests.RequestException as e:
      st.error(f"❌ Website is down or unreachable: {e}")