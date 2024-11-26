from langchain.chains import create_sql_query_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
def create_sql_generation_agent(llm, db):
    
    # prompt = """You are a  expert. Given an input question, create a syntactically correct  query to run.
    # Unless the user specifies in the question a specific number of examples to obtain, query for most  results using the LIMIT clause as per .
    # Never query for all columns from a table. You must query only the columns needed to answer the question.

    # question: {question}
    # db_info: {databaseinfo}
    # """
    # prompt_templet = ChatPromptTemplate.from_template(prompt)
    llms = create_sql_query_chain(llm,db )
    # chain_templete = (
    #         prompt_templet  
    #         | llms
            
    # )
    

    return llms
