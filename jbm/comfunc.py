'''
    This module contains functions that will be used in the application
'''

from datetime import datetime, date
from time import time

mr = ['Marital Status','Married', 'Single', 'Widow', 'Widower']
gr = ['Gender','Female', 'Male']
rs = [
	'Relationship','Wife', 'Husband', 'Mother', 'Father', 
	'Aunt', 'Uncle', 'Sister', 'Brother','Child', 'Cousin', 
	'Grand Child', 'Student', 'Friend'
]

# Generating years of birth
year = (y for y in range(1924, 2025, 1))
years = ['Year']
for x in year:
	years.append(x)


# Generating days of birth
day = (y for y in range(1, 32, 1))
days = ['Day']
for x in day:
	days.append(x)


# Generating months of birth
months = [
	'Month', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

depart = [
	'Department', 'Nurse', 'Doctor', 'Accounts', 'Laboratory', 'admin', 'dispenser'
]

def date_func():
	myDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	myYear = datetime.now().year
	myTime = datetime.now().strftime('%H:%M:%S')
	return (myDate, myYear, myTime)


def age_func(birth_day):
	birth_day = str(birth_day)
	year,month,day = map(int, birth_day.split('-'))
	today = date.today()
	age = today.year - year - ((today.month, today.day) < (month, day))
	return age



def dob_func(var):
	if var == 'Jan':
		month = 1
	elif var == 'Feb':
		month = 2
	elif var == 'Mar':
		month = 3
	elif var == 'Apr':
		month = 4
	elif var == 'May':
		month = 5
	elif var == 'Jun':
		month = 6
	elif var == 'Jul':
		month = 7
	elif var == 'Aug':
		month = 8
	elif var == 'Sep':
		month = 9
	elif var == 'Oct':
		month = 10
	elif var == 'Nov':
		month = 11
	elif var == 'Dec':
		month = 12
	return month