import random


# range 1->x
def guess(x):
    random_number = random.randint(1,x)
    # init user's guest, it will never be the random_number at the start
    # guess = None
    while True:
        guess = int(input(f"guess a number between 1 and {x}:")) # default input is string
        # tell the guest whether its greater or smaller
        if guess != random_number:
            print(f"'{guess}' is {'greater' if guess > random_number else 'smaller'} than the target")
        else:
            break
    print("congrations are in order") 

guess(10)
