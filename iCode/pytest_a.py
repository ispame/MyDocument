

var = 10                    # Second Example
k=2
while var > 0:
   print 'Current variable value :', var
   var = var -1
   if var == 5:
      if k ==2:
        break

print "Good bye!"










import numpy as np
import pytest as tst
def get_internet():
    from selenium import webdriver
    browser = webdriver.Chrome()
    browser.get("https://www.yahoo.com/")
    print browser.title
    assert "Yahoo" in browser.title
    browser.close()


from itertools import groupby

def height_class(h):
    if h > 180:
        return "tall"
    elif h < 160:
        return "short"
    else:
        return "middle"

friends = [191, 158, 159, 165, 170, 177, 181, 182, 190]


# friends = sorted(friends, key = height_class)
# print friends
for m, n in groupby(friends, key = height_class):
    print(m)
    print(list(n))



import datetime
import calendar

def get_month_range(start_day=None):
    if start_day==None:
        start_day=datetime.date.today().replace(day=1)
        a,days_in_months=calendar.monthrange(start_day.year,4)
        print "dddddddddddddddddd",days_in_months,a
        end_date= start_day+datetime.timedelta(days=days_in_months-1)
        return start_day,end_date

print get_month_range()




index=range(0,len(friends))
print index

