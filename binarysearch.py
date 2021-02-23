
import random
import time # time.time(), return current time

# look up an integer
# if found, return its index else return -1
def naive_search(num_list, target):
    for i,v in enumerate(num_list):
        if target == v:
            return i
    return -1

def binary_search(sorted_list, target):
    start = 0
    end = len(sorted_list)-1
    while(start <= end):
        mid = (start+end)//2
        if sorted_list[mid] == target:
            return mid
        # go left
        elif target < sorted_list[mid]:
            end = mid-1
        else:
            start = mid+1
    return -1

if __name__ == "__main__":
    # runtime analysis
    length = 10000
    test_list = [random.randint(-10*length, 10*length) for _ in range(length)]
    test_list.sort()

    start = time.time()
    for i in test_list:
        naive_search(test_list, i)
    end = time.time()
    print("linear search takes: ", end-start)

    start = time.time()
    for i in test_list:
        binary_search(test_list, i)
    end = time.time()
    print("binary search takes: ", end-start)
