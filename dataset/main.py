from .algo import *

from json import loads
from pathlib import Path
from time import time

def setup_parser(subparser):
    subparser.add_argument('name', type=str, help='algorithm name')
    subparser.add_argument('arguments', type=str, help='JSON arguments to algorithm')
    subparser.set_defaults(func=main)

def main(args):
    arguments = loads(args.arguments)
    arguments_memo = '-'.join(map(str, arguments.values()))

    save_path = Path('dataset', 'results', args.name, f'{arguments_memo}:{int(time())}')
    save_path.mkdir(parents=True, exist_ok=True)

    print(f'Create dir {save_path}')

    generated = globals()[args.name](**arguments)

    (save_path / 'data.json').write_text(dumps(generated))

