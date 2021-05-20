
#DJANGO IMPORTS


#PYTHON IMPORTS

import re
import json

# Adhaar Validation
def verify_adhaar(number):

    c = 0

    d = [
	    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
	    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
	    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
	    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
	    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
	    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
	    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
	    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
	    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
	]

    p = [
	    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
	    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
	    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
	    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
	    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
	    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
	    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
	    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
	]

    inverted_array = number[::-1]

    print(inverted_array)

    inverted_array = int(inverted_array)

    rev_list = list(map(int,str(inverted_array)))

    for ind,value in enumerate(rev_list) :
        c = d[c][p[( ind % 8)][value]]

    return (c == 0)


#Name Validation
def validate_name(name):
	
	nameRegex = "^[a-zA-Z\s]+$"

	if re.match(nameRegex,name) == None:
		return False
	else :
		return True


#Password Validation
def validate_password(password):
    
    passwordRegex = "^[A-Za-z0-9@#$%^&+=]{8,}$"

    if re.match(passwordRegex,password) == None:
        return False
    else :
        return True


#Username Validation
def validate_username(username):

    usernameRegex = "^[\w\d]+[@#$%^&*+=,.]{0,}[\w\d]*$" 

    if len(username) < 4 or re.match(usernameRegex,username) == None :
        return False
    else :
        return True



#Mobile Number Validation
def validate_mobile_number(number):
	
	phoneRegex = "^([7|8|9][0-9]{9})$"

	if re.match(phoneRegex,number) == None:
		return False
	else :
		return True

  

#State District Choices(Form)
state_district_obj = open('static/state_district.json')
state_district_dict = json.load(state_district_obj)

#get all States
def get_states():
    states = []
    for x in state_district_dict['states']:
        states.append((x['state'],x['state']))
    return states

#get state wise ditricts
def get_districts(state):
    districts = []
    for x in  state_district_dict['states']:
        if x['state'] == state :
            districts = x['districts']
    return districts


#GET ALL DISTRICTS
def get_all_districts():
	districts = []
	for x in state_district_dict['states'] :
		for y in x['districts']:
			districts.append((y,y))
	return districts


#GET STATE WISE DISTRICTS DICTIONARY
def get_districts_dict(state):
	districts = []
	for x in state_district_dict['states'] :
		if x['state'] == state :
			for y in x['districts'] :
				districts.append( (y,y) )
			return districts 
				