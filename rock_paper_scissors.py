import random

dictionary = {'r':0, 'p':1, 's':2}
# return 1 if a wins, 0 if draw, -1 if b wins
def beat(a,b):
    if a == b:
        return 0
    # +1 % 3 returns whoever can defeat myself
    if (dictionary[a]+1)%3 == dictionary[b]:
        return -1
    return 1

# 1,2,3 mod 4 does not work => mod4 can have 0,1,2,3, 3+1mod4 = 0

def play():
    user = input("r for rock, p for paper, s for scissor: ")
    computer = random.choice(['r', 'p', 's'])
    # generate random index, then take it from the list?
    result = beat(computer, user)
    if (result > 0):
        print(f"computer played {computer}, and it won")
    elif (result < 0):
        print(f"computer played {computer}, and it lost")
    else:
        print(f"computer played {computer}, and you draw")

play()
