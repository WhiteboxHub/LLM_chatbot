from sqlalchemy import create_engine


def DB_connection_engine():
    DATABASE_URI = "postgresql+psycopg2://postgres:password@localhost:5432/LLM_assistant"

    engine = create_engine(DATABASE_URI)

    return engine