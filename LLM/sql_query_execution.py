import re
import re

def clean_sql_query(query: str) -> str:
    """
    Cleans the SQL query by removing extra text and ensuring it's valid SQL.
    
    Parameters:
        query (str): The SQL query to clean.
    
    Returns:
        str: The cleaned SQL query.
    """
    # Example: Remove any text outside the SQL query
    # If the query contains "Final answer: <<QUERY>>", extract the part within "<< >>"
    match = re.search(r"Final answer:\s*<<(.+?)>>", query, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Remove comments or unwanted prefixes (e.g., system messages)
    query = re.sub(r"--.*?$", "", query, flags=re.MULTILINE)  # Remove comments
    query = query.strip()  # Remove leading/trailing spaces
    
    return query


def execute_sql_query(db, query):
    """
    Executes a validated SQL query against the database.
    
    Parameters:
        db: The database agent instance (e.g., DB_AGENT).
        query: The SQL query to execute.
    
    Returns:
        The results of the query.
    """
    try:
        # Clean the query before execution
        cleaned_query = clean_sql_query(query)
        return db.run(cleaned_query)
    except Exception as e:
        raise RuntimeError(f"Error executing SQL query: {e}")
