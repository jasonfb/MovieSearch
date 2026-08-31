

import sys
import psycopg2

from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

# setup database connection
conn = psycopg2.connect(
    host="localhost",
    database="moviesearch", 
    port="5432"
)

# register the vector on the database connection
register_vector(conn) 
cursor = conn.cursor()


# load the transformer model we will use for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


query = """
SELECT id, title, plot,
embedding <=> %s as distance
FROM movies 
ORDER BY distance
LIMIT 5
"""

if len(sys.argv) > 1:
    search_string = sys.argv[1]
    encoded_string = model.encode(search_string)
    cursor.execute(query, (encoded_string,))

    results = cursor.fetchall()
    for row in results:
        print(row[1])

else:
    print("No argument provided.")
