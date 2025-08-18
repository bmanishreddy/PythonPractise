arrayValues = [2,3,4,7,8,9,10,14,16,18]

serEle = 17

def binarySearch(arrayValues,serEle):
    found = False
    firstVal = 0
    lastVal = (len(arrayValues)-1)



    while firstVal <= lastVal and not found:
        midVal = int((firstVal+lastVal)/2)

        if serEle == arrayValues[midVal]:
            #return midVal
            found = True
        else:
            if arrayValues[midVal] > serEle:
                lastVal = midVal - 1
            else:
                firstVal = midVal + 1
    return found



print(binarySearch(arrayValues,serEle))
