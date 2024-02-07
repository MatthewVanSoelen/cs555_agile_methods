"""
Matthew Van Soelen 
CS-555 Agile Methods
Project 2: GEDCOM Data

This program will read a GEBCOM file print the following for each line:
--> <input line>
<-- <level>|<tag>|<valid?> : Y or N|<arguments>
"""

valid_tags = {
    "INDI": {
        "level": "0",
        "arguments": "Individual_ID",
        "belongs_to": "top level",
        "meaning": "Define a new individual with ID Individual_ID",
    },
    "NAME": {
        "level": "1",
        "arguments": "String with surname delimited by '/'s ",
        "belongs_to": "INDI",
        "meaning": "Name of individual",
    },
    "SEX": {
        "level": "1",
        "arguments": " 'M' or 'F' (without the quotes)",
        "belongs_to": "INDI",
        "meaning": "Sex of individual",
    },
    "BIRT": {
        "level": "1",
        "arguments": "none",
        "belongs_to": "INDI",
        "meaning": "Birth of individual. Typically followed by 2 DATE record that specifies the date.",
    },
    "DEAT": {
        "level": "1",
        "arguments": "none",
        "belongs_to": "INDI",
        "meaning": "Death of individual. Typically followed by 2 DATE record that specifies the date",
    },
    "FAMC": {
        "level": "1",
        "arguments": "Family_ID",
        "belongs_to": "INDI",
        "meaning": "Individual is a child family with Family_ID",
    },
    "FAMS": {
        "level": "1",
        "arguments": "Family_ID",
        "belongs_to": "INDI",
        "meaning": "Individual is a spouse in family with Family_ID",
    },
    "FAM": {
        "level": "0",
        "arguments": "Family_ID",
        "belongs_to": "top level",
        "meaning": "Define a new family with ID Family_ID",
    },
    "MARR": {
        "level": "1",
        "arguments": "none",
        "belongs_to": "FAM",
        "meaning": "Marriage event for family Typically followed by 2 Date record that specifies the date.",
    },
    "HUSB": {
        "level": "1",
        "arguments": "Individual_ID",
        "belongs_to": "FAM",
        "meaning": "Individual_ID of Husband in family",
    },
    "WIFE": {
        "level": "1",
        "arguments": "Individual_ID",
        "belongs_to": "FAM",
        "meaning": "Individual_ID of Wife in family",
    },
    "CHIL": {
        "level": "1",
        "arguments": "Individual_ID",
        "belongs_to": "FAM",
        "meaning": "Individual_ID of Child in family",
    },
    "DIV": {
        "level": "1",
        "arguments": "none",
        "belongs_to": "FAM",
        "meaning": "Divorce event for family. Typically followed by 2 DATE record that specifies the date.",
    },
    "DATE": {
        "level": "2",
        "arguments": "day, month, and year in Exact Format",
        "belongs_to": ["BIRT", "DEAT", "DIV", "MARR"],
        "meaning": "Date that an event occured",
    },
    "HEAD": {
        "level": "0",
        "arguments": "none",
        "belongs_to": "top level",
        "meaning": "Optional header record at beginning of file",
    },
    "TRLR": {
        "level": "0",
        "arguments": "none",
        "belongs_to": "top level",
        "meaning": "Optional trailer record at end of file",
    },
    "NOTE": {
        "level": "0",
        "arguments": "any string",
        "belongs_to": "top level",
        "meaning": "Optional comments, e.g. describes tests",
    },
}

import re
from datetime import datetime
import sys


