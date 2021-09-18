def test_location(cards, query, mid):
    tempcard = cards[mid]
    if cards[mid] == query:
        if mid-1 >= 0 and cards[mid-1] == query:
            return 'left'
        else:
            return 'found'
    elif cards[mid] < query:
        return 'left'
    else:
        return 'right'

def locate_card(cards, query):
    lo, hi = 0, len(cards) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        result = test_location(cards, query, mid)
        if result == 'found':
            return mid
        elif result == 'left':
            hi = mid - 1
        elif result == 'right':
            lo = mid + 1
    return -1

dictTest =  {'input': {'cards': [13, 11, 10, 7, 4, 3, 1,1,1,1,1, 0], 'query': 1}, 'output': 6}
result = locate_card(dictTest['input']['cards'],dictTest['input']['query'])
print(result)
