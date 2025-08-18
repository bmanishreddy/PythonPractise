#Lambda arguments: expression

add10 = lambda x: x+10

print(add10(4))

def add10_fun(x):
    return x + 10

print(add10_fun(4))

mult = lambda x,y: x*y

print(mult(4,8))


#filter
arr = [1, 2, 3, 4, 5, 6]
arr = list(filter(lambda x: x // 2 != 0, arr))
print(arr)