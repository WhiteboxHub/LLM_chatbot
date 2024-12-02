import sys
import os
# Add the parent directory (project folder) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from sqlalchemy import create_engine
from Scrape_brockercheck import main

from config import DATABASE_URI

#Load the CSV file

csv_file_path = 'AdvizorPro_Person_04.24.2024-1.csv'
df = pd.read_csv(csv_file_path)

#Display the first few rows of th dataframe to understand its structure
print(df.head())

#lowerCase
df.columns  = df.columns.str.lower()

#Setup prostgresSQL conection

engine = create_engine(DATABASE_URI)

#creat a table and load the csv data into postgresSQL
df.to_sql('financial_advisors_db',engine,if_exists="replace",index=False)

print('csv file inserted to the database.')

print(main())