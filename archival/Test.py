test = [2,4,6,7,8,10,14,15,15,17]

[2,4,6,7,11]

tempdict = {}

def duplicateEle(test):

    for i in test:
        if i in tempdict:
            tempdict[i]+=1
        else:
            tempdict[i] = 1
    print(tempdict)
    for j in tempdict:
        print(tempdict[j])
        if tempdict[j] == 2:
            print(tempdict[j])

duplicateEle(test)