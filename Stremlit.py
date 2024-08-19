import streamlit as st
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import os
from dotenv import load_dotenv
from LLm_1 import LLM_model
# Load environment variables
load_dotenv()

# Initialize database and LLM
pg_uri = os.getenv('DATABASE_URI')
db = SQLDatabase.from_uri(pg_uri)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
gpt = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

# Create the SQL agent
agent_executor = create_sql_agent(
    llm=gpt,
    db=db,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# Streamlit app
st.title("LLM SQL Chatbot")
st.write("Ask questions about financial advisors and disclosures.")

# Capture user input
question = st.text_input("Enter your question:")

# When the user submits the question
if st.button("Submit"):
    with st.spinner("Processing..."):
        try:
            result = LLM_model(question)
            st.write("**Question:**", question)
            st.write("**Answer:**", result['output'])
        except Exception as e:
            st.error(f"An error occurred: {e}")
