import requests
import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URI,RAPIDAPI_KEY
import json 
import http.client
from urllib.parse import quote
import os
from dotenv import load_dotenv

load_dotenv()
def ExtractLinkedinData(crdno,linkedinurl):
    print(linkedinurl)
    lurl = quote(linkedinurl, safe='')
    conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com")
    print(lurl)
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_LINKEDIN_KEY'),
        'x-rapidapi-host': "linkedin-data-api.p.rapidapi.com"
    }

    conn.request("GET", f"/get-profile-data-by-url?url={lurl}", headers=headers)

    res = conn.getresponse()
    data = res.read()
    decoded = data.decode("utf-8")
    print(data.decode("utf-8"))
    print('fetching the user with url ', linkedinurl)
   
    return 






# Setup PostgreSQL connection
engine = create_engine(DATABASE_URI)

# Load CRD Numbers from database
advisors_df = pd.read_sql('SELECT * FROM financial_advisors_db', engine)

crdno = [advisors_df['CRD']]
likedinurl = [advisors_df['LinkedIn']]
for index, row in advisors_df.iterrows():
    
    crd = row['CRD']
    url = row["LinkedIn"]
    
    if url:
        
        user_data = ExtractLinkedinData(crd,url)
        data = pd.DataFrame([user_data])
        data.to_sql('linkedin',engine, if_exists='replace', index=False)
    else:
        continue