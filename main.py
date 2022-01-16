#import library of the english dictionary
from dataclasses import KW_ONLY
from xml.dom import WrongDocumentErr
import argparse
import sys
import enchant
import itertools
dict = enchant.Dict("en_US")
wordlist = []
known_letters = ''
bad = ""

def clean_letters(bad):
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in bad:
        s = s.replace(i.capitalize(),'')
    return s

def generate_words(wordlist,bad,known_letters,possible_letters):
    s = clean_letters(bad)
    nums = list(s)
    permutation = list(itertools.permutations(nums,5))
    percent = len(permutation)
    curr_percent = 0
    for i in permutation:
        curr_percent += 1
        #calculate the percent of the permutation
        if dict.check(''.join(i)):
            sys.stdout.write(f"\r Current Percent: {str(round(curr_percent/percent,2)*100)}")
            sys.stdout.flush()
            guard = 0
            for key, value in known_letters.items():
               if ''.join(i)[key] == value:
                   guard += 1
            for z in possible_letters:
                if z not in ''.join(i):
                    guard = 0
            if guard == len(known_letters):
                wordlist.append(''.join(i))         

def known_letter_positions(known_letters):
    positions = {}
    # Get position of letters in word
    for i in range(len(known_letters)):
        if known_letters[i] != '_':
            positions.update({i:known_letters[i]})
    return positions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bad", help="Bad letters")
    parser.add_argument("-k", "--known", nargs='?', help="Known letters by posistion.\n Example A__LE")
    parser.add_argument("-p", "--possipable", nargs='?', help="Known letters, unknwon position.")
    args = parser.parse_args()
    bad = args.bad
    known_letters = args.known
    possible_letters = args.possipable
    if bad == None:
        bad = ''
    if known_letters == None:
        known_letters = ''
    else:
        known_letters = known_letter_positions(args.known)
    if possible_letters == None:
        possible_letters = ''

    generate_words(wordlist,bad,known_letters,possible_letters)
    print('\033c')
    print(wordlist)