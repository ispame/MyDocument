# -*- coding: utf-8 -*-
import math


class Circle:
    def __init__(self, r):
        self.r = r

    @property
    def area(self):
        return math.pi * self.r ** 2

    # @property
    def perimeter(self):
        return 2 * math.pi * self.r


def testcircle():
    c = Circle(4)
    print c.r
    print c.area
    print c.perimeter()


class Movie1(object):
    def __init__(self, title, rating, runtime, budget, gross):
        self.title = title
        self.rating = rating
        self.runtime = runtime
        self.gross = gross
        # 只能控制初始化的过程
        if budget < 0:
            raise ValueError("Negative value not allowed: %s" % budget)
        self.budget = budget

    def profit(self):
        return self.gross - self.budget


class Movie2(object):
    def __init__(self, title, rating, runtime, budget, gross):
        self._budget = None
        self.title = title
        self.rating = rating
        self.runtime = runtime
        self.gross = gross
        self.budget = budget

    @property
    def budget(self):
        return self._budget

    @budget.setter
    def budget(self, value):
        if value < 0:
            raise ValueError("Negative value not allowed: %s" % value)
        self._budget = value

    def profit(self):
        return self.gross - self.budget



from weakref import WeakKeyDictionary
class NonNegative(object):
    """A descriptor that forbids negative values"""
    def __init__(self,default):
        self.default= default
        self.data= WeakKeyDictionary()
    def __get__(self, instance, owner):
        return self.data.get(instance,self.default)

    def __set__(self, instance, value):
        if value<0:
            raise ValueError("Negative value not allowed: %s" % value)
        self.data[instance]=value

class Movie(object):

    #always put descriptors at the class-level
    rating = NonNegative(0)
    runtime = NonNegative(0)
    budget = NonNegative(0)
    gross = NonNegative(0)

    def __init__(self, title, rating, runtime, budget, gross):
        self.title = title
        self.rating = rating
        self.runtime = runtime
        self.budget = budget
        self.gross = gross

    def profit(self):
        return self.gross - self.budget

def testMovie():
    lovestory = Movie('lovestory',2, 7, 2, 10)

    lovestory.budget = 100
    print lovestory.profit()
    try:
        lovestory.budget = -100
    except:
        print "Woops,not allowed"


testMovie()

