# LLM_chatbot
# LLM_chatbot


This is a LLM chatbot using openai that answers question by checking into the database provided.

# config.py
the file shows the structure of the .env file required for this project

# load_data.py

This file contains the code to post the AdvizorPro_Person_.csv file's data into postgres SQL DB

# scrape_brokercheck.py

This file Extracts the data from brockercheck.com websites api by using the crd number extracts the data and stores it in differnt table. the crd number is stored in PGSQL DB from the previous step

# LLm_1.py
This file contains code that uses OpenAI key to leverages LLM chatbot to connect with our database to answer the question asked

# LLm_2.py
This file contains code that uses Grop cloud opensource LLM chatbot to connect with our database to answer the question asked

# stremlit.py
This file contains the code to run the streamlit application leveraging LLm chatbot created by importing the LLM_model function From Llm1.py file 

# Streamlib_Groq.py
This file contains the code to run the streamlit application leveraging LLm chatbot created by importing the LLM_model function From Llm1.py file 

how to run the file
# stremlit run Stremlit.py