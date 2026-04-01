def group_anagrams(word_list):
    group={}
    for i in word_list:
        k= ''.join(sorted(i))
        group.setdefault(k, []).append(i)
    return list(group.values())