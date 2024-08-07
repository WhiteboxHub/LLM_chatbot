from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.sql_database import SQLDatabase

# Import SQLDatabaseChain from the correct module, if available
from langchain.chains import SQLDatabaseChain  # Assuming chains module

from config import DATABASE_URI

load_dotenv()

openai_apikey = 'vqaa1wPIUsjPTvOr1woP0zmFj_a_6838ClGY0shfJ6M'
dburl = DATABASE_URI

db = SQLDatabase.from_uri(dburl)
llm = OpenAI(api_key=openai_apikey, temperature=0)  # Ensure API key is passed correctly

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

result = db_chain.run('how many advisors are there in total?')
print(result)
