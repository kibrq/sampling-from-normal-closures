from typing import List
from functools import reduce


Word = List[int]

def reciprocal(word: Word) -> Word:
    return [-factor for factor in word[::-1]]


def conjugation(word: Word, conjugator: Word) -> Word:
    return reciprocal(conjugator) + word + conjugator


def commutator(x: Word, y: Word) -> Word:
    return reciprocal(x) + reciprocal(y) + x + y


def iterable_commutator(words: List[Word]): 
    return reduce(commutator, words)


def word_as_str(word: Word) -> str:
    letters = "xyzpqrstuvwklmn"
    inverse_letters = letters.upper()

    return ''.join([letters[abs(f) - 1] if f >= 0 else inverse_letters[abs(f) - 1] for f in word])


def print_word(word: Word):
    print(word_as_str(word))


class Rule:
    def __init__(self):
        pass

    def __call__(self, reduced):
        raise NotImplementedError

class ZeroRule(Rule):
    def __init__(self):
        super().__init__()

    def __call__(self, reduced):
        if reduced[-1] == 0:
            del reduced[-1]

class ReciprocalRule(Rule):
    def __init__(self):
        super().__init__()

    def __call__(self, reduced):
        if len(reduced) >= 2 and reduced[-2] == -reduced[-1]:
            del reduced[-2:]

class BaseShiftRule(Rule):
    def check_cyclic_shift(base):
        doubled_base = base * 2
        def check(word):
            for i in range(len(doubled_base)):
                if word == doubled_base[i:i+len(base)]:
                    return True
        return check

    def __init__(self, base):
        super().__init__()
        self.base = base

        self.check            = BaseShiftRule.check_cyclic_shift(base)
        self.check_reciprocal = BaseShiftRule.check_cyclic_shift(reciprocal(base))

    def __call__(self, reduced):
        if self.base and len(reduced) >= len(self.base) and \
                (self.check(reduced[-len(self.base):]) or self.check_reciprocal(reduced[-len(self.base):])):
            del reduced[-len(self.base):]


def reduce_with_rules(word: Word, rules: List["Rule"]) -> Word:
    reduced = []
    for factor in word:
        reduced.append(factor)
        for rule in rules:
            rule(reduced)
    return reduced

def iterable_reduce_with_rules(word: Word, rules: List["Rule"]) -> Word:
    reduced = []
    for factor in word:
        reduced.append(factor)
        for rule in rules:
            rule(reduced)
        yield reduced


def normalize(word: Word) -> Word:
    return reduce_with_rules(word, [ZeroRule(), ReciprocalRule()])


def normal_closure_embedding(base: Word, word: Word) -> Word:
    return reduce_with_rules(word, [ZeroRule(), ReciprocalRule(), BaseShiftRule(base)])

def iterable_normal_closure_embedding(base: Word, word: Word) -> Word:
    return iterable_reduce_with_rules(word, [ZeroRule(), ReciprocalRule(), BaseShiftRule(base)])


def distance_to_normal_closure(base: Word, word: Word) -> Word:
    return len(normal_closure_embedding(base, word))


def is_from_normal_closure(base: Word, word: Word) -> Word:
    return distance_to_normal_closure(base, word) == 0


def minimal_change_to_identity(word: Word) -> int:
    inf = 10 ** 9
    n = len(word)

    dp = [[inf for d in range(0, n - l + 1)] for l in range(n)]
    for l in range(n):
        dp[l][0] = 0
        dp[l][1] = 0 if word[l] == 0 else 1

    for d in range(2, n + 1):
        for l in range(n - d + 1):
            choice = [
                dp[l + 1][d - 1] if word[l] == 0 else inf,
                dp[l][d - 1] if word[l + d - 1] == 0 else inf,
                dp[l + 1][d - 2] if word[l] == -word[l + d - 1] else inf,
                1 + dp[l + 1][d - 2], # change one of word[l], word[r] to make them reciprocal
                1 + dp[l][d - 1], # change word[r] to 0
                1 + dp[l + 1][d - 1], # change word[l] to 0
                *[dp[l][split - l] + dp[split][l + d - split] for split in range(l, l + d)]
            ]
            dp[l][d] = min(choice)

    return dp[0][n]

