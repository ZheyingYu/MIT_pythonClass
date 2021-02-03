# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*':0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#

def get_word_score(word, n):
    if not word:
        return 0
    else:
        firstComponent = sum(SCRABBLE_LETTER_VALUES[letter] for letter in word.lower())
        secondComponent = max(1,7*len(word)-3*(n-len(word)))
        return firstComponent * secondComponent




#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3)) - 1

    for i in range(num_vowels):
        x = random.choice(VOWELS)         #random.choice 随机抽取
        hand[x] = hand.get(x, 0) + 1    #dict.get(key, default = None) 字典中查找关键值，若键不存在则返回默认值
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    hand['*'] = 1
    
    return hand

#
# Problem #2: Update a hand by removing letters
#


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    hand_copy = hand.copy() #深拷贝，不会随着hand的变化而改变
    for letter in word.lower():
        hand_copy[letter] = hand_copy[letter] - 1
        if hand_copy[letter] == 0:
            del hand_copy[letter]
    new_hand = hand_copy
    return new_hand



#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    is_in_hand = True
    is_in_list = False
    hand_copy = hand.copy()

    #check if word is in hand
    for letter in word.lower():
        if letter not in hand_copy.keys():
            is_in_hand = False
            break
        else:
            hand_copy[letter] = hand_copy[letter] - 1
            if hand_copy[letter] == 0:
                del hand_copy[letter]

    #check if word is in word_list with wildhand
    starIndex = word.find('*')
    new_word = word
    if starIndex == -1:
        if word.lower() in word_list:
            is_in_list = True
    else:
        for vowel in VOWELS:
            new_word = new_word.replace(new_word[starIndex],vowel,starIndex)
            if new_word.lower() in word_list:
                is_in_list = True
                break

    return is_in_hand and is_in_list



#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand[key] for key in hand.keys())

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total score
    total_score = 0
    # As long as there are still letters left in the hand:
    while hand.keys():
        # Display the hand
        print('Current hand: ', display_hand(hand))
        # Ask user for input
        word = input('Enter word, or "!!" to indicate that you are finished: ')
        # If the input is two exclamation points:
        if word == '!!':
            # End the game (break out of the loop)
            print('Total score for this hand: ',total_score)
            break

        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word,hand,word_list):
                # Tell the user how many points the word earned,
                # and the updated total score
                total_score += get_word_score(word,calculate_handlen(hand))
                print('"',word,'"', 'earned', get_word_score(word, calculate_handlen(hand)), 'points. Total:', total_score,'points.')
            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print('That is not a valid word. Please choose another word.')
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand,word)


    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if not hand.keys():
        print('Run out of letters. Total score for this hand: ',total_score)

    # Return the total score as result of function
    return total_score





#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    if letter not in hand.keys():
        return hand
    else:
        alphabet = 'abvdefghijklmnopqrstuvwxyz'
        no_repeatAlphabet = list(set(alphabet) - set(hand.keys()))
        new_letter = random.choice(no_repeatAlphabet)
        hand[new_letter] = hand[letter]
        del hand[letter]

    return hand



    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    #Asks the user to input a total number of hands
    num_hands = int(input('Enter total number of hands: '))

    #keep track on the score
    total_score = 0


    # Before running out of the number of hands, and do not replay the hand
    while num_hands > 0:

        # display current hand and ask player if he wants to substitute
        hand = deal_hand(HAND_SIZE)
        print('Current hand: ', display_hand(hand))
        answer = input('Would you like to substitute a letter?')

        # if the play chose yes to substitute
        if answer == 'yes':
            new_letter = input('Which letter would you like to replace: ')

            #substitute the letter for the player and display the hand again
            hand = substitute_hand(hand,new_letter)

            #start the game and record the highest score for each hand
            hand_score = play_hand(hand,word_list)
        # if player does not want to substitute
        else:
            # play the game and record the highest score for each hand
            hand_score = play_hand(hand, word_list)

        #分割线
        print('----------')

        # Ask if the player if he wants to play the hand again
        answer_playagain = input('Would you like to play the hand again?')

        if answer_playagain == 'yes':
            hand_score = max(hand_score, play_hand(hand,word_list))
            print('----------')

        num_hands -= 1
        total_score += hand_score

    print("Total score over all hands: ", total_score)
    return total_score












#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
