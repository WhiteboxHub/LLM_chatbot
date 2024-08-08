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
pg_uri = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
db = SQLDatabase.from_uri(pg_uri)

# Initialize the ChatOpenAI model correctly
# gpt = OpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')


# toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
# agent_executor = create_sql_agent(
#     llm=gpt,
#     toolkit=toolkit,
#     verbose=True,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
# )

try:
        
    gpt = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')

    agent_executor = create_sql_agent(
        llm=gpt,
        db=db,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )


    question = "give damage amount of the disclousers information of the user with CRD=1000034"
    result = agent_executor.invoke(question)
    print(result)

except Exception as e :
    print(e)

