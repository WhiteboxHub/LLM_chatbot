import pandas as pd
import json

def upload_states_data(CRD_NUMBER,JSONDATA,engine):
    data = JSONDATA

    source = data['hits']['hits'][0]['_source']

    content = json.loads(source['content'])

    for data in content['registeredStates']:
        info = {'crd':CRD_NUMBER,
                "state": data['state'],
                "regscope": data['regScope'],
                "status": data['status'],
                "regdate": data['regDate']}
        registeredStates = pd.DataFrame([info])
        registeredStates.to_sql('registeredstates', engine, if_exists='append', index=False)
    
    print(f"states data uplodeed for {CRD_NUMBER} sucessfully")
    return True