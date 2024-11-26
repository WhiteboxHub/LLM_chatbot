import pandas as pd
import json


def Uplad_disclosures(CRD_NUMBER,JSONDATA,engine):
    data = JSONDATA

    source = data['hits']['hits'][0]['_source']

    content = json.loads(source['content'])

    for data in content['disclosures']:
        try:
            if data['disclosureType']=='Customer Dispute':
                amount = data['disclosureDetail'].get("Damage Amount Requested","$0")
                # Remove '$' and ',' then convert to float and then to int
                integer_value = int(float(amount.replace('$', '').replace(',', '')))
                info = {
                'crd':CRD_NUMBER,
                'eventdate':data['eventDate'],
                'disclosuretype':data['disclosureType'],
                'disclosureresolution':data['disclosureResolution'],
                'isiapdExcludedccflag':data['isIapdExcludedCCFlag'],
                'isbcexcludedccflag':data['isBcExcludedCCFlag'],
                'allegations':data['disclosureDetail']['Allegations'],
                'damageamountrequested':integer_value,
                'displaylink':data['disclosureDetail']['DisplayAAOLinkIfExists'],
                }

                bc_disclosures = pd.DataFrame([info])
                bc_disclosures.to_sql('disclosures', engine, if_exists='append', index=False)
            else:
                continue
        except Exception as e:
            print(f"expection occure while uploading disclosures {e}")
  
    
    