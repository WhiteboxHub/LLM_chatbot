import streamlit as st
from dotenv import load_dotenv
import os
from llm_2_opensource import LLM_model_Groq  # Import your LLM_model function

# Load environment variables
load_dotenv()

# Check if the API key is already set in the session state
if 'groq_api_key' not in st.session_state:
    st.session_state['groq_api_key'] = None

# Set up Streamlit app
st.title("LLM SQL Chatbot")
st.write("Ask questions about financial advisors and disclosures.")

# Only prompt for API key if it hasn't been set
if st.session_state['groq_api_key'] is None:
    groq_api_key = st.text_input("Enter your Groq API key:", type="password")
    if groq_api_key:
        # Store the API key in session state and set it as an environment variable
        st.session_state['groq_api_key'] = groq_api_key
        os.environ['GROQ_API_KEY'] = groq_api_key
        st.success("Groq API key set successfully!")
else:
    st.write("Groq API key is already set.")

# Capture user input for the question
question = st.text_input("Enter your question:")

# When the user submits the question
if st.button("Submit"):
    if not question:
        st.error("Please enter a question.")
    else:
        with st.spinner("Processing..."):
            try:
                # Call the LLM_model function with the user's question
                response = LLM_model_Groq(question)
                st.write("**Question:**", question)
                st.write("**Answer:**", response['output'])
            except Exception as e:
                st.error(f"An error occurred: {e}")
