import psutil, streamlit as st
import requests

st.metric("CPU Usage", f"{psutil.cpu_percent()}%")
if st.button("Restart API Service"):
    requests.post("https://internal.api/restart")
