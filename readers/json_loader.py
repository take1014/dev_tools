#!/usr/bin/env python3
import os
import json
from omegaconf import OmegaConf

class JSONLoader:
    @staticmethod
    def load_from_file(json_file_path:str) -> OmegaConf:
        if not os.path.exists(json_file_path):
            raise ValueError(
                f"Do not exists json file path {json_file_path}"
            )
        with open(json_file_path, 'r') as f:
            dict_data = json.load(f)
        return JSONLoader.load(dict_data)

    @staticmethod
    def load(dict_data:dict) -> OmegaConf:
        if dict_data is None:
            raise ValueError("dict_data must not be None")
        return OmegaConf.create(dict_data)

if __name__ == '__main__':
    dict_data = {
      "database": {
        "host": "localhost",
        "port": 5432
      },
      "app": {
        "name": "my_application",
        "version": 1.0
      }
    }
    loader = JSONLoader()
    json_data = loader.load_from_file('./test.json')
    print(json_data.database.port)
    print(json_data.app.version)
