#hellow = hellow Then it is an anagram

def anagramcheck(argsOne,argsTwo):
    argsOne = argsOne.replace(" ","").lower()
    argsTwo = argsTwo.replace(" ","").lower()


    print(argsOne," valus split",argsTwo)

    dicttemp = {}

    for valone in argsOne:
        if valone in dicttemp:
            dicttemp[valone]+= 1
        else:
            dicttemp[valone] = 1
    for valtwo in argsTwo:
        if valtwo in dicttemp:
            dicttemp[valtwo] -= 1
        else:
            dicttemp[valtwo] = 1
    for j in dicttemp:
        if dicttemp[j] != 0:
            return False

    #print(dicttemp)
    return True


print(anagramcheck("hellow word","hellow word"))