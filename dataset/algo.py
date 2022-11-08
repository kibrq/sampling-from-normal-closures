from json import dumps, loads
from tqdm import trange
from random import shuffle

from core.free_group import normalize, iterable_commutator
from .sampling import create_identites_from_normal_closure, random_from_identities

def single_closure(generators_num, base, depth, words_num, verbose=True):
    generated = set()

    identites = create_identites_from_normal_closure(generators_num, base)
    for _ in (trange if verbose else range)(words_num):
        word = None
        while word is None or dumps(word) in generated:
            word = normalize(random_from_identities(depth, identites))
        generated.add(dumps(word))
    
    return list(map(loads, generated))

def symmetric_commutator(generators_num, bases, depth, words_num, verbose=True):
    generated = set()

    identitess = [create_identites_from_normal_closure(generators_num, base) for base in bases]

    for _ in (trange if verbose else range)(words_num):
        word = None
        while word is None or dumps(word) in generated:
            parts = [random_from_identities(depth, identites) for identites in identitess]
            shuffle(parts)
            word = normalize(iterable_commutator(parts))
        generated.add(dumps(word))
    
    return list(map(loads, generated))
