def find_mirror_words(sentence):
    result=[]
    lst=sentence.split()
    for i in lst:
        if i==i[::-1] :
            result.append(i)
    return result


