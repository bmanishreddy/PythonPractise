def binary_search(cards,query):
    #defining start and ed of the list, starting at zero and end is the last element in this case end mins one
    start = 0; high = len(cards) -1

    while start <= high:
        # looks at the middle element to see if we have to traverse left of right
        mid = (start + high) // 2

        # variable helps us to debug
        print('start', start, 'high', high, 'query', query, 'mid', mid)

        # if the search element is the middle one, the we found it. We can return the value

        if query == cards[mid]:
            return mid
        # if the search element is greater than middle value we have to check for the next element in the array,
        # we are going to iterate by one value
        elif query > cards[mid]:
            start = mid + 1
        # in case the query is lesser than mid, we have to traverse to the left
        elif cards[mid] > query:
            high = mid - 1




dictTest = {
    'input':{'cards':[2,4,6,8,9,12,15],'query':12},
    'output':3
}
result = binary_search(dictTest['input']['cards'],dictTest['input']['query'])
print(result)
