def strcomp(s1):
    s1 = s1.replace(' ','').lower()



    count = {}
    for letter in s1:
        if letter in count:
            count[letter] +=1
        else:
            count[letter] = 1
    return count





print(strcomp('helllllo'))
