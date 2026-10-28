# Meshflix Self-Serve Data Platform

A small Python platform that lets a team register a **data product**, list it in a **data catalog**, and read or append to it from Python. It applies data mesh ideas (domain ownership, data as a product, self-serve infrastructure) at a small scale.

Built for the Manning liveProject *Build a Self-Serve Data Platform* as part of ITSE 1350 Systems Analysis & Design at Kilgore College.

## Who it is for

| Persona | How they use data | Access route |
|---|---|---|
| Analyst | Excel and SQL, finds data by browsing | CSV files and the catalog (SQL not covered here) |
| Machine learning engineer | Python APIs and batch files to pretrain models | CSV and Python |
| Data scientist | Jupyter notebooks and prototypes | Native Python |

## How it works

- `register.py` creates a data product (a CSV with a defined schema) and adds one row for it in `data_folder/catalog.csv`.
- `access.py` looks a data product up in the catalog and reads it into a pandas DataFrame, or appends rows to it.

### Catalog attributes

| Attribute | Why it matters |
|---|---|
| name | Unique ID for the data product |
| location | Where the data lives |
| owner | The domain team responsible |
| description | What the data is, in plain language |
| schema | Column names, separated by `\|` |
| created_at | When it was registered |

Registering a name that already exists is rejected, so an existing product's data is never overwritten.

## Setup

```
pip install pandas fire
```

## Usage

Register data products:

```
python register.py register --name=movie_popularity --schema=movie_id,title,views --owner=content_team --description="Views per movie"
python register.py register --name=cast_list --schema=movie_id,actor,role --owner=content_team --description="Cast per movie"
```

List the catalog:

```
python register.py catalog
```

Read and write from Python:

```python
from access import read_data_product, write_to_data_product, get_catalog

write_to_data_product("movie_popularity", [{"movie_id": 1, "title": "Example", "views": 100}])
print(read_data_product("movie_popularity"))
print(get_catalog())
```

## What I learned

- Why ownership and a catalog matter more than the storage format.
- Keeping a registration step safe: check the catalog first, then create files.
- Git details that cost time, such as a `.gitignore` rule that hid my data folder.

## Limits

This is a learning prototype. It uses local CSV files, has no authentication, and has no automated tests. Access control, data quality checks, and SQL access would come next.
