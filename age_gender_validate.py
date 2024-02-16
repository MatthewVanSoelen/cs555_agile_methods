from ged_validator import *

def check_age(indi_table):
    for person in indi_table:
        #check if a person lived for 150 years or older
        if person['AGE'] >=150 and person['ALIVE'] == False:
            print(f'Age of individual after death is 150 or greater, please check birth and death date')
        else:
            name = person['NAME']
            age = person['AGE']
            print(f'{name}: {age} years old')

def check_gender(indi_table, fam_table):
    for person in indi_table:
        #check indivdual against family table to see if they have husband tag
        if person['uid'] == fam_table[-1]["HUSB"]:
            name = person['NAME']
            #check if gender was set to M for the husband
            if person['SEX'] != 'M':
                print(f'incorrect gender has been used for the husband: {name}')
            else:
                print(f'correct gender used for the husband: {name}')
        #check indivdual against family table to see if they have wife tag
        if person['uid'] == fam_table[-1]["WIFE"]:
            name = person['NAME']
            #check if gender was set to F for the wife
            if person['SEX'] != 'F':
                print(f'incorrect gender has been used for the wife: {name}')
            else:
                print(f'correct gender used for the wife: {name}')

age_response = check_age(indi_table)
gender_response = check_gender(indi_table, fam_table)
print(age_response)
print(gender_response)