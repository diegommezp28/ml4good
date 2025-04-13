import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Debating Agents", page_icon="🤖", layout="wide")

# Title
st.title("Debating Agents Interface")

# Sidebar
st.sidebar.header("Settings")
api_url = st.sidebar.text_input("API URL", "http://app:8000")

# Main content
st.header("Welcome to the Debating Agents Platform")

# Example of API interaction
if st.button("Get API Status"):
    try:
        response = requests.get(f"{api_url}/")
        if response.status_code == 200:
            st.success(f"API is running! Message: {response.json()['message']}")
        else:
            st.error(f"API returned status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")

# Add some example content
st.markdown(
    """
### About
This is a simple interface for interacting with the Debating Agents API.

### Features
- Real-time API status checking
- Easy-to-use interface
- Responsive design
"""
)
