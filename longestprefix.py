def find_longest_sequence(words):
    dictionary = {}  # word => highest

    def dfs(word):
        temp_max = 0
        for w in words:
            if len(w) == len(word) + 1 and w[:-1] == word:
                if w not in dictionary:
                    # no backedge
                    dfs(w)
                print(word, w, dictionary[w])
                if temp_max < dictionary[w]:
                    temp_max = dictionary[w]

    result_v = 0
    for w in words:
        # if w in dictionary, it is descendent of previously visited word
        if w not in dictionary:
            # we don't need to add it to the dictionary, since exploring the word will not go back to self
            dfs(w)  # also update dictonary[w]
            if dictionary[w] > result_v:
                result_v = dictionary[w]
    return result_v


test = ["a", "abc", "ab", "aa", "aac", "aacx"]
print(find_longest_sequence(test))

# runtime is O(n^2)
