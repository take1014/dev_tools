#!/usr/bin/env python3
import os
import chardet
import numpy as np
import pandas as pd

def get_encoding(file_path, check_bytes=1000):
    if not os.path.exists(file_path):
        raise ValueError(
            f"Do not exists file path {file_path}"
        )
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(check_bytes))
        print(f"encoding: {result['encoding']}")
        return result['encoding']

class CSVReader:
    def __init__(self):
        self.csv_file_path = None
        self.df = None

    def set(self, csv_file_path:str) -> None:
        if not os.path.exists(csv_file_path):
            raise ValueError(
                f"Do not exists csv file path {csv_file_path}"
            )

        self.csv_file_path = csv_file_path
        # get encoding
        encoding = get_encoding(csv_file_path)
        self.df = pd.read_csv(csv_file_path, encoding=encoding)

    def _exists_dataframe(self):
        if self.df is None:
            raise RuntimeError("No DataFrame has been created. Call `set` first.")

    def get_column_names(self) -> list:
        self._exists_dataframe()
        return self.df.columns.values

    def get_index_names(self) -> list:
        self._exists_dataframe()
        return self.df.index.values

    def get_column_values(self, column_name=None) -> dict:
        self._exists_dataframe()
        if column_name in self.df.columns:
            return {column_name: self.df[column_name].tolist()}
        raise KeyError(f"Column '{column_name}' does not exist in the DataFrame.")

    def get_row_values(self, start_index=0, end_index=0) -> list:
        self._exists_dataframe()
        end_index = start_index+1 if start_index > end_index else end_index
        if start_index in self.df.index and end_index in self.df.index:
            return self.df.iloc[start_index:end_index].values.tolist()
        raise KeyError(f"Row index '{index}' does not exist in the DataFrame.")

if __name__ == '__main__':
    reader = CSVReader()
    reader.set('/home/take/fun/dataset/titanic/train.csv')
    print(reader.get_column_names())
    print(reader.get_index_names())
    print(reader.get_column_values(column_name='Survived'))
    print(reader.get_row_values(start_index=0, end_index=1))

