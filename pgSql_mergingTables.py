import psycopg2

# Database connection parameters
db_params = {
    'dbname': 'mydb',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

# SQL queries to create and populate the consolidated table
create_table_query = """
CREATE TABLE financial_advisor_profile AS
SELECT
    fa."CRD" AS crd_number,
    fa."First Name" AS first_name,
    fa."Middle Name" AS middle_name,
    fa."Last Name" AS last_name,
    fa."Email 1" AS email,
    fa."Phone" AS phone,
    fa."Address" AS address,
    fa."City" AS city,
    fa."State" AS state,
    fa."Zip" AS zip,
    fa."Broker-Dealer" AS broker_dealer,
    fa."RIA" AS ria,
    fa."Years of Experience" AS years_of_experience,
    fa."Current BD Start Date" AS current_bd_start_date,
    fa."Current RIA State Date" AS current_ria_start_date,
    fa."Title" AS title,
    fa."Gender" AS gender,
    bc."Exams Passed" AS exams_passed,
    bc."State Licenses" AS state_licenses,
    pec."examCategory" AS exam_category,
    pec."examName" AS exam_name,
    pec."examTakenDate" AS exam_taken_date,
    d."disclosureType" AS disclosure_type,
    d."disclosureResolution" AS disclosure_resolution,
    d."Allegations" AS allegations,
    d."Damage Amount Requested" AS damage_amount_requested,
    d."arbitrationDocketNumber" AS arbitration_docket_number,
    d."isIapdExcludedCCFlag" AS is_iapd_excluded_cc_flag,
    d."isBcExcludedCCFlag" AS is_bc_excluded_cc_flag
FROM public.financial_advisors_db fa
LEFT JOIN public.brokercheck_data bc ON fa."CRD" = bc."CRD Number"
LEFT JOIN public."principalExamCategory" pec ON fa."CRD" = pec.crd_number
LEFT JOIN public."Disclosures" d ON fa."CRD" = d.crd_number;
"""

# Function to run the SQL queries
def run_queries():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Execute the create table query
        cursor.execute(create_table_query)
        connection.commit()

        print("Consolidated table 'financial_advisor_profile' created successfully.")

    except Exception as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Run the function to execute the queries
run_queries()
