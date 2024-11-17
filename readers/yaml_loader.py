#!/usr/bin/env python3
import os
import yaml
from omegaconf import OmegaConf

class YAMLLoader:
    @staticmethod
    def load_from_file(yaml_file_path:str) -> OmegaConf:
        if not os.path.exists(yaml_file_path):
            raise ValueError(
                f"Do not exists yaml file path {yaml_file_path}"
            )
        with open(yaml_file_path, 'r') as f:
            dict_data = yaml.safe_load(f)

        return OmegaConf.create(dict_data)

if __name__ == '__main__':
    loader = YAMLLoader()
    json_data = loader.load_from_file('./config.yaml')
    print(json_data.database.port)
    print(json_data.app.version)
