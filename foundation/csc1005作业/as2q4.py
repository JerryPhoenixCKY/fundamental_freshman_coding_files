def rotation(word):
    n = len(word)
    return [word[i:] + word[:i] for i in range(n)]

def group_rotated_words(word_list):
    finalkey= set()
    result = []

    for word in word_list:
        r =rotation(word)
        minr = min(r)
        if minr not in finalkey:
            finalkey.add(minr)
            r.sort()
            result.append(r)

    return result
