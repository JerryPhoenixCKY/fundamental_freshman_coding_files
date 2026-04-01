def character_frequency(input_str):
    group = {}
    result={}
    for i in input_str:
        group[i] = group.get(i, 0) + 1
    for key,value in group.items():
        result.setdefault(value,[]).append(key)
    for i in result.values():
        i.sort()
    return dict(sorted(result.items()))