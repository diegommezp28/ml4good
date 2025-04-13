import streamlit as st
import openai
from typing import List, Dict, Optional
import json

# Set page config
st.set_page_config(page_title="Debating Agents", page_icon="🤖", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_started" not in st.session_state:
    st.session_state.conversation_started = False
if "current_turn" not in st.session_state:
    st.session_state.current_turn = 0
if "max_messages" not in st.session_state:
    st.session_state.max_messages = 10

# Title
st.title("Debating Agents Interface")

# Sidebar for API key and settings
with st.sidebar:
    st.header("Settings")

    # API Key input
    api_key = st.text_input(
        "OpenAI API Key", type="password", help="Enter your OpenAI API key"
    )

    # Model selection
    model = st.selectbox(
        "Model",
        [
            "gpt-4-turbo-preview",
            "gpt-4",
            "gpt-4-32k",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-instruct",
        ],
        help="Select the OpenAI model to use",
    )

    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness in the model's responses",
    )

# Main interface
if not st.session_state.conversation_started:
    st.header("Start a New Conversation")

    # Subject input
    subject = st.text_area(
        "Conversation Subject", help="Enter the topic for the chatbots to discuss"
    )

    # Message limit input
    message_limit = st.number_input(
        "Maximum Number of Messages",
        min_value=1,
        max_value=50,
        value=10,
        help="Set the maximum number of back-and-forth messages",
    )

    if st.button("Start Conversation") and subject and api_key:
        st.session_state.max_messages = message_limit
        st.session_state.conversation_started = True
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are Chatbot 1. You are having a discussion with "
                    f"Chatbot 2 about {subject}. Be concise and direct in "
                    "your responses."
                ),
            },
            {
                "role": "system",
                "content": (
                    "You are Chatbot 2. You are having a discussion with "
                    f"Chatbot 1 about {subject}. Be concise and direct in "
                    "your responses."
                ),
            },
            {
                "role": "assistant",
                "content": f"Chatbot 1: Let's discuss {subject}. What are your thoughts?",
            },
        ]
        st.session_state.current_turn = 1
        st.rerun()

else:
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=api_key)

    # Function to get response from OpenAI
    def get_openai_response(messages: List[Dict[str, str]]) -> Optional[str]:
        try:
            response = client.chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error getting response from OpenAI: {str(e)}")
            return None

    # Display conversation
    st.header("Conversation")

    # Create two columns for the chat messages
    left_col, right_col = st.columns(2)

    # Show messages
    for message in st.session_state.messages[2:]:  # Skip system messages
        content = message["content"]
        if "Chatbot 1:" in content:
            with left_col:
                with st.chat_message("assistant"):
                    st.write(content.replace("Chatbot 1:", "").strip())
        else:
            with right_col:
                with st.chat_message("assistant"):
                    st.write(content.replace("Chatbot 2:", "").strip())

    # Continue conversation if not reached max messages
    if st.session_state.current_turn < st.session_state.max_messages:
        # Get the last message
        last_message = st.session_state.messages[-1]["content"]

        # Determine which chatbot should respond
        current_chatbot = "Chatbot 2" if "Chatbot 1:" in last_message else "Chatbot 1"

        # Get response
        response = get_openai_response(st.session_state.messages)
        if response:
            st.session_state.messages.append(
                {"role": "assistant", "content": f"{current_chatbot}: {response}"}
            )
            st.session_state.current_turn += 1
            st.rerun()
    else:
        st.success("Conversation completed!")
        if st.button("Start New Conversation"):
            st.session_state.conversation_started = False
            st.session_state.messages = []
            st.session_state.current_turn = 0
            st.rerun()

# Debug section (can be removed in production)
with st.expander("Debug Information"):
    st.write("Current messages:", json.dumps(st.session_state.messages, indent=2))
    st.write(f"Current turn: {st.session_state.current_turn}")
    st.write(f"Max messages: {st.session_state.max_messages}")
