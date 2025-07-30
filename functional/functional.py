def zero(func=None): 
    return 0 if func is None else func(0)
def one(func=None):
    return 1 if func is None else func(1)
def two(func=None):
    return 2 if func is None else func(2)
def three(func=None):
    return 3 if func is None else func(3)
def four(func=None):
    return 4 if func is None else func(4)
def five(func=None):
    return 5 if func is None else func(5)
def six(func=None):
    return 6 if func is None else func(6)
def seven(func=None):
    return 7 if func is None else func(7)
def eight(func=None):
    return 8 if func is None else func(8)
def nine(func=None):
    return 9 if func is None else func(9)

def identity(a): return a
def zero(f=identity): return f(0)
def one(f=identity): return f(1)
def two(f=identity): return f(2)
def three(f=identity): return f(3)
def four(f=identity): return f(4)
def five(f=identity): return f(5)
def six(f=identity): return f(6)
def seven(f=identity): return f(7)
def eight(f=identity): return f(8)
def nine(f=identity): return f(9)

def plus(b): return lambda a: a + b
def minus(b): return lambda a: a - b
def times(b): return lambda a: a * b
def divided_by(b): return lambda a: a // b

     #   test.assert_equals(seven(times(five())), 35)
     #   test.assert_equals(four(plus(nine())), 13)
     #   test.assert_equals(eight(minus(three())), 5)
     #   test.assert_equals(six(divided_by(two())), 3)