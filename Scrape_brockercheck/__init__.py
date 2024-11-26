
from .DB_connection import DB_connection_engine
from .Extract_json_info import Extract_jsoninfo
from .make_request import Get_BrokerCheck_response
from .Upload_exams import exams_data
from .Upload_reg_states import upload_states_data
from .Upload_disclosures import Uplad_disclosures
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


__all__ = ['DB_connection_engine', 'Extract_jsoninfo','exams_data','Get_BrokerCheck_response','upload_states_data','Uplad_disclosures']

def Scrape_data(CRD_NUMBER, engine, delay=1):
    """
    Scrape data for a given CRD_NUMBER, with a delay to avoid 429 errors.

    Parameters:
        CRD_NUMBER: int
            The CRD number of the financial advisor.
        engine: SQLAlchemy Engine
            The database engine for storing data.
        delay: int, optional
            Delay in seconds between requests to avoid hitting rate limits. Default is 1 second.
    """
    try:
        response_Status, CRD, data = Get_BrokerCheck_response(CRD_NUMBER)

        if response_Status:
            json_status, response = Extract_jsoninfo(CRD, data, engine)
            print(response)
            exams_data(CRD, data, engine)
            upload_states_data(CRD, data, engine)
            Uplad_disclosures(CRD, data, engine)
        else:
            print(data)

    except Exception as e:
        print(f"Error processing CRD {CRD_NUMBER}: {e}")
    finally:
        # Introduce a delay to avoid 429 errors
        time.sleep(delay)

def main():
    engine = DB_connection_engine()
    advisors_df = pd.read_sql('SELECT * FROM financial_advisors_db', engine)

    # Create a thread pool
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks to the executor
        future_to_crd = {
            executor.submit(Scrape_data, crd, engine,delay = 2): crd
            for crd in advisors_df['crd']
        }
        
        # Process results as they complete
        for future in as_completed(future_to_crd):
            crd = future_to_crd[future]
            try:
                result = future.result()  # Get the result of the Scrape_data function
                print(f"CRD {crd} processed successfully.")
            except Exception as e:
                print(f"Error processing CRD {crd}: {e}")
    
    return "Data Scraping executed for all CRD_NUMBER"