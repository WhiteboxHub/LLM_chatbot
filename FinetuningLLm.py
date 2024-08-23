from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit 
import xml.etree.ElementTree as ET
import os
from groq import Groq
import getpass
# Load environment variables (for database URI)
load_dotenv()
pg_uri = os.getenv('DATABASE_URI')


GorqApiKey = os.getenv('GROQ_API_KEY')
# os.environ['GROQ_API_KEY'] = getpass.getpass('Enter your Groq API key:')
# Initialize the SQL database connection
db = SQLDatabase.from_uri(pg_uri)



def FineTuned_LLM_model_Groq(question):
    try:
        print("function insitated")
        # Initialize the ChatGroq model (no API key required)
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv('GROQ_API_KEY')
            
        )
        # groqLLMModel = Groq(api_key=os.getenv('GROQ_API_KEY'))



        # Create the SQL agent using the ChatGroq LLM
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            handle_parsing_errors=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

        questionpromt = LLM_queryModel(question)
        print('Query returned')
        result = agent_executor.invoke(f'query the following and return a well structured answer{questionpromt}')
        print(result)
        return result
    except Exception as e:
        print(e)
        return None

def LLM_queryModel(quetion):
    print('qury modle initated')
    client = Groq(
    api_key=os.environ.get("GorqApiKey"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt(quetion),
            }
        ],
        model="llama-3.1-8b-instant",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content


def prompt(question):
    with open('database_metadata.xml','r') as file:
        xml_data = file.read()
    root = ET.fromstring(xml_data)

    tables = {}

    # Iterate over each table
    for table in root.findall('table'):
        # Extract table name and description
        table_name = table.attrib.get('name', 'Unknown')
        table_description = table.find('description').text if table.find('description') is not None else 'No description available'

        # Extract column information
        columns = []
        for column in table.findall('column'):
            column_name = column.attrib.get('name', 'Unnamed')
            column_type = column.attrib.get('type', 'Unknown')
            column_description = column.find('description').text if column.find('description') is not None else 'No description available'
            columns.append({
                'name': column_name,
                'type': column_type,
                'description': column_description
            })
        totalinfo = {"tableName":table_name,"Description":table_description,"coloums":columns}
        tables[table_name] = totalinfo

    llmprompt = f"""
            You are provided with the following database metadata for the db:
    {tables} Based on this give sql query for the following Question : {question}
    
    """
    return llmprompt