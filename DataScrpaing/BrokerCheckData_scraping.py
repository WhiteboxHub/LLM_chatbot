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

#uploading the scrape_brokercheck data into scrape_brokercheck Table in pgsql
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
        

        cdata = Extract_infofrom_json(crd_number,data)
        return {
                'CRD Number': crd_number,
            'Disclosures': cdata.get('Disclosures'),
            'Exams Passed': cdata.get('Exams_Passed'),
            'State Licenses': cdata.get('State_Licenses')
        }
    else:
        return {
            'CRD Number': crd_number,
            'Disclosures': 'N/A',
            'Exams Passed': 'N/A',
            'State Licenses': 'N/A'
        }
    
#destructureing the Json data and using differnt fucntion to store the data into the pgsql
def Extract_infofrom_json(crdno,jsondata):
       # Parse the JSON data
    data = jsondata
    soures = data['hits']['hits'][0]['_source']
    content = json.loads(soures['content'])
    # Extract disclosures length
   
    disclosures_length = len(content['disclosures'])
   
    
    
    # Extract exams count and compute the sum
    exams_count = content['examsCount']
    total_exams_count = (exams_count['stateExamCount'] +
                         exams_count['principalExamCount'] +
                         exams_count['productExamCount'])
    
    # Extract registered states length
    registered_states_length = len(content['registeredStates'])
    print({
        'Disclosures': disclosures_length,
            'Exams_Passed': total_exams_count,
            'State_Licenses': registered_states_length
    })
    
    uploadStateLicenses(crdno,content['registeredStates'])
    # for data in content['stateExamCategory']:
    #     UploadStateExamInfo(crdno,data)
    # for data in content['principalExamCategory']: 
    #    UploadPrincipalExamInfo(crdno,data)
    # for data in content['productExamCategory']:
    #    UploadProductExamInfo(crdno,data)
        
    # if len(content['disclosures'])>0:
    #     print(len(content['disclosures']))
    #     for data in content['disclosures']:
    #         uploadDisclosures(crdno,data)

    return {
       'Disclosures': disclosures_length,
            'Exams_Passed': total_exams_count,
            'State_Licenses': registered_states_length
    }

#uploading the Disclosures data into Disclosures Table in pgsql
def uploadDisclosures(crdno,data):
    if data['disclosureType']=='Customer Dispute':
        info = {
        'CRD':crdno,
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
        bc_disclosures.to_sql('disclosures', engine, if_exists='replace', index=False)
    else:
        return

def UploadStateExamInfo(CRD,datajson):
    info= {
        'CRD':CRD,
        'examType':'State Exam',
        'examCategory':datajson['examCategory'],
        'examName':datajson['examName'],
        'examTakenDate':datajson['examTakenDate'],
        'examScope':datajson['examScope']
    }
    bc_principalExamCategory = pd.DataFrame([info])
    bc_principalExamCategory.to_sql('Financial_Advisor_Exams_Info', engine, if_exists='append', index=False)

    print("data Inserted Successfulley for CRD: ",CRD)

def uploadStateLicenses(CRD,datajson):
    engine = create_engine(database_url)

    metadata = MetaData()   
    json_data = json.dumps(datajson)

    
    registered_states = Table(
            'registered_states',metadata,
            Column('CRD',BigInteger,primary_key=True),
            Column("Registered_states_info",JSON)
    )

    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    insert_statement = registered_states.insert().values(CRD=CRD,Registered_states_info=json_data)

    session.execute(insert_statement)

    session.commit()

    session.close()

    print("data Inserted Successfulley for CRD: ",CRD)

def UploadProductExamInfo(CRD,datajson):

    info= {
        'CRD':CRD,
        'examType':'Product Exam',
        'examCategory':datajson['examCategory'],
        'examName':datajson['examName'],
        'examTakenDate':datajson['examTakenDate'],
        'examScope':datajson['examScope']
    }
    bc_principalExamCategory = pd.DataFrame([info])
    bc_principalExamCategory.to_sql('Financial_Advisor_Exams_Info', engine, if_exists='append', index=False)
    print("data Inserted Successfulley for CRD: ",CRD)

def UploadPrincipalExamInfo(CRD,datajson):
    engine = create_engine(database_url)

    info= {
        'CRD':CRD,
        'examType':'Principal Exam',
        'examCategory':datajson['examCategory'],
        'examName':datajson['examName'],
        'examTakenDate':datajson['examTakenDate'],
        'examScope':datajson['examScope']
    }
    bc_principalExamCategory = pd.DataFrame([info])
    bc_principalExamCategory.to_sql('Financial_Advisor_Exams_Info', engine, if_exists='append', index=False)
    print("data Inserted Successfulley for CRD: ",CRD)



# Load CRD Numbers from database
advisors_df = pd.read_sql('SELECT * FROM financial_advisors_db', engine)


# Check if 'CRD' is a valid column
if 'CRD' not in advisors_df.columns:
    raise ValueError("Column 'CRD' not found in DataFrame")


# Scrape data for each CRD Number
crdboolena = False
for crd in advisors_df['CRD']:
    if crdboolena:
        # print(crd)
        brokercheck_data = scrape_brokercheck(crd)
        brokercheck_df = pd.DataFrame([brokercheck_data])
        brokercheck_df.to_sql('brokercheck_data', engine, if_exists='replace', index=False)
    if crd ==1454077:
        crdboolena=True
    
    


