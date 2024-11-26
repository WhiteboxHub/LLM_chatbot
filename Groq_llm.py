import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from LLM import main  # Assuming you have a main function that retrieves context and query
from config import GROQ_key
def Groq_LLM(question):
    # Get the context and query from your 'main' function
    context, query = main(question)
    
    
    # Define the prompt for the LLM
    print("GRO_Started")
    
    try:
        prompt = f"""
            You are an assistant that take out the information form the context and create a well structrued paragraph answers along with the given question

            <Question>: {question}  </Question>
            <Query>: {query} </Query>
            <Context>: {context[0:2500]} </Context>
            If the question is not about the information in the database, you should reply "I don't know. iam assistant with 
            financial advisors knowledge please ask related questions."
            Please check the question, query, and context before providing an answer.
            You are not allowed to give any answer that is beyond the context.

            If the question is beyond the context, you should say, 
            "I am an assistant with financial advisors data, please ask related questions."

            if you find the answer for the question use the following structure to show the answer:
                'the given question is : question'\n
                'the answer is : answer'
            """

        # Set the API key for Groq
        api_key =  GROQ_key  # Replace with your actual Groq API key
        os.environ["GROQ_API_KEY"] = api_key  # Set the environment variable for the API key
        print("line 35")
        # Define the ChatGroq instance using the llama3 model
        llm = ChatGroq(model="llama3-8b-8192", streaming=True)

        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_template(prompt)
        print("line 41")

        # Define the context chain using Groq
        context_chain = prompt_template | llm

        # Invoke the chain and get the response
        response = context_chain.invoke({"question": question})
        print("line 48")
        print(response.content)
        return response
        # If the response is not of type AIMessage, convert to string

    except Exception as e:
        print(f"Error occurred: {e} while constructing the answer")
        return e
