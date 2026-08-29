
Similarity search for 

## Setup environment
```
python3 -m venv venv
source venv/bin/activate
pip install sentence-transformers pandas
pip install pandas
pip install psycopg2-binary
```

## Database

Using Postgres + pgvector via Homebrew (no Docker).

```
psql postgres -f schema.sql
```
(drop with `psql postgres -f drop.sql`)

## Data

`data/wiki_movie_plots_deduped.csv` — Wikipedia movie plots dataset (Title, Plot columns), ~34k rows.

## Progress

- [x] Step 1: Postgres + pgvector schema (`schema.sql`)
- [x] Step 2: Embedding generation (in progress)
- [x] Step 3: Ingestion (`ingest.py`)
- [ ] Step 4: Indexing + query (`search.py`)
- [ ] Step 5: Evaluation