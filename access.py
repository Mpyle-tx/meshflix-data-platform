import pandas as pd

from register import CATALOG_PATH


def get_catalog():
    """Return the full data catalog as a pandas DataFrame."""
    return pd.read_csv(CATALOG_PATH)


def list_data_products():
    """Return the names of all data products in the catalog."""
    return get_catalog()["name"].tolist()


def get_location(name):
    """Return the file location of a data product, looked up in the catalog."""
    catalog = get_catalog()
    match = catalog.loc[catalog["name"] == name, "location"]
    if match.empty:
        raise KeyError(f"No data product named '{name}' in the catalog.")
    return match.iloc[0]


def read_data_product(name):
    """Return a data product as a pandas DataFrame."""
    return pd.read_csv(get_location(name))


def write_to_data_product(name, rows):
    """Append rows (list of dicts) to a data product."""
    location = get_location(name)
    columns = pd.read_csv(location, nrows=0).columns
    new = pd.DataFrame(rows).reindex(columns=columns)
    new.to_csv(location, mode="a", header=False, index=False)
