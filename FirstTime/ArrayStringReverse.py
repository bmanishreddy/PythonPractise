def reverse(s):
    length = len(s)
    spaces = [' ']
    words = []

    i = 0
    while i < length:
        if s[i] not in spaces:
            word_start = i
            while i < length and s[i] not in spaces:
                i += 1
            words.append(s[word_start:i])

        i += 1

    #return s

    return  " ".join(reversed(s))


def reverse1(s):
    Xlen = len(s)
    for i in Xlen:
        print(i)

print(reverse("hellow world how are you "))



