from django.test import TestCase

# Create your tests here.
class A:
    def __init__(self):
        print('enterA')
        print('outA')

class B:
    def __init__(self):
        print('enterB')
        print('outB')

class C(A):
    def __init__(self):
        print('enterC')
        super().__init__()
        print('outC')

class D(B):
    def __init__(self):
        print('enterD')
        B.__init__(self)
        print('outD')

class F(D,C):
    def __init__(self):
        print('enterF')
        super().__init__()
        print('outF')

f=F()


a = []
def test(a):
    a.append(1)
    print(a)


print(a)
test(a)

b=1
def test1(b):
    b=2
    print(b)
test1(b)
print(b)


class A:
    pass
a=A()
b=A()
print(a is b)
print(a==b)


