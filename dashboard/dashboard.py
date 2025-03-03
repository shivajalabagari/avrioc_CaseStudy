# dashboard/dashboard.py
import streamlit as st
import requests

st.title("Real-time Interaction Metrics")
response = requests.get('http://localhost:5000/metrics').json()

st.write(f"Avg interactions per user: {response['avg_interactions_per_user']}")
st.write(f"Max interactions per item: {response['max_interactions_per_item']}")
st.write(f"Min interactions per item: {response['min_interactions_per_item']}")
