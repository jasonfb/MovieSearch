import pandas as pd
import psycopg2
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

df = pd.read_csv("data/wiki_movie_plots_deduped.csv")
print(df.shape)
print(df.columns)

model = SentenceTransformer("all-MiniLM-L6-v2")



conn = psycopg2.connect(
    host="localhost",
    database="moviesearch", 
   
    port="5432"
)
register_vector(conn) 

cur = conn.cursor()

insert_query = """
INSERT INTO movies (title, plot, embedding) 
VALUES (%s, %s, %s);
"""

embeddings = model.encode(df["Plot"].tolist())

print(embeddings.shape)


try:
        for i, row in enumerate(df.itertuples(index=False)):
              cur.execute(insert_query, (row.Title, 
                                         row.Plot, 
                                         embeddings[i]))

        conn.commit()
        print(f"successfully inserted {len(df)} movies")

except Exception as e:
    conn.rollback()
    print(f"An error occurred: {e}")

finally:
    # 7. Clean up and close connections
    cur.close()
    conn.close()