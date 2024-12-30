# src/config/__init__.py

import os.path as osp
import yaml


def load_config(config_path=None):
    """Load configuration from YAML file"""
    if config_path is None:
        config_path = osp.join(osp.dirname(osp.abspath(__file__)), 'default_config.yaml')

    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {str(e)}")
        print("Using default values")
        return {
            "chunking": {
                "chunk_size": 1000,
                "overlap": 100
            }
        }