
import requests


def Get_BrokerCheck_response(CRD_NUMBER):
    url = f'https://api.brokercheck.finra.org/search/individual/{CRD_NUMBER}'
    try:
        response = requests.get(url, timeout=10) 
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for CRD Number {CRD_NUMBER}: {e}")
        return False,CRD_NUMBER,{
            'CRD Number': CRD_NUMBER,
            'Disclosures': 'Error',
            'Exams Passed': 'Error',
            'State Licenses': 'Error'
        }

    data = response.json()

    if 'hits' in data and data['hits']['total'] > 0:
        return True,CRD_NUMBER,data
    else:
        return False,CRD_NUMBER,{
            'CRD Number': CRD_NUMBER,
            'Disclosures': 'N/A',
            'Exams Passed': 'N/A',
            'State Licenses': 'N/A'
        }