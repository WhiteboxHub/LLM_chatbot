import requests
import pandas as pd
from sqlalchemy import create_engine
from config import DATABASE_URI
import json 


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
    
    for data in content['stateExamCategory']:
        uploadStateExamInfo(crdno,data)
    for data in content['principalExamCategory']:
        principalExamCategory(crdno,data)
    for data in content['productExamCategory']:
        productExamCategory(crdno,data)
    for data in content['registeredStates']:
        registeredStates(crdno,data)
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

    print()


#uploading the uploadStateExam data into uploadStateExam Table in pgsql

def uploadStateExamInfo(crdno,data):

    info= {
        'CRD':crdno,
        'examCategory':data['examCategory'],
        'examName':data['examName'],
        'examTakenDate':data['examTakenDate'],
        'examScope':data['examScope']
    }
    bc_stateexaminfo = pd.DataFrame([info])
    bc_stateexaminfo.to_sql('stateExamCategory', engine, if_exists='replace', index=False)


#uploading the principalExamCategory data into principalExamCategory Table in pgsql

def principalExamCategory(crdno,data):
    info= {
        'CRD':crdno,
        'examCategory':data['examCategory'],
        'examName':data['examName'],
        'examTakenDate':data['examTakenDate'],
        'examScope':data['examScope']
    }
    bc_principalExamCategory = pd.DataFrame([info])
    bc_principalExamCategory.to_sql('principalExamCategory', engine, if_exists='replace', index=False)

#uploading the productExamCategory data into productExamCategory Table in pgsql
def productExamCategory(crdno,data):
    info= {
        'CRD':crdno,
        'examCategory':data['examCategory'],
        'examName':data['examName'],
        'examTakenDate':data['examTakenDate'],
        'examScope':data['examScope']
    }
    bc_productexamcategory = pd.DataFrame([info])
    bc_productexamcategory.to_sql('productExamCategory', engine, if_exists='replace', index=False)



#uploading the registeredStates data into registeredStates Table in pgsql
def registeredStates(crdno,data):
    info = {'CRD':crdno,
        "state": data['state'],
                "regScope": data['regScope'],
                "status": data['status'],
                "regDate": data['regDate']}
    
    bc_registeredStates = pd.DataFrame([info])
    bc_registeredStates.to_sql('registeredStates', engine, if_exists='replace', index=False)

#uploading the scrape_brokercheck data into scrape_brokercheck Table in pgsql
def scrape_brokercheck(crd_number):
    url = f'https://api.brokercheck.finra.org/search/individual/{crd_number}'
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

# Setup PostgreSQL connection
engine = create_engine(DATABASE_URI)

# Load CRD Numbers from database
advisors_df = pd.read_sql('SELECT * FROM financial_advisors_db', engine)


# Check if 'CRD' is a valid column
if 'CRD' not in advisors_df.columns:
    raise ValueError("Column 'CRD' not found in DataFrame")

# Scrape data for each CRD Number
for crd in advisors_df['CRD']:
    brokercheck_data = scrape_brokercheck(crd)
    brokercheck_df = pd.DataFrame([brokercheck_data])
    brokercheck_df.to_sql('brokercheck_data', engine, if_exists='replace', index=False)

