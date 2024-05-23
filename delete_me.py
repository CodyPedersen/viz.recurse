
def my_fn(*args, **kwargs):
    print(args)
    print(kwargs)

d = {'a':1, 'b':2}
my_fn(3,4,**d)
my_fn(1,2,john=1,bob=2)