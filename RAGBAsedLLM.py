from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine,text

load_dotenv()
pg_uri = os.getenv('DATABASE_URI')

# Initialize the SQL database connection
db = SQLDatabase.from_uri(pg_uri)
def retrieve_documents(question):
    engine = db._engine
    # Function to retrieve relevant rows based on the question
    # Use a more specific or advanced query to handle large datasets
    
    # Example query, you might need to adjust it based on your schema
    # Assuming 'description' is a relevant column for the search
    
    with engine.connect() as connection:
        print('Qurey called')
        query = text("""SELECT * FROM financial_advisor_data WHERE CONCAT_WS(' ', "CRD", "Phone", "First Name", "Middle Name", "Last Name", "Gender", "Personal Email", "Address", "City", "State", "Zip", "Designations", "Person Tag - Investments", "Person Tag - Expertise", "Person Tag - Role", "Team", "Team ID", "Notes", "Carrier", "Company", "Total Disclosures", "Total Exams Passed", "Total State Licenses", "Disclosure-eventDate", "Disclosure-type","Disclosure-Resolution", "Disclosure-Allegations", "Disclosure-Damage Amount Requested", "Initial Appointment Date", "Insurance Years of Experience", "Previous Broker Dealer", "Previous RIA", "Person Tag - Family", "Person Tag - Hobbies", "Person Tag - Services", "Person Tag - Sports Teams", "Person Tag - School", "Person Tag - Military Status", "Person Tag - Faith Based Investing") LIKE :question LIMIT 100""")
        result = connection.execute(query,{'question':f'%{question}%'})
        rows = result.fetchall()
        print(rows)
    return rows


def format_results(results):
    # Function to format the retrieved rows into a string
    # Adjust this function based on how you want to present the data
    formatted_results = []
    for row in results:
        formatted_row = ", ".join([f"{col}: {row[col]}" for col in row.keys()])
        formatted_results.append(formatted_row)
    
    return "\n".join(formatted_results)

def LLM_model_RAG(question):
    try:
        print("Function initiated")
        
        # Step 1: Retrieve relevant documents
        documents = retrieve_documents(question)
        print("Documents retrieved")
        
        # Step 2: Format the results
        context = format_results(documents)
        print("Results formatted")
        
        # Initialize the ChatGroq model
        llm = ChatGroq(
            model="llama3-8b-8192",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=os.getenv('GROQ_API_KEY')
        )
        print("Groq LLM initialized")

        # Combine retrieved documents with the question
        augmented_question = f"Context: {context}\nQuestion: {question}"
        
        # Use the LLM to generate a response based on the augmented question
        response = llm.generate(augmented_question)
        print("Response generated")
        return response
    
    except Exception as e:
        print(e)
        return None


LLM_model_RAG("Stephen Wendell")