from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit 
import os
from groq import Groq
import getpass
# Load environment variables (for database URI)
load_dotenv()
pg_uri = os.getenv('DATABASE_URI')

# GorqApiKey = os.getenv('GROQ_API_KEY')
# os.environ['GROQ_API_KEY'] = getpass.getpass('Enter your Groq API key:')
# Initialize the SQL database connection
db = SQLDatabase.from_uri(pg_uri)



def LLM_model_Groq(question):
    try:
        print("function insitated")
        # Initialize the ChatGroq model (no API key required)
        llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv('GROQ_API_KEY')
            
        )
        # groqLLMModel = Groq(api_key=os.getenv('GROQ_API_KEY'))


        print("Groq llm done")

        # Create the SQL agent using the ChatGroq LLM
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            handle_parsing_errors=True,
            # agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        print("Agent executer llm done")


        result = agent_executor.invoke(f"based on DB connection provided give a precise answer with query Limit = 1 for the following question: {question}")
        print(result)
        return result
    except Exception as e:
        print(e)
        return None

# Example usage
# question = "How many different people live at the zip code 60606?"
# response = LLM_model(question)
# print(response)
