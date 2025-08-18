#hellow = wolleh = anagram

def anagram_sol(s1,s2):
    #read botht the strigs and convert them to small and remove them split them
    s1 = s1.replace(' ','').lower()
    s2 = s2.replace(' ','').lower()

    print(s1,s2)

    dict_decide = {}

    for i in s1:
        #checking if the word is present, if it already has adding it to an existing array
        if i in dict_decide:
            dict_decide[i] += 1
        else:
            #If the word is not present we are adding it
            dict_decide[i] = 1
    for j in s2:
        if j in dict_decide:
            #if the value is already present subract it
            dict_decide[j] -= 1
        else:
            #if not present append it
            dict_decide[j] = 1

    #let us check the length of the dict and decide on rhe result
    for k in  dict_decide:
        if dict_decide[k] != 0:
            return False

    print(dict_decide)




    return True

print(anagram_sol("Hellow world", "hellow worldd"))