def parse_input(input_str: str):
    if (input_str is None) or (len(input_str) < 1):
        return {"tag": "Error: No input Provided", "level": "", "arguments": ""}

    input_arr = input_str.split()
    if len(input_arr) < 1:
        return {
            "tag": "Error: Input does not contain required level and tag field in the correct format.",
            "level": "",
            "arguments": "",
            "original": input_str,
        }

    if (not input_arr[0].isnumeric()) or (input_arr[0] not in ["0", "1", "2"]):
        return {
            "tag": "Error: The level must be 0, 1 or 2.",
            "level": "",
            "arguments": "",
            "original": input_str,
        }
    level = input_arr[0]
    tag = ""
    arguments = ""
    if (level == "0") and (len(input_arr) > 2) and (input_arr[2] in ["INDI", "FAM"]):
        # Contains the ID for INDI or FAM
        arguments = input_arr[1]
        tag = input_arr[2]
    else:
        tag = input_arr[1]
        if len(input_arr) > 1:
            # Contains the arguments for other tags
            arguments = (" ".join(input_arr[2:])).strip()

    return {"level": level, "tag": tag, "arguments": arguments, "original": input_str}


def is_valid(cur_line, prev_line_tag):
    if (not cur_line["level"].isnumeric()) or (
        cur_line["level"] not in ["0", "1", "2"]
    ):
        print("error: 0 - Invalid level")
        return False

    if not cur_line["tag"] in list(valid_tags.keys()):
        print("error: 1 - Invalid tag")
        return False

    if cur_line["tag"] in ["INDI", "FAM", "HEAD", "TRLR", "NOTE"]:
        if cur_line["level"] != "0":
            print(f"error: 2 - The tag {cur_line['tag']} is required to be on level 0")
            return False
    elif cur_line["tag"] == "DATE":
        if not prev_line_tag in valid_tags[cur_line["tag"]]["belongs_to"]:
            print(
                f"error: 3 - The parent of this tag DATE does not match one of the required parents: {valid_tags[cur_line['tag']]['belongs_to']}"
            )
            return False
    else:
        if valid_tags[cur_line["tag"]]["belongs_to"] != prev_line_tag:
            print(
                f"error: 4 - The parent of this tag {cur_line['tag']} does not match the required parent of {valid_tags[cur_line['tag']]['belongs_to']}"
            )
            return False

    if valid_tags[cur_line["tag"]]["level"] != cur_line["level"]:
        print(
            f"error: 5 - The tag  {cur_line['tag']} does not have the correct level of  {valid_tags[cur_line['tag']]['level']}"
        )
        return False

    if cur_line["tag"] == "DATE":

        if (len(cur_line["arguments"]) < 1) or (cur_line["arguments"][0] == "0"):
            print(
                "error: 6 - Either no argument was provided or the date format contains a leading 0"
            )
            return False
        try:
            datetime.strptime(cur_line["arguments"], "%d %b %Y")
        except:
            print("error: 7 - The date does not follow the required format.")
            return False

    return True


filename = "simple_sample.ged"
if len(sys.argv) > 1:
    filename = sys.argv[1]
print(f"Reading from file: {filename}")

prev_result = {"level": "top level", "tag": "NOTE", "arguments": "-1"}
valid_letter = ""
input_list = []
with open(filename, "r") as fstream:
    for line in fstream:
        line = line.strip()
        result = parse_input(line)
        input_list.append(result)

for i, result in enumerate(input_list):
    if i == 0:
        input_list[i].update({"belongs_to": "top level"})
        continue
    cur_level = result["level"]
    prev_level = input_list[i - 1]["level"]
    x = 0
    while ((cur_level <= prev_level) or (input_list[i - 1 - x]["tag"] == "NOTE")) and (
        (i - 1 - x) >= 0
    ):
        x += 1
        prev_level = input_list[i - 1 - x]["level"]

    if (i - 1 - x) < 0:
        if cur_level == "0":
            input_list[i].update({"belongs_to": "top level"})
        else:
            input_list[i].update({"belongs_to": "Unknown"})
    else:
        input_list[i].update({"belongs_to": input_list[i - 1 - x]["tag"]})
    valid_status = is_valid(result, result["belongs_to"])
    valid_letter = "Y" if valid_status else "N"
    input_list[i].update({"is_valid": valid_letter})
    print(f"--> {result['original']}")
    print(
        f"<-- {result['level']} | {result['tag']} | {result['is_valid']} | {result['arguments']}"
    )
