def binarySearchPract(reqarray,searchelement):
    #pick the first and last elemtn in the array and initialize it to min and max
    min = 0 ; max = (len(reqarray)-1)

    #finding the mid point and searching if if found the value .
    while max >= max:
        #here we want to get a mid point, it should be a whole number
        mid = (min+max)//2

        #If we find the element return it
        if reqarray[mid] == searchelement:
            return mid
        #if the element is greater than middle make the mid your new start point
        elif reqarray[mid] < searchelement:
            min = mid+1
        #if the search element is lesser than the mid max is going to decrement it new value
        elif reqarray[mid] > searchelement:
            max = mid - 1

dictTest = {
    'input':{'cards':[2,4,6,8,9,12,15],'query':4},
    'output':3
}
result = binarySearchPract(dictTest['input']['cards'],dictTest['input']['query'])
print(result)



