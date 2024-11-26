
from langchain_community.utilities import SQLDatabase
import sys
import os

# Add the parent directory (project folder) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DATABASE_URI





def DB_connection_AGENT():
    db = SQLDatabase.from_uri(DATABASE_URI)
    tables = db.get_usable_table_names()

    db_info = db.run("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, column_name;
            """)
    return db,db_info

