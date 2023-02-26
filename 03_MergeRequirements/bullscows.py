from typing import Tuple
from random import randrange
import sys
import urllib.request
import os.path
import argparse


def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    if (valid):
        while (word not in valid):
            word = input(prompt)
    return word

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    guess_set = set(guess)
    b = 0
    c = 0
    for i in range(min(len(guess), len(secret))):
        if (guess[i] == secret[i]):
            b += 1
    for el in guess_set:
        if el in secret:
            c += 1
    return (b, c)

def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    word = words[randrange(len(words))]
    b, c = 0, 0
    ask_count = 0
    while (b != len(word)):
        b, c = bullscows(ask("Введите слово: ", words), word)
        inform("Быки: {}, Коровы: {}", b, c)
        ask_count += 1
    return ask_count

parser = argparse.ArgumentParser(prog = 'Bulls and Cows',
                                 description='Cow say like program.')


parser.add_argument('dict', 
                    action='store', 
                    help='Dictionary file name or URL.')

parser.add_argument('len',
                    action='store',
                    default=5,
                    type=int,
                    help='Indicates the length of the words used.',
                    nargs='?')


if __name__ == '__main__':
    args = parser.parse_args()
    
    dict = []
    if (os.path.isfile(args.dict)):
        with open(args.dict) as f:
            for line in f:
                word = line.rstrip()
                if (len(word) == args.len):
                    dict.append(word)
    else:
        with urllib.request.urlopen(args.dict) as f:
            for line in f:
                word = line.decode('utf-8').rstrip()
                if (len(word) == args.len):
                    dict.append(word)

    print(gameplay(ask=ask, inform=inform, words=dict))
