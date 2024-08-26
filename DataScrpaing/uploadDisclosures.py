import requests
import pandas as pd
from sqlalchemy import create_engine,Table, Column,Integer,BigInteger,JSON,MetaData
from sqlalchemy.orm import sessionmaker
# from config import DATABASE_URI
import json 
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()
database_url = os.getenv('DATABASE_URI')
engine = create_engine(database_url)

metadata = MetaData()


def scrape_brokercheck(crd_number):
    url = f'https://api.brokercheck.finra.org/search/individual/{crd_number}?hl=true&includePrevious=true&nrows=12&query=john&r=25&sort=bc_lastname_sort+asc,bc_firstname_sort+asc,bc_middlename_sort+asc,score+desc&wt=json'
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for CRD Number {crd_number}: {e}")
        return {
            'CRD Number': crd_number,
            'Disclosures': 'Error',
            'Exams Passed': 'Error',
            'State Licenses': 'Error'
        }

    data = response.json()

    if 'hits' in data and data['hits']['total'] > 0:

        Extract_infofrom_json(crd_number,data)
        
    else:
        
        return

#destructureing the Json data and using differnt fucntion to store the data into the pgsql
def Extract_infofrom_json(crdno,jsondata):
       # Parse the JSON data
    data = jsondata
    soures = data['hits']['hits'][0]['_source']
    content = json.loads(soures['content'])
    # Extract disclosures length
    for data in content['disclosures']:
        uploadDisclosure(crdno,data)
   
    
   
def uploadDisclosure(CRD,data):
    if data['disclosureType']=='Customer Dispute':
        info = {
        'CRD':CRD,
        'eventDate':data['eventDate'],
        'disclosureType':data['disclosureType'],
        'disclosureResolution':data['disclosureResolution'],
        'isIapdExcludedCCFlag':data['isIapdExcludedCCFlag'],
        'isBcExcludedCCFlag':data['isBcExcludedCCFlag'],
        'bcCtgryType':data['bcCtgryType'],
        'iaCtgryType':data['iaCtgryType'],
        'Allegations':data['disclosureDetail']['Allegations'],
        'Damage Amount Requested':data['disclosureDetail']['Damage Amount Requested'],
        'DisplayAAOLinkIfExists':data['disclosureDetail']['DisplayAAOLinkIfExists'],
        'arbitrationClaimFiledDetail':data['disclosureDetail']['arbitrationClaimFiledDetail'],
        'arbitrationDocketNumber':data['disclosureDetail']['arbitrationDocketNumber'],
        }

        bc_disclosures = pd.DataFrame([info])
        bc_disclosures.to_sql('disclosures', engine, if_exists='append', index=False)
    else:
        return  
    
    


# Load CRD Numbers from database
advisors_df = pd.read_sql('SELECT * FROM financial_advisors_db', engine)


# Check if 'CRD' is a valid column
if 'CRD' not in advisors_df.columns:
    raise ValueError("Column 'CRD' not found in DataFrame")

# Scrape data for each CRD Number
for crd in advisors_df['CRD']:
    print(crd)
    brokercheck_data = scrape_brokercheck(crd)
    brokercheck_df = pd.DataFrame([brokercheck_data])
    brokercheck_df.to_sql('brokercheck_data', engine, if_exists='replace', index=False)

