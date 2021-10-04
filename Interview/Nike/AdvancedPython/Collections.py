#collections
from collections import Counter

a = "aabbbbccccdddddddeeeefffff wqef"

myCounter = Counter(a)

print(myCounter)
print(myCounter.most_common())
print(myCounter.most_common(2))
print(myCounter.elements())


from collections import OrderedDict

