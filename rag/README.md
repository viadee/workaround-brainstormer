# RAG setup for the WA-brainstormer

In order to utilize the feature of retreiving similar workarounds using RAG, a q-drant database needs to be setup:

## Setup and populate the database

```console
python populate_qdrant_db.py
```

This script will create a q-drant collection named "workaround" if not already present. It will also populate the collection with all the workflow examples from the file workarounds_corpus.csv