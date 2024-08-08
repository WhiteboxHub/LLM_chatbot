import os

import requests
import streamlit as st

CHATBOT_URL = os.getenv(
    "CHATBOT_URL", "http://localhost:8000/hospital-rag-agent"
)

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        data that has been synthetically generated.
        """
    )

    st.header("Example Questions")
    st.markdown("- Question1")
    st.markdown(
        """- Question1?"""
    )
    st.markdown(
        """- Question2?"""
    )
    st.markdown(
        "- Question3?"
    )
    st.markdown(
        """- Question4?"""
    )
 



st.title("System Chatbot")
st.info(
    """Ask me questions about CRD!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Searching for an answer..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
