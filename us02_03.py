from ged_validator import indi_table, fam_table, input_list
from datetime import *

# us02: Birth Before Marriage - check that married individuals were born before they got married
def invalid_marriage(indi_table, fam_table):
	invalid = False
	for person in indi_table:
		if person['uid'] == fam_table[-1]["WIFE"] or person['uid'] == fam_table[-1]['HUSB']:
			marriage = str(datetime.strptime(fam_table[-1]["MARR"], "%d %b %Y"))
			birth = str(datetime.strptime(person["BIRT"], "%d %b %Y"))
			if marriage <= birth:
				name = person['NAME']
				uid = person['uid']
				birthday = person['BIRT']
				marr_date = fam_table[-1]['MARR']
				msg = 'Error: INDIVIDUAL: US02: Individual was recorded as married before they were born, please check birth and marriage date: ' + name + '(' + uid + ')\nBirthday: ' + birthday + '\nMarriage Date: ' + marr_date 
				with open("errors.txt", "a") as errorFile:
					errorFile.write(msg + '\n')
				invalid = True
			else:
				invalid = False
	return invalid

# us03: Birth Before Death - check that married individuals were born before they died
def invalid_death(indi_table):
	invalid = False
	death = ''
	for person in indi_table:
		if person['DEAT'] != 'NA':
			death = str(datetime.strptime(person["DEAT"], "%d %b %Y"))
		birth = str(datetime.strptime(person["BIRT"], "%d %b %Y"))
		if death != '' and person['ALIVE'] == False and death < birth:
			name = person['NAME']
			uid = person['uid']
			birthday = person['BIRT']
			death_date = person['DEAT']
			msg = 'Error: INDIVIDUAL: US03: Individual was recorded as dead before they were born, please check birth and death date: ' + name + '(' + uid + ')\nBirthday: ' + birthday + '\nDeath: ' + death_date
			with open("errors.txt", "a") as errorFile:
				errorFile.write(msg + '\n')
			invalid = True
		else:
			invalid = False
	return invalid

