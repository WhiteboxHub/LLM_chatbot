from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, text,Table, MetaData, select, func, Column, String, Text
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
import os

load_dotenv()


# Load the pre-trained SentenceTransformer model

db_url = os.getenv('DATABASE_URI')



def connect_to_db():
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Test the connection
    try:
        engine.connect()
        print("Database connection successful.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
    
    return engine, session


def similarity(session,question):
    relevant_data = {
        'advisories': [],
        'broker_data': []
    }
    try:
        advisor_query = text("""
                        SELECT *
                        FROM advisors
                        WHERE to_tsvector('english', advisory_text) @@ to_tsquery('english', :query)
                        ORDER BY ts_rank(to_tsvector('english', advisory_text), to_tsquery('english', :query)) DESC
                        LIMIT 5;
                        """)
        brokercheck_query = text("""
                            SELECT *
                            FROM brokercheck_data
                            WHERE to_tsvector('english', advisory_text) @@ to_tsquery('english', :query)
                            ORDER BY ts_rank(to_tsvector('english', advisory_text), to_tsquery('english', :query)) DESC
                            LIMIT 5;
                            """)
        combined_query = text("""
            SELECT 'advisors' AS source, id, advisory_text
            FROM advisors
            WHERE to_tsvector('english', advisory_text) @@ to_tsquery('english', :query)
            ORDER BY ts_rank(to_tsvector('english', advisory_text), to_tsquery('english', :query)) DESC
            LIMIT 5

            UNION ALL

            SELECT 'brokercheck_data' AS source, id, advisory_text
            FROM brokercheck_data
            WHERE to_tsvector('english', advisory_text) @@ to_tsquery('english', :query)
            ORDER BY ts_rank(to_tsvector('english', advisory_text), to_tsquery('english', :query)) DESC
            LIMIT 5;
        """)

        results = session.execute(advisor_query, {'query': question}).fetchall()
        # Populate relevant_data based on the source of the results
        for row in results:
            if row.source == 'advisors':
                relevant_data['advisories'].append({
                    'id': row.id,
                    'advisory_text': row.advisory_text
                })
            elif row.source == 'brokercheck_data':
                relevant_data['broker_data'].append({
                    'id': row.id,
                    'advisory_text': row.advisory_text
                })
        print(f"Combined Results: {relevant_data}")
    except Exception as e:
        print(f"Error fetching relevant data: {e}")

question = "give me the information on crd 1000034"

e,s = connect_to_db()
similarity(s,question)
# # Define the base for the ORM models
# Base = declarative_base()

# # Advisory table model
# class Advisory(Base):
#     __tablename__ = 'advisors'
#     id = Column(String(50), primary_key=True)  # Primary key
#     advisory_text = Column(Text)
#     embedding = Column(Vector(384))  # Using pgvector with 384 dimensions


# class BrokerData(Base):
#     __tablename__ = 'brokercheck_data'
#     id =  Column(String(50), primary_key=True)  # Primary key with text ID
#     advisory_text = Column(Text)
#     embedding = Column(Vector(384))
# model = SentenceTransformer('all-MiniLM-L6-v2')


# # Create an engine and connect to the database
# engine = create_engine(db_url)
# Session = sessionmaker(bind=engine)
# session = Session()

# # Create tables if they do not exist (optional)
# Base.metadata.create_all(engine)
# def similarity_search(question):


#     #   Step 1: Generate the embedding for the input question
#     query_embedding = model.encode(question).tolist()

#     query_embedding_tuple = tuple(query_embedding)
#     # Step 2: Query the Advisory table for cosine similarity
#     advisory_query = (
#         select([Advisory.id, Advisory.advisory_text, func.pgv_cosine(Advisory.embedding, query_embedding_tuple).label("similarity")])
#         .order_by("similarity")
#         .limit(5)
#     )

#     # Step 3: Query the BrokerData table for cosine similarity
#     brokercheck_query = (
#         select([BrokerData.id, BrokerData.advisory_text, func.pgv_cosine(BrokerData.embedding, query_embedding_tuplezzzzz).label("similarity")])
#         .order_by("similarity")
#         .limit(5)
#     )

#     # Step 4: Execute both queries
#     advisory_results = session.execute(advisory_query).fetchall()
#     brokercheck_results = session.execute(brokercheck_query).fetchall()

#     # Combine the results and sort by similarity
#     combined_results = sorted(advisory_results + brokercheck_results, key=lambda x: x.similarity)[:5]

#     # Print the results
#     print("Similarity Search Results:")
#     for result in combined_results:
#         doc_id, advisory_text, similarity = result
#         print(f"ID: {doc_id}, Similarity: {similarity:.4f}, Advisory: {advisory_text[:100]}")

# # Example question
# question = "give me the information on crd 1000034"

# # Perform similarity search
# similarity_search(question)

# # Close the session
# session.close()