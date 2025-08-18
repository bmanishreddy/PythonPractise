

def divfun(x,y):
    return x/y



def divdecorator(fun):
    def wrapper(x,y):
        if y>x:
            x,y = y,x
        return fun(x,y)
    return wrapper


print(divfun(2,4))

divone = divdecorator(divfun)

print(divone(2,4))



@divdecorator
def divfun(x,y):
    return x/y



def divdecorator(fun):
    def wrapper(*args,**kwargs):
        if fun.__y__>fun.__x__:
            fun.__y__,fun.__x__ = fun.__x__,fun.__y__
        return fun(*args,**kwargs)
    return wrapper


print(divfun(1,4))
