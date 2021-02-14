import random


# range 1->x
def guess(x):
    random_number = random.randint(1,x)
    # init user's guest, it will never be the random_number at the start
    # guess = None
    while True:
        guess = int(input(f"guess a number between 1 and {x}: ")) # default input is string
        # tell the guest whether its greater or smaller
        # if we don't cast it to int, it compare string and int
        if guess != random_number:
            print(f"'{guess}' is {'greater' if guess > random_number else 'smaller'} than the target")
        else:
            break
    print("congrations are in order") 

def computer_guess(x):
    user_random_number = int(input(f"please ask computer to guess a number between 1 to {x}: "))
    # validate input
    assert( 1 <= user_random_number <= x)
    # binary search
    start = 1
    end = x
    while start <= end:
        mid = (start+end)//2
        print(f"computer guessed {mid}")
        if mid == user_random_number:
            print("Yay, computer got the correct answer")
            break
        elif mid < user_random_number:
            start = mid+1
        else:
            end = mid-1

# because => "b/c"
def computer_guess2(x):
    input(f"think of a random number between 1 and {x}, and computer will guess it: ") # does not store the input
    start = 1
    end = x
    while start <= end:
        # computer guess
        guess = random.randint(start, end)
        user_input = input(f"computer guessed {guess}, is it too [H], too [L] or correct [C]: ").lower()
        if user_input == 'h':
            end = guess-1
        elif user_input == 'l':
            start = guess+1
        else:
            break
    # variable "guess" has function scope
    print(f"yay, computer guessed {guess}")

#guess(10)
#computer_guess(10)
computer_guess2(10)
