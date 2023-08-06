import os
from random import choice, sample


def get_path(relative_path: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


vowels = {'a', 'e', 'i', 'o', 'u'}

with open(get_path('data/adjectives.txt')) as file:
    adjectives = file.read().split()
with open(get_path('data/nouns.txt')) as file:
    nouns = file.read().split()


def new(word_count=3, capitalize=True, separator='') -> str:
    if word_count not in range(1, 100):
        raise ValueError('Invalid word count!')

    noun = choice(nouns)
    word_list = []

    if word_count > 3:
        if noun in vowels:
            word_list = ['an']
        else:
            word_list = ['the']

    word_list.extend(sample(adjectives, k=word_count - 1))

    if word_count > 4:
        word_list.insert(2, 'and')

    word_list.append(noun)

    if capitalize:
        word_list = map(str.title, word_list)

    return separator.join(word_list)
