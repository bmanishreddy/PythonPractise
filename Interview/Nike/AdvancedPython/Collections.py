#collections
from collections import Counter

a = "aabbbbccccdddddddeeeefffff wqef"

myCounter = Counter(a)

print(myCounter)
print("--------")
print(myCounter.most_common())
print("--------")

print(myCounter.most_common(2))
print("--------")

print(myCounter.elements())


from collections import OrderedDict

