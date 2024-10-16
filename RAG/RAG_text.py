from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os
import psycopg2
from sentence_transformers import SentenceTransformer,util
import csv
import numpy as np
dburl = os.getenv('DATABASE_URL')

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

que = "an advisor with CRD: 1300032, NPN: nan,"

embeding= model.encode(que).astype(np.float32)
emb_query = embeding.tolist()

conn = psycopg2.connect(
    database="LLM_vectordb",
    user="postgres",
    password="password",
    host="localhost",
    port = 5432
)

cursor = conn.cursor()

cursor.execute("SELECT embedding from advisors")
res = cursor.fetchall()
embeddings = np.array([np.fromstring(row[0][1:-1], sep=',', dtype=np.float32) for row in res])
# Compute cosine similarities
cosine_scores = util.pytorch_cos_sim(np.array(emb_query,dtype=np.float32), embeddings)

top_embedding = cosine_scores.numpy().flatten().tolist()

# Convert the embedding list to a string format for PostgreSQL
top_embedding_str = "[" + ",".join(map(str, top_embedding)) + "]"
top_n = 384
top_indices = np.argsort(cosine_scores.numpy().flatten())[-top_n:][::-1]

# Retrieve and display the corresponding results from the database
cursor.execute(f"SELECT * FROM advisors ORDER BY embedding <-> '{top_embedding_str}' LIMIT 4")

# cursor.execute("SELECT * FROM advisors LIMIT 1 OFFSET %s", (index,))
result = cursor.fetchone()
with open('test.csv',mode='w') as file:
    csvfile = csv.writer(file)
    # csvfile.writerow(cosine_scores)
    # csvfile.writerow(cosine_scores.numpy().flatten().tolist())
    for lines in result:
        csvfile.writerow(lines)
print(result)

# cursor.execute(f"SELECT * FROM advisors ORDER BY embedding <-> '{[[cosine_scores.numpy().flatten().tolist()]]}' LIMIT 4")

# # result = cursor.fetchall()
# top_embedding = cosine_scores.numpy().flatten().tolist()

# # Convert the embedding list to a string format for PostgreSQL
# top_embedding_str = "[" + ",".join(map(str, top_embedding)) + "]"

# # Use a parameterized query with explicit type casting
# cursor.execute("SELECT * FROM advisors ORDER BY embedding <-> %s::vector LIMIT 4", (top_embedding_str,))

# # Fetch the results
# result = cursor.fetchall()



# with open('test.csv',mode='w') as file:
#     csvfile = csv.writer(file)
#     # csvfile.writerow(cosine_scores)
#     # csvfile.writerow(cosine_scores.numpy().flatten().tolist())
#     for lines in result:
#         csvfile.writerow(lines)

    # for lines in result1:
    #     csvfile.writerow(lines)
    

print('done with execution')