﻿# **BrokerCheck Data Scraper and Query Agent**

This project provides a comprehensive solution for scraping broker information from the FINRA BrokerCheck website, storing it in a PostgreSQL database, and enabling advanced query capabilities using a text-to-SQL agent. The system includes a feedback loop for iterative query refinement, a validation and execution workflow, and a user-friendly interface built with Streamlit.

---

## **Streamlit UI**

![Streamlit UI](https://github.com/WhiteboxHub/LLM_chatbot/blob/c34621f4567bc6f573ad73aba0c9afffcadd8ffd/Images/UI.png)

## **Streamlit UI with user query and response**

![Streamlit UI](https://github.com/WhiteboxHub/LLM_chatbot/blob/c34621f4567bc6f573ad73aba0c9afffcadd8ffd/Images/image.png)


## **Features**
1. **API Scraping**:
   - Scrapes broker data from the BrokerCheck platform.
   - Uses a CSV file as a starting point to define scraping parameters.

2. **Data Storage**:
   - Stores scraped data in a PostgreSQL database for secure and efficient management.

3. **Query Agents**:
   - **Text-SQL Agent**: Converts natural language queries into SQL.
   - **Validation Agent**: Ensures the SQL query generated is syntactically correct and valid.
   - **Execution Agent**: Executes the validated SQL query against the database.

4. **Feedback Loop**:
   - Allows users to refine queries and responses iteratively for improved results.

5. **Streamlit Interface**:
   - A dynamic web-based user interface for interacting with the data, querying the database, and visualizing results.

---

# **Prerequisites**
    - Python version 3.10.5
    - PostgreSQL installed and running in Docker container 
    - Streamlit for the web interface

# **Getting Started with Docker and PostgreSQL Setup**

Follow these steps to set up Docker and PostgreSQL in your local environment.

## **Step 1: Download and Install Docker**
1. **Download Docker**:
   - Go to the Docker official website: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Choose the appropriate version based on your operating system:
     - **Windows**: [Download for Windows](https://www.docker.com/products/docker-desktop/)
     - **Mac**: [Download for Mac](https://www.docker.com/products/docker-desktop/)

2. **Install Docker**:
   - Follow the on-screen instructions for your OS to install Docker Desktop.

---

## **Step 2: Set Up PostgreSQL using Docker**
1. **Watch the YouTube Video**:
   - Follow the instructions in this [YouTube video](https://youtu.be/DvURiNIvhxA?si=q_Cva1bPTvA_ByjZ) to set up PostgreSQL using Docker.
   - The video provides a step-by-step guide on running PostgreSQL in a Docker container.

2. **Follow Colab Instructions for Docker Commands**:
   - As you follow the video, refer to the [Colab notebook](https://colab.research.google.com/drive/1zh93oUlFV6KR3VNE7Mcm23G13G6oLGj8?usp=sharing) for the necessary Docker commands.
   - The Colab contains the setup commands that are relevant for PostgreSQL installation using Docker.
---

## **Step 3: Install Python Dependencies**
Once Docker and PostgreSQL are set up, install the necessary Python packages:

1. **For Mac Users**:
   - Open a terminal and run the following command to install the required packages from the `requirements.txt` file:
     ```bash
     pip3 install -r requirements.txt
     ```

2. **For Windows Users**:
   - Open Command Prompt or PowerShell and run the following command to install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

---


# **.env File Structure**

The `.env` file contains important environment variables for your application. This file should be placed in the root of your project directory and not be committed to version control (e.g., GitHub) to protect sensitive information such as API keys and database credentials.

## **Environment Variables**

Below is the structure of the `.env` file:
```
.env

# Your OpenAI API key to connect to OpenAI services
OPENAI_API_KEY='YourOpenaikey'

# Your RapidAPI LinkedIn key for accessing LinkedIn data via RapidAPI
RAPIDAPI_LINKEDIN_KEY = 'your Rapid api linkedin key'

# The URI for connecting to your PostgreSQL database (replace with your credentials)
DATABASE_URI = "DB URL"

# Your Groq API key for accessing Groq-related services
GROQ_key = "GROQ key" 
```
[Get your Groq API Key](https://console.groq.com/keys)

## **Folder Structure**



```plaintext
.
├── DataLodation/
│   ├── CSV_data_loading.py           # Script to load data from CSV files into the database
├── LLM/
│       ├── __init__.py               # Module initializer
│       ├── DB_connection.py          # Database connection logic for the LLM module
│       ├── sql_generation_agent.py   # Text-to-SQL generation agent
│       ├── sql_query_execution.py    # Executes SQL queries on the database
│       ├── sql_query_validation.py   # Validates the generated SQL queries
├── Scrape_brockercheck/
│       ├── __init__.py               # Module initializer
│       ├── DB_connection.py          # Database connection logic for scraping module
│       ├── Extract_json_info.py      # Extracts information from JSON responses
│       ├── make_request.py           # Handles HTTP requests to the BrokerCheck API
│       ├── Upload_disclosures.py     # Uploads broker disclosure data to the database
│       ├── Upload_exams.py           # Uploads exam-related data to the database
│       ├── Upload_reg_states.py      # Uploads state registration data to the database
│   ├── AdvizorPro_Person_04.24.2024-1.csv  # Sample CSV file for initial data input
├── config.py                         # Configuration settings for the project
├── Groq_llm.py                       # Main script to integrate LLM with the project
├── Streamlit_Groq.py                 # Streamlit-based user interface for query interaction
├── requirements.txt                  # Python dependencies


```

# Data Extraction Guide

## Step 1: Update the Database URL

Before running the scripts for data extraction, you need to update the database connection URL (`DATABASE_URI`) to connect to the correct PostgreSQL instance.

1. Open the `.env` file located in your project root directory.
2. Update the `DATABASE_URI` field with the correct connection details:

```env
DATABASE_URI = "postgresql+psycopg2://<username>:<password>@<host>:<port>/<dbname>"
```

## Step 2: Run the CSV Data Loading Script

After updating the `DATABASE_URI` in the `.env` file, the next step is to load data from the CSV file into your PostgreSQL database.



## 1. we start with csv data uploading.

Open a terminal or command prompt in your project’s root directory.

```bash
python /DataLoading/CSV_data_loading.py      #for Windows user
python3 /DataLoading/CSV_data_loading.py      #for Mac users
```

## 2. we Scrape the data from Brokercheck and upload into DB.
```bash
python /DataLoading/Scrape_data.py      #for Windows user
python3 /DataLoading/Scrape_data.py      #for Mac users
```

## 3. we run the Streamlit application.
```bash
streamlit run Streamlit_Groq.py    
```
