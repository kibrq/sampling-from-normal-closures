from argparse import ArgumentParser
from sys import argv

from dataset.main import setup_parser

if __name__ == '__main__':
    parser = ArgumentParser(prog = 'Sampling from normal closure')
    subparsers = parser.add_subparsers()
    
    parser_datasets = subparsers.add_parser('dataset', help = 'generating datasets')
    setup_parser(parser_datasets)
    
    args = parser.parse_args()
    args.func(args)

