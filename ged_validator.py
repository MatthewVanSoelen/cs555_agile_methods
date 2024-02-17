"""
Matthew Van Soelen 
CS-555 Agile Methods
Project 2: GEDCOM Data

This program will read a GEBCOM file print the following for each line:
--> <input line>
<-- <level>|<tag>|<valid?> : Y or N|<arguments>
"""

import sys
from helper import *
import pymongo

# Choose file to read from
filename = "simple_sample.ged"
if len(sys.argv) > 1:
    filename = sys.argv[1]
print(f"Reading from file: {filename}")

# Create connection to local MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["cs555_db"]
db_collection = database["people"]

# Read file lines into an array
input_list = []
try:
    with open(filename, "r") as fstream:
        for line in fstream:
            line = line.strip()
            result = parse_input(line)
            input_list.append(result)
except:
    print(f"Unable to open file: {filename}")

find_parent(input_list)
indi_table = create_individual_table(input_list, valid_tags)
db_insert(db_collection, indi_table)

indi_pretty = create_pretty_indi_table(indi_table)
# print("Individuals")
# print(indi_pretty)

fam_table = create_family_table(input_list, valid_tags, indi_table)
fam_pretty = create_pretty_fam_table(fam_table)
# print("Families")
# print(fam_pretty)
