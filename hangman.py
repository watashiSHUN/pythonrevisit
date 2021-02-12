import random
from words import words

# no abc-def 
# return a valid word
def GetValidWord():
    while True:
        random_select = random.choice(words)
        if '-' not in random_select and ' ' not in random_select:
            return random_select

def Play():
    mistakes = 5
    mistake_list = []
    computer_word = GetValidWord()
    #map of letters => position
    total_letters = set()
    for l in computer_word:
        total_letters.add(l)
    length = len(computer_word)
    print(f"please guess the word: {(' ').join(['_']*length)}") # 3 underscores, middle underscore can be used to replace the letter
    partial_result = set() # letters that user has guessed correctly
    while len(mistake_list) < mistakes:
        user_letter = input("letter: ")
        if user_letter in mistake_list or user_letter in partial_result:
            print("already guessed")
        elif user_letter in total_letters:
            # guessed correctly
            partial_result.add(user_letter)
            # print word
            print_word = []
            for l in computer_word:
                if l in partial_result:
                    print_word.append(l)
                else:
                    print_word.append("_")
            print(f"new result: {(' '.join(print_word))}")
            if len(partial_result) == len(total_letters):
                print("congrats")
                return
        else:
            mistake_list.append(user_letter)
            print(f"you've guess wrong {len(mistake_list)} times: {','.join(mistake_list)}, there are total of {mistakes} chances")
    print(f"correct word is {computer_word}")

Play()


