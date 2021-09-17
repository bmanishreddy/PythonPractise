def locatecards(cards,query):
    """

    :type query: object
    """

   # if len(cards) == 0:
    #    return False
    #Create a position which is pointing to zero
    position = 0
    #set a wile loop which starts and also check if the length of cards is zero
    while position < len(cards):

        #check the first element and current position if it matches
        if cards[position] == query:
            #if the match is found return it and exit the loop
            return position
        else:
            #go and increment the value and search the second card
            position+=1
        #We are trying to check if it is the end of list so we can quit and return that it has ended
        if cards[position] == len(cards):

            #If number is not found return -1
            return -1






dictTest = {
    'input':{'cards':[2,5,7,3,9,6],'query':9},
    'output':4
}


dictTest = {
    'input':{'cards':[2,5,7,7,7,7,7,3,9,6],'query':7},
    'output':3
}
result = locatecards(dictTest['input']['cards'],dictTest['input']['query'])
print(result)
