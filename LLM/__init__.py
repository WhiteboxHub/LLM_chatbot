from .DB_Connection import DB_connection_AGENT
from langchain_groq import ChatGroq
from .sql_generation_agent import create_sql_generation_agent
import os
from .sql_query_validation import create_sql_validataion_agent
from .sql_query_execution import execute_sql_query

__all__ = ['DB_connection_AGENT','create_sql_generation_agent']

def main(question, count=0):
    # Set up environment variables
    key = "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"
    os.environ["GROQ_API_KEY"] = key
    
    # Initialize LLM and Database agent
    llm = ChatGroq(model="llama3-8b-8192")

    db, db_info = DB_connection_AGENT()

    # Create agents
    sql_generation_agent = create_sql_generation_agent(llm, db)
    sql_query_validation = create_sql_validataion_agent(llm, db, sql_generation_agent)

    # Construct the query prompt
    prompt_query = f"""
                            {question} give a query for the question using the following db information {db_info} .
                            just reproduce the query with no further commentary.
                            
                            if the question is generic that is not asking about the advisors generate a query to return the table names.

                    """

    try:
        # Generate SQL query
        generate_query = sql_generation_agent.invoke({"question": prompt_query})
        print(f"Generated Query:\n{generate_query}")

        # Add question context to the query for validation
        generate_query_with_question = f"{generate_query} and the question is : {question} "

        # Validate the query
        validated_query = sql_query_validation.invoke({"query": generate_query_with_question})
        print(f"Validated Query:\n{validated_query}")

        # Execute the validated query
        results = execute_sql_query(db, validated_query)
        print(f"Query Results:\n{results}")
        return results, validated_query
    
    except Exception as e:
        print(f"Error occurred: {e}")
        if count < 10:
            print(f"Retrying... Attempt {count + 1}")
            return main(question, count=count + 1)
        else:
            return f"Error occurred while generating or executing the query for the given question: {question}", f"Query generated and validated: {validated_query}"

# Uncomment if you want to run it directly
# if __name__ == "__main__":
#     main("Give me the names of people who have registered in more than 20 states?")
