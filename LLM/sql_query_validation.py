from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def create_sql_validataion_agent(llm,db,question):
        
    system = """Double check the user's {dialect} query for common mistakes, including:
    - Using NOT IN with NULL values
    - Using UNION when UNION ALL should have been used
    - Using BETWEEN for exclusive ranges
    - Data type mismatch in predicates
    - Properly quoting identifiers
    - Using the correct number of arguments for functions
    - Casting to the correct data type
    - Using the proper columns for joins
    - Giving Excess data other than imformation requested in the question
    If there are any of the above mistakes, rewrite the query.
    If there are no mistakes, just reproduce the original query with no further commentary.

    Output the final SQL query only.
    
    """

    chain_prompt  = ChatPromptTemplate.from_messages(
                            [("system", system), ("human", "{query}")]
                            ).partial(dialect=db.dialect)
    # validation_chain = prompt | llm | StrOutputParser() 

    # full_chain = {"query": chain} | validation_chain

    return chain_prompt | llm | StrOutputParser()