from ged_validator import indi_table, fam_table, input_list

def check_age(indi_table):
	over_150 = False
	for person in indi_table:
		#check if a person lived for 150 years or older
		if person['AGE'] >=150 and person['ALIVE'] == False:
			name = person['NAME']
			uid = person['uid']
			age = str(person['AGE'])
			msg = 'Error: INDIVIDUAL: US07: Age of individual after death is 150 or greater, please check birth and death date: ' + name + '(' + uid + ') died at age: ' + age
			with open("errors.txt", "a") as errorFile:
				errorFile.write(msg + '\n')
			over_150 = True
        #check if a person is currently 150 years or older
		if person['AGE'] >=150 and person['ALIVE'] == True:
			name = person['NAME']
			uid = person['uid']
			age = str(person['AGE'])
			msg = 'Error: INDIVIDUAL: US07: Current age of individual is 150 or greater, please check birthdate: ' + name + '(' + uid + ') is currently: ' + age + ' years old'
			with open("errors.txt", "a") as errorFile:
				errorFile.write(msg + '\n')
			over_150 = True
	return over_150

def check_wife_gender(indi_table, fam_table):

	wife = False

	wife_gender = 'F'
	for person in indi_table:
		#check indivdual against family table to see if they have wife tag
		if person['uid'] == fam_table[-1]["WIFE"]:
			name = person['NAME']
			uid = person['uid']
			indi_gender = person['SEX']
			#check if gender was set to F for the wife
			if person['SEX'] != wife_gender:
				wife = False
				msg = 'Error: FAMILY: US21: Incorrect gender has been used for the wife: ' + name + '(' + uid + '): Current Gender Set to ' + indi_gender + ' - should be set to ' + wife_gender
				with open("errors.txt", "a") as errorFile:
					errorFile.write(msg + '\n')
			else:
				wife = True
	if wife == True:
		return True
	else:
		return False
def check_husband_gender(indi_table, fam_table):
	husband = False
	husband_gender = 'M'
	for person in indi_table:
		#check indivdual against family table to see if they have husband tag
		if person['uid'] == fam_table[-1]["HUSB"]:
			name = person['NAME']
			uid = person['uid']
			indi_gender = person['SEX']
			#check if gender was set to M for the husband
			if person['SEX'] != husband_gender:
				husband = False
				msg = 'Error: FAMILY: US21: Incorrect gender has been used for the husband: ' + name + '(' + uid + '): Current Gender Set to ' + indi_gender + ' - should be set to ' + husband_gender
				with open("errors.txt", "a") as errorFile:
					errorFile.write(msg + '\n')
			else:
				husband = True
	if husband == True:
		return True
	else:
		return False

age_response = check_age(indi_table)
wife_response = check_wife_gender(indi_table, fam_table)
husband_response = check_husband_gender(indi_table, fam_table)
