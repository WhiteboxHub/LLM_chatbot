from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit 
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI
import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
pg_uri = "postgresql+psycopg2://postgres:password@localhost:5432/postgres"

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
db = SQLDatabase.from_uri(pg_uri)


try:
    gpt = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name='gpt-3.5-turbo')


    toolkit = SQLDatabaseToolkit(db=db, llm=gpt)
    agent_executor = create_sql_agent(
        llm=gpt,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )

    question = "total number of disclousers of with crd number 1000034 "
    agent_executor.run(question)

except Exception as e:
    print(e)