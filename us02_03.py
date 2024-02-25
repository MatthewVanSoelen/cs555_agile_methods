from ged_validator import indi_table, fam_table, input_list
from datetime import *

def invalid_marriage(indi_table, fam_table):
	invalid = False
	for person in indi_table:
		if person['uid'] == fam_table[-1]["WIFE"] or person['uid'] == fam_table[-1]['HUSB']:
			marriage = str(datetime.strptime(fam_table[-1]["MARR"], "%d %b %Y"))
			birth = str(datetime.strptime(person["BIRT"], "%d %b %Y"))
			if marriage <= birth:
				name = person['NAME']
				uid = person['uid']
				marr_date = fam_table[-1]['MARR']
				msg = 'Error: INDIVIDUAL: US02: Individual was recorded as married before they were born, please check birth and marriage date: ' + name + '(' + uid + ')\nMarriage Date: ' + marriage + '\nBirthday: ' + birth
				# print('Invalid Marriage: ' + marriage < birth)
				with open("errors.txt", "a") as errorFile:
					errorFile.write(msg + '\n')
				invalid = True
			else:
				invalid = False
	return invalid

def invalid_death(indi_table):
	invalid = False
	death = ''
	for person in indi_table:
		if indi_table[-1]['DEAT'] != 'NA':
			death = str(datetime.strptime(person["DEAT"], "%d %b %Y"))
		birth = str(datetime.strptime(person["BIRT"], "%d %b %Y"))
		if death != '' and death < birth:
			name = person['NAME']
			uid = person['uid']
			msg = 'Error: INDIVIDUAL: US03: Individual was recorded as dead before they were born, please check birth and death date: ' + name + '(' + uid + ')\n Birthday: ' + birth + '\nDeath: ' + death
			with open("errors.txt", "a") as errorFile:
				errorFile.write(msg + '\n')
			invalid = True
		else:
			invalid = False
	return invalid

