import random
from words import words
import string

# lives in hangman
mistakes = 10

# no abc-def 
# return a valid word
def GetValidWord():
    while True:
        random_select = random.choice(words)
        if '-' not in random_select and ' ' not in random_select:
            return random_select

# option2, keeping only 2 sets
# 1, the alphabet
# 2, used letters (guessed, right/wrong)
# 1-2 = new letters

# every single time guess correctly, remove from word_letter
# word_letter = what's left to be matched
def Play():
    computer_word = GetValidWord()
    mistake_set = set() # words that user guessed, but wrong
    # map of letters => position
    # set constructor takes in an iterable (string)
    total_letters = set(computer_word)
    length = len(computer_word)
    print(f"please guess the word: {(' ').join(['_']*length)}") # 3 underscores, middle underscore can be used to replace the letter
    # return only lower case letters
    alphabet = set(string.ascii_lowercase)
    partial_result = set() # letters that user has guessed correctly
    while len(mistake_set) < mistakes:
        user_letter = input("letter: ")
        if user_letter not in alphabet:
            print("invalid input")
        elif user_letter in mistake_set or user_letter in partial_result:
            print("already guessed")
        elif user_letter not in total_letters:
            # guessed wrong
            mistake_set.add(user_letter)
            # using set, printing order is not garanteed
            print(f"you've guess wrong {len(mistake_set)} times: {','.join(mistake_set)}, there are a total of {mistakes} tries")
        else:
            # guessed correctly
            partial_result.add(user_letter)
            # print word
            print_word = [ l if l in partial_result else '_' for l in computer_word]
            print(f"new result: {(' '.join(print_word))}")
            if len(partial_result) == len(total_letters):
                print("congrats")
                return
    print(f"correct word is '{computer_word}'")

Play()


