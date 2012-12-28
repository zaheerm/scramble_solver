"""
scramble_solver.py

Usage:
  scramble_solver.py <grid>
"""
import copy
import time

from collections import defaultdict

from docopt import docopt

POSSIBLE_POSITIONS={
    (0,0):[(0,1), (1,0), (1,1)],
    (0,1):[(0,0), (0,2), (1,0), (1,1), (1,2)],
    (0,2):[(0,1), (0,3), (1,1), (1,2), (1,3)],
    (0,3):[(0,2), (1,2), (1,3)],
    (1,0):[(1,1), (0,0), (0,1), (2,0), (2,1)],
    (1,1):[(1,0), (1,2), (0,0), (0,1), (0,2), (2,0), (2,1), (2,2)],
    (1,2):[(1,1), (1,3), (0,1), (0,2), (0,3), (2,1), (2,2), (2,3)],
    (1,3):[(1,2), (0,2), (0,3), (2,2), (2,3)],
    (2,0):[(2,1), (1,0), (1,1), (3,0), (3,1)],
    (2,1):[(2,0), (2,2), (1,0), (1,1), (1,2), (3,0), (3,1), (3,2)],
    (2,2):[(2,1), (2,3), (1,1), (1,2), (1,3), (3,1), (3,2), (3,3)],
    (2,3):[(2,2), (1,2), (1,3), (3,2), (3,3)],
    (3,0):[(3,1), (2,0), (2,1)],
    (3,1):[(3,0), (3,2), (2,0), (2,1), (2,2)],
    (3,2):[(3,1), (3,3), (2,1), (2,2), (2,3)],
    (3,3):[(3,2), (2,2), (2,3)]}

SCORE = dict(a=1,b=4,c=4,d=2,e=1,f=4,g=3,h=3,i=1,j=10,k=5,l=2,m=4,n=1,o=1,p=4,q=10,r=1,s=1,t=1,u=2,v=5,w=4,x=8,y=3,z=10)
DICTIONARY = defaultdict(bool)
POSSIBLE_PREFIXES = defaultdict(bool) # 'ab':True, 'zx':False

def generate_optimised_grid(grid):
    return [grid[0:4], grid[4:8], grid[8:12], grid[12:16]]
            
def build_words(grid, current_pos, possible_words, word_so_far=None, visited_positions=None):
    if not visited_positions:
        visited_positions = []
    visited_positions.append(current_pos)
    if word_so_far is None:
        word_so_far = ''
    x, y = current_pos
    current_char = grid[x][y]
    word_so_far = "%s%s" % (word_so_far, current_char)
    if word_so_far in DICTIONARY:
        possible_words[word_so_far] = True
    for position in POSSIBLE_POSITIONS[current_pos]:
        if position not in visited_positions and POSSIBLE_PREFIXES["%s%s" % (word_so_far, grid[position[0]][position[1]])]:
#            print "Current position", current_pos, "Next position", position
            build_words(grid, position, possible_words, word_so_far, copy.copy(visited_positions))

def load_dictionary():
    dictionary = open("words.txt","r")
    for line in dictionary:
        DICTIONARY[line.strip().lower()] = True
        previous_chars = ''
        for char in line:
            if previous_chars != '':
                previous_chars = '%s%s' % (previous_chars, char)
                POSSIBLE_PREFIXES[previous_chars] = True
            else:
                previous_chars = char

def score(word):
    the_score = 0
    for char in word:
        the_score += SCORE[char]
    return the_score

def output_possible_words(possible_words):
    words = defaultdict(list)
    for word in possible_words:
        words[score(word)].append(word)
    for score_of_word in sorted(words, reverse=True):
        print "Words of score", score_of_word
        print words[score_of_word]

def main(grid):
    load_dictionary()
    possible_words = defaultdict(bool)
    optimised_grid = generate_optimised_grid(grid)
    start = time.time()
    for pos in POSSIBLE_POSITIONS:
        print "Starting at position", pos
        build_words(optimised_grid, pos, possible_words)
        print "Words so far", len(possible_words)
    end = time.time()
    output_possible_words(possible_words)
    print "Building words took ", end - start

if __name__ == '__main__':
    arguments = docopt(__doc__, version="scramble_solver.py v0.1")
    main(arguments["<grid>"])