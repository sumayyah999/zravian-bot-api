import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Run some config')
    parser.add_argument('--config', type=str, dest="config_file_path")
    return parser
