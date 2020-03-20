import argparse

parser = argparse.ArgumentParser(description='Run some config')

parser.add_argument('--config', type=str, dest="config_file_path")

args = parser.parse_args()