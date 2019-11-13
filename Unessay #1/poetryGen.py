#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# -*- coding: utf-8 -*-

# All this file does is call the library which actually generates the poem.

# For reading arguments from the command line
import argparse
import sys

# Library for generating poem
import poetryGenLib

# reads inputs from the command line
parser = argparse.ArgumentParser(description='Generates a poem')
parser.add_argument('template', help='A comma-delimited list of pairs of numbers, representing the number of syllables in a line, and a string, representing the ending rhyme of the line or skipped if no rhymes are used, seperated with no spaces. For example: a haiku would look like "5,7,5", and a rhyming couplet would look like "8A,8A".')
parser.add_argument('-t', '--topics', help='a comma-delimited list of words to use as a topic for the poem. For multiple words, wrap in quotes.', default='')
args = parser.parse_args()

template = poetryGenLib.checkSyntax(args.template)
if (not template):
    # input was not valid
    parser.print_help()
    sys.exit()

# seperate on commas and then strip whitespace
topics = [s.strip() for s in args.topics.split(',')]

generator = poetryGenLib.poemGenerator()

print(generator.generatePoem(template, topics))


