import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype

class DataCleaner:
    def __init__(self):
        pass

    def handle_missing_values(self, df, strategy="mean"):
        """Handle missing values using a specified strategy."""
        if strategy == "mean":
            for col in df.columns:
                if is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].mean(), inplace=True)
        elif strategy == "median":
            for col in df.columns:
                if is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].median(), inplace=True)
        elif strategy == "mode":
            for col in df.columns:
                df[col].fillna(df[col].mode().iloc[0], inplace=True)
        elif strategy == "drop":
            df.dropna(inplace=True)
        else:
            raise ValueError("Unsupported missing value strategy")
        return df
    
    def remove_duplicates(self, df):
        """Remove duplicate rows."""
        return df.drop_duplicates()
    
    def fix_data_types(self, df):
        """Try to conver columns to appropriate data types."""
        for col in df.columns:
            if df[col].dtype=="object":
                sample = df[col].dropna().astype(str).head(5)
                if all(val.replace('.','',1).isdigit() for val in sample):
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                elif all(any(char.isdigit() for char in val) and "-" in val for val in sample):
                    df[col]=pd.to_datetime(df[col], errors='coerce')
        return df
    def trim_whitespace(self, df):
        """Strip whitespace from string columns."""
        for col in df.columns:
            if is_string_dtype(df[col]):
                df[col] = df[col].str.strip()

        return df
    
    def remove_constant_columns(self, df):
        """Remove columns with the same value in all rows."""
        return df.loc[:, df.nunique(dropna=False)>1]
    
    def clean_data(self, df, missing_value_strategy="mean"):
        """Apply all data cleaning steps in sequence."""
        df = self.trim_whitespace(df)
        df = self.handle_missing_values(df, strategy=missing_value_strategy)
        df = self.remove_duplicates(df)
        df = self.remove_constant_columns(df)
        df = self.fix_data_types(df)

        return df


