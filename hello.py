import streamlit as st
import requests

st.set_page_config(page_title="Dashboard")
st.title("Dashboard")

st.markdown("""
<style>
/* Make the expander label text larger */

div[data-testid="stExpander"] > details > summary p 
    {
        font-size: 1.5rem !important; 
        font-weight: bold !important;
        /*color: #ff4b4b !important;*/
    }
</style>
""", 
unsafe_allow_html=True)

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

  payloadMessageCheck = {
      "username": username,
      "secret": secret,
      "sendIds": ""
      #"messageIds": ""
  }

  payloadWebform = {
      "username": "TEST",
      "password": "TEST",
  }

  headers = {
      "Content-Type": "application/json"
  }

  try:
      response = requests.post(f"{BASE_URL}/acc/balance", data=payload)
      response.raise_for_status()
      print("✅ API is up!")
      print(response.json())
      
      with col1:
          st.write("API")
          st.success("✅ Up")  # Show success in dashboard
      with col2:
          st.write("Balance")
          st.warning(response.json()["sms_credits"])

  except requests.RequestException as e:
      print("❌ API check failed:", e)
      
      with col1:
          st.write("API")
          st.error("❌ Down")  # Use st.error() for failures
      with col2:
          st.write("Balance")
          st.error("❌ Down")

  try:
      response = requests.post(f"{BASE_URL}/sms/report", data=payloadMessageCheck)
      response.raise_for_status()
      data = response.json()
      #st.write(response.json()) Bollocks
      
      messages = data.get("result", [])  # safe access to the list

      # Filter delivered messages
      delivered = [msg for msg in messages if msg.get("status") == "Delivered"]

      with col3:
          st.write("Delivered")
          if delivered:
              for msg in delivered:
                  st.json(msg)  # nicely formatted JSON
          else:
              st.info("Needs V3 API.")
        
  except requests.RequestException as e:
      print("❌ API check failed:", e)
      with col3:
        st.write("Messages")
        st.error("❌ Down")

#Production Check
with st.expander("Production Health Check", expanded=True):

  col1, col2, col3 = st.columns(3)
  with col1:
    st.write("ERS-SA")
    try:
        response = requests.get("https://secure.refer-all.net/ers-sa/", timeout=5)  # short timeout to avoid hanging
        if response.ok:  # status_code 200–299
            st.success(f"✅ Website is up! ({response.status_code})")
        else:
            st.warning(f"⚠️ Website returned status {response.status_code}")
    except requests.RequestException as e:
        st.error(f"❌ Website is down or unreachable: {e}")

  with col2:
    st.write("Questionnaire API") #NOTE I should probably make this shit actually point at the questionnaire svc, this just looks at MemberUI
                                  # which could work without Q-SVC, CANT REMEMBER WHICH APP POOL Q-SVC USES! FIND OUT!!!!
    try:
        response = requests.get("https://secure.refer-all.net/member/svc/GetReferralData.asmx", timeout=5)  # short timeout to avoid hanging
        if response.ok:  # status_code 200–299
            st.success(f"✅ API is up! ({response.status_code})")
        else:
            st.warning(f"⚠️ API returned status {response.status_code}")
    except requests.RequestException as e:
        st.error(f"❌ Website is down or unreachable: {e}")

  with col3:
    try:
      st.write("Webform API (401 = fine)")
      response = requests.post(f"https://secure.refer-all.net/api/webformapi/v1/Authorization/Authenticate", headers=headers, json=payloadWebform)
      #response.raise_for_status()
      if response.ok:  # status_code 200–299
        st.success(f"✅ API is up! ({response.status_code})")
      if response.status_code == 401:
        st.warning(f"⚠️ API returned status {response.status_code}")
      else:
        st.warning(f"⚠️ API returned status {response.status_code}")
      print(response.json())
    except requests.RequestException as e:
      if response.status_code != 401:
        print("❌ API check failed:", e)
        st.error(f"❌ Down ({response.status_code})")  # Use st.error() for failures

#Staging Check
with st.expander("Staging Health Check", expanded=True):

  col1, col2, col3 = st.columns(3)

  with col1:
    st.write("Staging SA")
    try:
        response = requests.get("https://secure.refer-all.net/staging/sa/", timeout=5)  # short timeout to avoid hanging
        if response.ok:  # status_code 200–299
            st.success(f"✅ Website is up! ({response.status_code})")
        else:
            st.warning(f"⚠️ Website returned status {response.status_code}")
    except requests.RequestException as e:
        st.error(f"❌ Website is down or unreachable: {e}")