"""
Matthew Van Soelen, Cameron Sonn and Ehimare Agboneni
CS-555 Agile Methods
Project 4: GEDCOM Data

This program will read a GEBCOM file print the following for each line:
--> <input line>
<-- <level>|<tag>|<valid?> : Y or N|<arguments>
Stories: us23, us27
"""

import sys
from helper import *
import pymongo

# Choose file to read from
filename = "simple_sample.ged"
if len(sys.argv) > 1:
    filename = sys.argv[1]
print(f"Reading from file: {filename}")

errorFile = open("errors.txt", "w")
errorFile.close()

# Create connection to local MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("cs555_db")
database = client["cs555_db"]

db_indi_col = database.create_collection("people", validator=people_schema)

db_indi_col.create_index(["uid"], unique=True)
db_indi_col.create_index(["NAME", "BIRT"], unique=True)

#db_fam_col = database["families"]

#TODO: fix the required fields in the family_schema validator 
db_fam_col = database.create_collection("families", validator=family_schema)
db_fam_col.create_index(["uid"], unique=True)


# Read file lines into an array
input_list = file_to_array(filename)

find_parent(input_list)
indi_table = create_individual_table(input_list, valid_tags)
db_insert(db_indi_col, indi_table)
indi_pretty = create_pretty_indi_table(db_indi_col)
list_all_deceased(indi_table)
print(indi_pretty)

fam_table = create_family_table(input_list, valid_tags, indi_table)
db_insert(db_fam_col, fam_table)
fam_pretty = create_pretty_fam_table(db_fam_col)
print("Families")
print(fam_pretty)
check_age(indi_table)
check_husband_gender(indi_table, fam_table)
check_wife_gender(indi_table, fam_table)
no_dates_after_current(db_indi_col, db_fam_col)
checkDiv_Deat(db_indi_col, db_fam_col)
invalid_death(indi_table)
invalid_marriage(indi_table, fam_table)
checkDiv_Marr(db_fam_col)
checkMarr_Deat(db_indi_col, db_fam_col)
list_all_orphans(db_indi_col, db_fam_col) # Must be last in order to print output correctly
read_error_file()
