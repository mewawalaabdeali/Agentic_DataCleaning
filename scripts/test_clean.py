import pandas as pd
from dataCleaning import DataCleaner

data = {
    "name": [" Alice ", "Bob", "Charlie", "Alice ", "Bob"],
    "age": [25, 30, None, 25, 30],
    "salary": [50000, 60000, None, 50000, 60000],
    "constant": [1, 1, 1, 1, 1],
    "joined": ["2022-01-01", "2022-01-02", "not_a_date", "2022-01-01", "2022-01-02"]
}

df = pd.DataFrame(data)

cleaner = DataCleaner()
clean_df = cleaner.clean_data(df, missing_value_strategy="mean")

print(clean_df)