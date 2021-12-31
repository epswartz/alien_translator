# Alien translator for fictional languages, used for D&D 5e.
# Uses the methods described in Game Designer's Workshop mTraveler Alien Module 2:
# K'kree, Encounters with the Enigmatic Centaurs, Copyright 1984 by Game Designer's Workshop.

import string
import sys
from random import randint as ri
from random import choices
import random
from functools import cache

CONSONANTS = [
    "B",
    "G",
    "GH",
    "GN",
    "GR",
    "GZ",
    "HK",
    "K",
    "KR",
    "KT",
    "L",
    "M",
    "MB",
    "N",
    "P",
    "R",
    "RR",
    "T",
    "TR",
    "X",
    "XX",
    "XR",
    "XT"
]

VOWELS = [
    "A",
    "AA",
    "E",
    "EE",
    "I",
    "II",
    "O",
    "OO",
    "U",
    "UU",
    "'",
    "!",
    "!!",
    "!'"
]

CONSONANT_FREQUENCIES = [
    1,
    3,
    6,
    4,
    2,
    1,
    2,
    24,
    10,
    1,
    5,
    2,
    1,
    4,
    1,
    12,
    3,
    7,
    2,
    4,
    1,
    1,
    1
]

VOWEL_FREQUENCIES = [
    19,
    2,
    3,
    4,
    6,
    2,
    1,
    2,
    6,
    2,
    8,
    3,
    1,
    1
]

SYLLABLE_TYPES = [
    "V",
    "CV",
    "VC",
    "CVC"
]

INITIAL_TYPE_FREQUENCIES = [
    3,
    15,
    6,
    12
]

AFTER_C_TYPE_FREQUENCIES = [
    12,
    0,
    24,
    0,
]

AFTER_V_TYPE_FREQUENCIES = [
    0,
    24,
    0,
    12
]


class Syllable:
    def __init__(self, text, kind):
        """
        text: The actual text of the syllable
        kind: Syllable kind, one of: ["V", "CV", "VC", "CVC"]
        """
        self.text = text
        self.kind = kind


def word_from_syls(syl_list):
    return "".join([s.text for s in syl_list])


def num_syllables(word: str) -> int:
    """
    Determine the length of a word in syllables.
    """
    return ri(1,6)

def get_vowel():
    return choices(VOWELS, weights=VOWEL_FREQUENCIES)[0]

def get_consonant():
    return choices(CONSONANTS, weights=CONSONANT_FREQUENCIES)[0]


def create_syllable(syl_type: str):
    syllable = get_vowel()
    if syl_type.startswith("C"):
        syllable = get_consonant()
    if syl_type.endswith("C"):
        syllable += get_consonant()

    return Syllable(syllable, syl_type)



def initial_syllable():
    syl_type = choices(SYLLABLE_TYPES, weights=INITIAL_TYPE_FREQUENCIES)[0]
    return create_syllable(syl_type)

def after_consonant_syllable():
    syl_type = choices(SYLLABLE_TYPES, weights=AFTER_C_TYPE_FREQUENCIES)[0]
    return create_syllable(syl_type)

def after_vowel_syllable():
    syl_type = choices(SYLLABLE_TYPES, weights=AFTER_V_TYPE_FREQUENCIES)[0]
    return create_syllable(syl_type)

def add_syllable(syl_list):
    """
    Adds another syllable to the in-progress word,
    which is represented by a syllable list.
    """
    if len(syl_list) == 0:
        new_syl = initial_syllable()
    else:
        if syl_list[-1].kind.endswith("C"):
            new_syl = after_consonant_syllable()
        else:
            new_syl = after_vowel_syllable()
    syl_list.append(new_syl)


@cache
def translate_word(word: str) -> str:
    """
    Translate an individual word.
    """

    syllables = num_syllables(word)
    result = []
    for i in range(syllables):
        add_syllable(result)

    return word_from_syls(result)


def translate_message(message: str) -> str:
    """
    Translate a message.
    Deletes all punctuation, splits by spaces, and translates each word individually.
    """
    result = []
    for word in message.split(" "):
        word = word.translate(str.maketrans('', '', string.punctuation))
        result.append(translate_word(word))
    return " ".join(result)


if __name__ == "__main__":
    message = " ".join(sys.argv[1:])
    print(translate_message(message))