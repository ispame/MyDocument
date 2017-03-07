class Person:
    def __init__(self,f_name):
        self.f_name=f_name
    #get
    @property
    def f_name(self):
        return self._first_name
    #set
    @f_name.setter
    def f_name(self,value):
        if not isinstance(value,str):
            raise TypeError("Expected a string")
        self._first_name= value

    @f_name.deleter
    def f_name(self):
        raise AttributeError("delete Error!")

a= Person("Lucy")
b= Person(1323)
print a.f_name
print b.f_name
del a
class Date:
    __slots__=['year','month','day']
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
    count=2
today=Date(1998,12,2)
today.count=3
print today.count





class card:
    count=0
    def __init__(self,name='fire',health=3):

        self.count= self.count+1
        self.name=name
        self.health= health
    def __str__(self):
        return '{},{}'.format(self.name,self.health)
    def __repr__(self):
         return '{},{},{}'.format(self.name,self.health,type(self))
    def healthchange(self,change):
        self.health+=change
        if self.health<0:
            print "die"
            del self

    def __del__(self):
        self.count=self.count-1
        assert card>0
    def howMayr(self):
        return  self.count
def testcard():
    a= card()
    print a
    a
    a.healthchange(-4)
    print "############"
    print a.health

    b=card()
    print a.count
    print b.count
    a= card()
    a= card()
    b=card()
    print b.count
    print card.count


class card:
    count=0
    def __init__(self):
        card.count= card.count+1
        print "new  a card"

    def __del__(self):
        card.count=card.count-1
        assert card>0
    def howMayr(self):
        return  card.count
    def die(self):
        del self
        card.count=card.count-1
        assert card>0





class c:
    i=222
    def __init__(self):
        print "new  a card"
    def __del__(self):
        print "no cards"


def testc():
    c1=c()
    c2=c()
    del c1
    del c2


a_str = 'this is a string'
assert type(a_str)== str
