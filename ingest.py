import pandas as pd
import psycopg2


df = pd.read_csv("data/wiki_movie_plots_deduped.csv")
print(df.shape)
print(df.columns)

conn = psycopg2.connect(
    host="localhost",
    database="moviesearch", 
   
    port="5432"
)


cur = conn.cursor()

insert_query = """
INSERT INTO movies (title, plot) 
VALUES (%s, %s);
"""


try:
        for row in df.itertuples(index=False):
              cur.execute(insert_query, (row.Title, row.Plot))

        conn.commit()
        print(f"successfully inserted {len(df)} movies")

except Exception as e:
    conn.rollback()
    print(f"An error occurred: {e}")

finally:
    # 7. Clean up and close connections
    cur.close()
    conn.close()