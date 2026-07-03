# https://pyjanitor-devs.github.io/pyjanitor/

# Libraries
import numpy as np
import pandas as pd
import janitor

# Sample Data curated for this example
company_sales = {
    "SalesMonth": ["Jan", "Feb", "Mar", "April"],
    "Company1": [150.0, 200.0, 300.0, 400.0],
    "Company2": [180.0, 250.0, np.nan, 500.0],
    "Company3": [400.0, 500.0, 600.0, 675.0],
}

# Pandas functional API
df = (
    pd.DataFrame(company_sales)
    .drop(columns="Company1")
    .dropna(subset=["Company2", "Company3"])
    .rename(columns={"Company2": "Amazon", "Company3": "Facebook"})
    .assign(Google=[450.0, 550.0, 800.0])
)

# With pyjanitor, we enable method chaining with method names that are explicitly named verbs,
# which describe the action taken
df = (
    pd.DataFrame.from_dict(company_sales)
    .remove_columns(["Company1"])
    .dropna(subset=["Company2", "Company3"])
    .rename_column("Company2", "Amazon")
    .rename_column("Company3", "Facebook")
    .add_column("Google", [450.0, 550.0, 800.0])
)
