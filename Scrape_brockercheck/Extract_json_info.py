import json
import pandas as pd
def Extract_jsoninfo(CRD_NUMBER, JSONDATA,engine):

    data = JSONDATA

    source = data['hits']['hits'][0]['_source']

    content = json.loads(source['content'])

    disclosures_length = len(content['disclosures'])

    # Extract exams count and compute the sum
    exams_count = content['examsCount']
    total_exams_count = (exams_count['stateExamCount'] +
                         exams_count['principalExamCount'] +
                         exams_count['productExamCount'])
    
    # Extract registered states length
    registered_states_length = len(content['registeredStates'])
    info = {
        'crd':CRD_NUMBER,
        'disclosures': disclosures_length,
        'exams_passed': total_exams_count,
        'state_licenses': registered_states_length
    }

    new_data = pd.DataFrame([info])
    try:
        new_data.to_sql('brokercheck_data',engine,if_exists="append",index=False)
        return True,"Data successfully written to the table 'brokercheck_data'."
    except Exception as e:
        return False,f"An error occurred: {e} for uploading {CRD_NUMBER}'s brokercheck_data"
    


    