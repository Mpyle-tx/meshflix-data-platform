"""Example: using the Meshflix data platform access helpers."""
from access import (
    list_data_products,
    get_location,
    read_data_product,
    write_to_data_product,
)

# 1. List the data products in the catalog
print("Data products:", list_data_products())

# 2. Find where a data product lives
print("movie_popularity is stored at:", get_location("movie_popularity"))

# 3. Add sample rows the first time, so there is something to load
if read_data_product("movie_popularity").empty:
    write_to_data_product("movie_popularity", [
        {"movie_id": 1, "title": "Example Movie A", "views": 1200},
        {"movie_id": 2, "title": "Example Movie B", "views": 845},
    ])
if read_data_product("cast_list").empty:
    write_to_data_product("cast_list", [
        {"movie_id": 1, "actor": "Actor One", "role": "Lead"},
        {"movie_id": 2, "actor": "Actor Two", "role": "Lead"},
    ])

# 4. Load every data product into a pandas DataFrame
for name in list_data_products():
    print(f"\n{name}:")
    print(read_data_product(name))
