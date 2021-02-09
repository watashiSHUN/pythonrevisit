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


#guess(10)
computer_guess(10)
