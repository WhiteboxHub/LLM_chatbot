import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv
from groq import Groq
from langchain_community.utilities import SQLDatabase
import psycopg2
load_dotenv()
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
            You are provided with the following database metadata:
    {tables} Based on this schema, give me a  SQL query to retrieve data for the following Question: {question}
    
    """
    return llmprompt



def LLM_model_using_metadata(question):
    gorq_apikey = os.getenv('GROQ_API_KEY')
        
    client = Groq(
        api_key=gorq_apikey,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt(question),
            }
        ],
        model="llama3-8b-8192",
    )
    ans = chat_completion.choices[0].message.content
    print(ans)

    return ans


def SqlConnection(question):

    db_connection = {
        'dbname':'LLM_Finetune2',
        'user':'postgres',
        'password':'password',
        'host':'localhost',
        'port':'5432'

    }


    connection = psycopg2.connect(**db_connection)

    cursor  = connection.cursor()
    query = ''
    ans =  LLM_model_using_metadata(question)
        
    print(query)
    # print(LLM_model_using_metadata(question))
    cursor.execute(f"""{query}""")
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    
    cursor.close()
    connection.close()
    # pgurl = os.getenv('DATABASE_URI')

    # db = SQLDatabase.from_uri(pgurl)

    # qurey = LLM_model_using_metadata(question)

    # with db._engine.connect() as connection:
            
    #     results = connection.execute(qurey)
    #     rows = results.fetchall()
    
    # for row in rows:
    #     print(row)


SqlConnection('give me some names')