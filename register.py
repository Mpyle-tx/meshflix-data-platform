import os
from datetime import datetime

import fire
import pandas as pd

DATA_FOLDER = "data_folder"
CATALOG_PATH = os.path.join(DATA_FOLDER, "catalog.csv")
CATALOG_COLUMNS = ["name", "location", "owner", "description", "schema", "created_at"]


def _clean_schema(schema):
    """fire passes --schema=a,b,c as a tuple; accept a string too."""
    if isinstance(schema, str):
        schema = schema.split(",")
    return [str(col).strip() for col in schema]


def _ensure_catalog():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    if not os.path.exists(CATALOG_PATH):
        pd.DataFrame(columns=CATALOG_COLUMNS).to_csv(CATALOG_PATH, index=False)


def add_to_catalog(name, location, owner, description, schema):
    _ensure_catalog()
    catalog = pd.read_csv(CATALOG_PATH)
    if name in catalog["name"].values:
        raise ValueError(f"Data product '{name}' is already in the catalog.")
    row = pd.DataFrame([{
        "name": name,
        "location": location,
        "owner": owner,
        "description": description,
        "schema": "|".join(schema),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }])
    row.to_csv(CATALOG_PATH, mode="a", header=False, index=False)


def register_csv_port(name, schema):
    location = os.path.join(DATA_FOLDER, f"{name}.csv")
    pd.DataFrame(columns=schema).to_csv(location, index=False)
    return location


def register_data_product(name, schema, owner="unknown", description=""):
    schema = _clean_schema(schema)
    _ensure_catalog()
    if name in pd.read_csv(CATALOG_PATH)["name"].values:
        print(f"Data product '{name}' is already registered. Nothing changed.")
        return
    print(f"Registering {name} CSV port...")
    location = register_csv_port(name, schema)
    add_to_catalog(name, location, owner, description, schema)
    print(f"Added {name} to the catalog.")

def list_catalog():
    _ensure_catalog()
    print(pd.read_csv(CATALOG_PATH).to_string(index=False))


if __name__ == "__main__":
    fire.Fire({
        "register": register_data_product,
        "catalog": list_catalog,
    })
