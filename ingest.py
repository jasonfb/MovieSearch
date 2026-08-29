import pandas as pd
import psycopg2
from sentence_transformers import SentenceTransformer
from pgvector.psycopg2 import register_vector

# read the CSV into a dataframe with pandas
df = pd.read_csv("data/wiki_movie_plots_deduped.csv")
print(df.shape)
print(df.columns)

# load the transformer model we will use for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# encode the plot text into the embeddings
embeddings = model.encode(df["Plot"].tolist())

# setup database connection
conn = psycopg2.connect(
    host="localhost",
    database="moviesearch", 
    port="5432"
)

# register the vector on the database connection
register_vector(conn) 
cur = conn.cursor()

# reusable query for inserting values into database
insert_query = """
INSERT INTO movies (title, plot, embedding) 
VALUES (%s, %s, %s);
"""

try:    
        # loop through the rows and join the data to the embeddings, inserting rows as we go
        for i, row in enumerate(df.itertuples(index=False)):
              cur.execute(insert_query, (row.Title, 
                                         row.Plot, 
                                         embeddings[i]))

        conn.commit()
        print(f"successfully inserted {len(df)} movies")

except Exception as e:
    # if there was a problem rollback and tell the user what the error is
    conn.rollback()
    print(f"An error occurred: {e}")

finally:
    # Clean up and close connections
    cur.close()
    conn.close()