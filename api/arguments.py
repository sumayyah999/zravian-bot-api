import argparse


def get_parser():
    parser = argparse.ArgumentParser(description='Run some config')
    parser.add_argument('--credentials', type=str, dest="credentials_file_path")
    return parser
