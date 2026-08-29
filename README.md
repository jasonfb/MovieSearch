
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
- [x] Step 2: Embedding generation
- [x] Step 3: Ingestion (`ingest.py`)
- [ ] Step 4: Indexing + query (`search.py`)
- [ ] Step 5: Evaluation

## Concepts: what's actually in the `embedding` column?

**What is a vector here?** A fixed-size list of numbers — 384 floats — that represents the *meaning* of a plot's text. Two plots about similar stories end up with vectors that are numerically close together; unrelated plots end up far apart. That's what makes similarity search possible: comparing meaning becomes comparing numbers.

**Why always 384 numbers?** Because `all-MiniLM-L6-v2` (the model we use) was trained to always output 384 dimensions, regardless of how long or short the input text is. This is a property of the specific model, not something we chose. A different model (e.g. OpenAI's `text-embedding-3-small`, 1536 dims) would need a different column size — and vectors from two different models can't be compared against each other, since they don't share the same "meaning space." Query model and ingestion model must always match.

**Does the model "know" English, like a dictionary?** Not in the sense of stored definitions. There are two layers to this:
- The *tokenizer* really does have a static lookup table: a fixed vocabulary of ~30k subword pieces, each mapped to an ID, each ID mapped to an initial numeric vector. That part is a literal list with numbers attached.
- But those initial per-token vectors then pass through several transformer layers, where attention lets each token's vector shift based on the words around it ("bank" near "river" vs. "bank" near "money"). Only after that context-dependent reshuffling do all the token vectors get pooled into one final 384-number sentence vector.

So the model's "understanding" is learned statistical association from massive exposure to English text during training — not a symbolic dictionary of meanings.

**What if the plot text were gibberish or an unknown language?** Nothing crashes. The tokenizer will still chop the text into *something* (falling back to subword fragments or unknown-token markers), and `.encode()` still returns a 384-dim vector. But that vector is meaningless noise — the model never learned real patterns for that input, so distances computed against it are meaningless too, even though the query runs fine and returns results. Nothing signals the failure; it just silently stops meaning anything.