def fun(*args):
    for arg in args:
        print arg

l=[1,2,3,4, "Gano el barca!"]
fun(1,l)


def fun2(*args, **kwargs):
    for item in kwargs.items():
        print item

fun2(x=456, y=45, z=55)
