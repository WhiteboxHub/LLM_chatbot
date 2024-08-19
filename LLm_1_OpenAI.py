from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit 
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
pg_uri = os.getenv('DATABASE_URI')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
db = SQLDatabase.from_uri(pg_uri)

def LLM_model(question):
    try:
            
        gpt = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')
        
        agent_executor = create_sql_agent(
            llm=gpt,
            db=db,
            handle_parsing_errors=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )


        # question = "are there any disclosures denied for the phone 3108936060?"
        # question = 'how many different people live at this zip code 60606'
        # question = 'Tell me more about Debora nunez'
        # question = 'Tell me more about Colleen Rielle pedey'
        # question = 'Does elisabeth hickox have any disclosure? If so what was the allegation and how recent and what was the dollar amount?'
        
        result = agent_executor.invoke(question)
        return result

    except Exception as e :
        print(e)

