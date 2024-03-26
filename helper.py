from datetime import datetime
from datetime import date
from prettytable import PrettyTable
import pymongo

def file_to_array(filename):
    input_list = []
    try:
        with open(filename, "r") as fstream:
            for line in fstream:
                line = line.strip()
                result = parse_input(line)
                input_list.append(result)
    except:
        print(f"Unable to open file: {filename}")
    return input_list


def read_error_file():
    input_list = []
    try:
        with open("errors.txt", "r") as fstream:
            for line in fstream:
                print(line, end="")
    except:
        print(f"Unable to open file error.txt")


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

        if (not get_date(cur_line["arguments"], validation_only=True)):
            print("error: 7 - The date does not follow the required format.")
            return False            

    return True


def find_parent(input_list):
    for i, result in enumerate(input_list):
        if i == 0:
            input_list[i].update({"belongs_to": "top level"})
            continue
        cur_level = result["level"]
        prev_level = input_list[i - 1]["level"]
        x = 0
        while (
            (cur_level <= prev_level) or (input_list[i - 1 - x]["tag"] == "NOTE")
        ) and ((i - 1 - x) >= 0):
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

def get_date(input_str, validation_only=False):
    # Accept multiple date formats (YYYY), (MMM, YYYY), (D MMM YYYY)
    for fmt in ("%d %b %Y", "%b %Y", "%Y"):
        try:
            if(validation_only):
                return True
            return datetime.strptime(input_str, fmt)
        except:
            pass
    if(validation_only):
        return False

    with open("errors.txt", "a") as errorFile:
        errorFile.write(f"Invalid Date Found: {input_str}. Substituing minimum date {datetime.min}")
    return datetime.min


def create_individual_table(input_list, valid_tags):
    indi_table = []

    for i, line in enumerate(input_list):
        if line["level"] == "0" and line["tag"] == "INDI":
            uid = line["arguments"]
            # check to see if the unique id already exists in indi_table
            uid_exists = any(d.get("uid") == uid for d in indi_table)
            # if it does then log the error
            if uid_exists:
                msg = "Error: INDIVIDUAL: US22: Unique ID already exists. Duplicate not allowed."
                with open("errors.txt", "a") as errorFile:
                    errorFile.write(f"{msg}\n")
                indi_table.append({"uid": uid})
                # continue
            else:
                indi_table.append({"uid": uid})
            x = i + 1
            while len(input_list) > x and input_list[x]["level"] != "0":
                if (input_list[x]["tag"] in valid_tags["DATE"]["belongs_to"]) and len(
                    input_list
                ) > x + 1:
                    indi_table[-1].update(
                        {input_list[x]["tag"]: input_list[x + 1]["arguments"]}
                    )
                    x += 1
                else:
                    indi_table[-1].update(
                        {input_list[x]["tag"]: input_list[x]["arguments"]}
                    )
                x += 1
            spouse = ""
            if "FAMS" in indi_table[-1].keys():
                spouse = indi_table[-1]["FAMS"]
            else:
                spouse = "NA"
            indi_table[-1].update({"FAMS": spouse})

            child = ""
            if "FAMC" in indi_table[-1].keys():
                child = indi_table[-1]["FAMC"]
            else:
                child = "NA"
            indi_table[-1].update({"FAMC": child})

            death = ""
            if "DEAT" in indi_table[-1].keys():
                death = indi_table[-1]["DEAT"]
            else:
                death = "NA"
            indi_table[-1].update({"DEAT": death})

            alive = ""
            if death == "NA":
                alive = True
            else:
                alive = False
            indi_table[-1].update({"ALIVE": alive})

            age = ""
            if "BIRT" in indi_table[-1].keys():
                if indi_table[-1]["DEAT"] != "NA":
                    death = get_date(indi_table[-1]["DEAT"])
                    age = ( death.year - get_date(indi_table[-1]["BIRT"]).year )
                else:
                    today = date.today()
                    age = ( today.year - get_date(indi_table[-1]["BIRT"]).year )
                # if age < 0:
                #     age = "NA"
            else:
                age = -100
            indi_table[-1].update({"AGE": age})

    return indi_table


def create_family_table(input_list, valid_tags, indi_table):
    fam_table = []

    for i, line in enumerate(input_list):
        if line["level"] == "0" and line["tag"] == "FAM":
            uid = line["arguments"]
            fam_table.append({"uid": uid})
            x = i + 1

            while len(input_list) > x and input_list[x]["level"] != "0":
                if (input_list[x]["tag"] in valid_tags["DATE"]["belongs_to"]) and len(
                    input_list
                ) > x + 1:
                    fam_table[-1].update(
                        {input_list[x]["tag"]: input_list[x + 1]["arguments"]}
                    )
                    x += 1
                else:
                    fam_table[-1].update(
                        {input_list[x]["tag"]: input_list[x]["arguments"]}
                    )
                x += 1
            marriage = ""
            if "MARR" in fam_table[-1].keys():
                marriage = fam_table[-1]["MARR"]
            else:
                marriage = "NA"
            fam_table[-1].update({"MARR": marriage})

            divorce = ""
            if "DIV" in fam_table[-1].keys():
                divorce = fam_table[-1]["DIV"]
            else:
                divorce = "NA"
            fam_table[-1].update({"DIV": divorce})

            husb_name = next(
                person
                for person in indi_table
                if person["uid"] == fam_table[-1]["HUSB"]
            )["NAME"]
            if not husb_name:
                husb_name = "NA"
            fam_table[-1].update({"HUSB_NAME": husb_name})

            wife_name = next(
                person
                for person in indi_table
                if person["uid"] == fam_table[-1]["WIFE"]
            )["NAME"]
            if not wife_name:
                wife_name = "NA"
            fam_table[-1].update({"WIFE_NAME": wife_name})

            children = list(
                filter(lambda child: child["FAMC"] == fam_table[-1]["uid"], indi_table)
            )
            
            if len(children) < 1:
                children = "NA"
            else:
                children = sorted(children, key=lambda e: e['AGE'], reverse=True)
                for i, child in enumerate(children):
                    children[i] = child["uid"]
            fam_table[-1].update({"CHILDREN": children})

    return fam_table

def create_pretty_indi_table(db_collection):
    indi_pretty = PrettyTable()
    indi_pretty.field_names = [
        "ID",
        "Name",
        "Gender",
        "Birthday",
        "Age",
        "Alive",
        "Death",
        "Child",
        "Spouse",
    ]

    for person in db_collection.find():
        indi_pretty.add_row(
            [
                person["uid"],
                person["NAME"],
                person["SEX"],
                person["BIRT"],
                person["AGE"],
                person["ALIVE"],
                person["DEAT"],
                person["FAMC"],
                person["FAMS"],
            ]
        )
    return indi_pretty


def create_pretty_fam_table(db_collection):
    fam_pretty = PrettyTable()
    fam_pretty.field_names = [
        "ID",
        "Married",
        "Divorced",
        "Husband ID",
        "Husband Name",
        "Wife ID",
        "Wife Name",
        "Children",
    ]

    for person in db_collection.find():
        fam_pretty.add_row(
            [
                person["uid"],
                person["MARR"],
                person["DIV"],
                person["HUSB"],
                person["HUSB_NAME"],
                person["WIFE"],
                person["WIFE_NAME"],
                person["CHILDREN"],
            ]
        )
    return fam_pretty


def db_insert(db_collection, data_table):
    for row in data_table:
        try:
            result = db_collection.insert_one(row)
        except pymongo.errors.DuplicateKeyError as error:
            msg = ""
            if "NAME_1_BIRT_1" in str(error):
                msg = "Error: INDIVIDUAL: US23: No more than one individual with the same name and birth date should appear in a GEDCOM file"
            elif "uid" in str(error):
                msg = "Error: INDIVIDUAL: US22: No more than one individual with the same unique ID should appear in a GEDCOM file"

            with open("errors.txt", "a") as errorFile:
                errorFile.write(msg)
            continue
        except pymongo.errors.WriteError as error:
            msg = ""
            if "AGE" in str(error):
                msg = "Error: INDIVIDUAL: US27: Include person's current age when listing individuals"

            with open("errors.txt", "a") as errorFile:
                errorFile.write(f"{msg}\n")
            continue


def list_all_deceased(indi_table):
    deceased_list = []
    for person in indi_table:
        curr_name = person["NAME"]
        curr_alive = person["ALIVE"]
        if curr_alive == False:
            deceased_list.append(curr_name)
    with open("errors.txt", "a") as errorFile:
        errorFile.write(f"\nList of all deceased individuals US29: \n")
        errorFile.write(f"{deceased_list}\n")
    return deceased_list
    # print("List of all deceased individuals: ")
    # print(deceased_list)


def detect_duplicate_uid(indi_table):
    seen_uids = set()
    for d in indi_table:
        uid = d.get("uid")
        if uid in seen_uids:
            return True  # Found a duplicate uid
        seen_uids.add(uid)
    return False  # No duplicate uid found


# us07: Less than 150 Years Old
def check_age(indi_table):
    over_150 = False
    for person in indi_table:
        # check if a person lived for 150 years or older
        if type(person['AGE']) is int and person["AGE"] >= 150 and person["ALIVE"] == False:
            name = person["NAME"]
            uid = person["uid"]
            age = str(person["AGE"])
            msg = ("Error: INDIVIDUAL: US07: Age of individual after death is 150 or greater, please check birth and death date: " + name + "(" + uid + ") died at age: " + age)
            with open("errors.txt", "a") as errorFile:
                errorFile.write(msg + "\n")
            over_150 = True
            # check if a person is currently 150 years or older
        if type(person['AGE']) is int and person["AGE"] >= 150 and person["ALIVE"] == True:
            name = person["NAME"]
            uid = person["uid"]
            age = str(person["AGE"])
            msg = (
                "Error: INDIVIDUAL: US07: Current age of individual is 150 or greater, please check birthdate: "
                + name
                + "("
                + uid
                + ") is currently: "
                + age
                + " years old"
            )
            with open("errors.txt", "a") as errorFile:
                errorFile.write(msg + "\n")
            over_150 = True
    return over_150


# us21: Correct gender for role
def check_wife_gender(indi_table, fam_table):

    wife = False

    wife_gender = "F"
    for person in indi_table:
        # check indivdual against family table to see if they have wife tag
        if person["uid"] == fam_table[-1]["WIFE"]:
            name = person["NAME"]
            uid = person["uid"]
            indi_gender = person["SEX"]
            # check if gender was set to F for the wife
            if person["SEX"] != wife_gender:
                wife = False
                msg = (
                    "Error: FAMILY: US21: Incorrect gender has been used for the wife: "
                    + name
                    + "("
                    + uid
                    + "): Current Gender Set to "
                    + indi_gender
                    + " - should be set to "
                    + wife_gender
                )
                with open("errors.txt", "a") as errorFile:
                    errorFile.write(msg + "\n")
            else:
                wife = True
    if wife == True:
        return True
    else:
        return False

# us01: Dates (birth, marriage, divorce, death) should not be after the current date
def no_dates_after_current(people_collection, families_collection):
    #get today's date to compare our other dates to
    #use datetime.now to match the datetime.datetime format that is being used in the return of the get_date function
    today = datetime.now()

    for family in families_collection.find():
        keys = family.keys()
        if("DIV" in keys and family['DIV'] != "NA"):
            div_date = get_date(family["DIV"])
            if(today < div_date):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US01: DIV occurs after current date\n")
        if("MARR" in keys and family['MARR'] != "NA"):
            marr_date = get_date(family["MARR"])
            if(today < marr_date):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US01: MARR occurs after current date\n")
    
    for people in people_collection.find():
        keys = people.keys()
        if("BIRT" in keys and people['BIRT'] != "NA"):
            birth_date = get_date(people["BIRT"])
            if(today < birth_date):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US01: BIRT occurs after current date\n")
        if("DEAT" in keys and people['DEAT'] != "NA"):
            death_date = get_date(people["DEAT"])
            if(today < death_date):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US01: DEAT occurs after current date\n")

# us10: Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
def no_marriage_before_14(people_collection):
    #get today's date to compare our other dates to
    #use datetime.now to match the datetime.datetime format that is being used in the return of the get_date function
    today = datetime.now()

    for people in people_collection.find():
        keys = people.keys()
        if("FAMS" in keys and people['FAMS'] != "NA"):
            age = people["AGE"]
            if(age < 14):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US10: Married Individual is younger than 14\n")

# us25: No more than one child with the same name and birth date should appear in a family
def unique_name_and_birthdates(people_collection):
    seen = set()
    for people in people_collection.find():
        if(people['FAMC'] == "NA"):
            continue
        name = people["NAME"]
        birthdate = people["BIRT"]
        family = people["FAMC"]
        key = (name, birthdate, family)
        if key in seen:
            with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US25: a child in a family has a duplicate name and birthday\n")
        seen.add(key)

# us06: Divorce can only occur before death of both spouses
def checkDiv_Deat(people_collection, families_collection):
    for family in families_collection.find():
        keys = family.keys()
        if ("DIV" not in keys or family['DIV'] == "NA"):
            continue
        div_date = get_date(family["DIV"])
        husb = people_collection.find_one({"uid":family["HUSB"]})
        wife = people_collection.find_one({"uid":family["WIFE"]})
        if (husb["DEAT"] == "NA" and wife["DEAT"] == "NA"):
            continue
        if (husb["DEAT"] != "NA"):
            husb_deat_date = get_date(husb["DEAT"])
            if(husb_deat_date < div_date):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US06: Husband died before divorce\n")

        if (wife["DEAT"] != "NA"):
            wife_deat_date = get_date(wife["DEAT"])
            if(wife_deat_date < div_date):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US06: Wife died before divorce\n")

# us21: Correct gender for role
def check_husband_gender(indi_table, fam_table):
    husband = False
    husband_gender = "M"
    for person in indi_table:
        # check indivdual against family table to see if they have husband tag
        if person["uid"] == fam_table[-1]["HUSB"]:
            name = person["NAME"]
            uid = person["uid"]
            indi_gender = person["SEX"]
            # check if gender was set to M for the husband
            if person["SEX"] != husband_gender:
                husband = False
                msg = (
                    "Error: FAMILY: US21: Incorrect gender has been used for the husband: "
                    + name
                    + "("
                    + uid
                    + "): Current Gender Set to "
                    + indi_gender
                    + " - should be set to "
                    + husband_gender
                )
                with open("errors.txt", "a") as errorFile:
                    errorFile.write(msg + "\n")
            else:
                husband = True
    if husband == True:
        return True
    else:
        return False

# us02: Birth Before Marriage - check that married individuals were born before they got married
def invalid_marriage(indi_table, fam_table):
	invalid = False
	for person in indi_table:
		if person['uid'] == fam_table[-1]["WIFE"] or person['uid'] == fam_table[-1]['HUSB']:
			marriage = str(get_date(fam_table[-1]["MARR"]))
			birth = str(get_date(person["BIRT"]))
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
			death = str(get_date(person["DEAT"]))
		birth = str(get_date(person["BIRT"]))
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


# us33: List all orphaned children (both parents dead and child < 18 years old) in a GEDCOM file
def list_all_orphans(people_collection, families_collection):

    with open("errors.txt", "a") as errorFile:
        errorFile.write("\nList of all orphaned individuals US33:" + "\n")

    for family in families_collection.find():
        # check if there are any children in the family. If no there cannot be any orphans so move to the next family.
        if len(family["CHILDREN"]) == 0:
            continue

        father_id = family["HUSB"]
        mother_id = family["WIFE"]
        if (people_collection.find_one({"uid": father_id})["ALIVE"] == True or people_collection.find_one({"uid": mother_id})["ALIVE"] == True ):
            continue
        
        for child_id in family["CHILDREN"]:
            child = people_collection.find_one({"uid": child_id})
            if(child["AGE"] < 18):
                with open("errors.txt", "a") as errorFile:
                    errorFile.write(f"{child['uid']} - {child['NAME']} \n")

    return True

# us04: Marriage should occur before divorce of spouses, and divorce can only occur after marriage
def checkDiv_Marr(families_collection):
    for family in families_collection.find():
        keys = family.keys()
        if("DIV" in keys and family['DIV'] != "NA" and "MARR" in keys and family['MARR'] == "NA"):
            with open("errors.txt", "a") as errorFile:
                    errorFile.write(f"Error: US04: DIV present without MARR\n")
        if ("MARR" not in keys):
            continue
        if("DIV" not in keys or family['DIV'] == "NA"):
            continue
        marr_date = get_date(family["MARR"])
        div_date = get_date(family["DIV"])

        if(div_date < marr_date):
            with open("errors.txt", "a") as errorFile:
                    errorFile.write(f"Error: US04: DIV before MARR\n")

# us05: Marriage should occur before death of either spouse
def checkMarr_Deat(people_collection, families_collection):
    for family in families_collection.find():
        keys = family.keys()
        if ("MARR" not in keys or family['MARR'] == "NA"):
            continue
        marr_date = get_date(family["MARR"])
        husb = people_collection.find_one({"uid":family["HUSB"]})
        wife = people_collection.find_one({"uid":family["WIFE"]})
        if (husb["DEAT"] == "NA" and wife["DEAT"] == "NA"):
            continue
        if (husb["DEAT"] != "NA"):
            husb_deat_date = get_date(husb["DEAT"])
            if(husb_deat_date < marr_date):
                with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US05: Husband died before marrage\n")

        if (wife["DEAT"] != "NA"):
            wife_deat_date = get_date(wife["DEAT"])
            if(wife_deat_date < marr_date):
                with open("errors.txt", "a") as errorFile:
                    errorFile.write(f"Error: US05: Wife died before marrage\n")

def check_male_last_names(people_collection, families_collection):
    for family in families_collection.find():
        full_name = people_collection.find_one({"uid":family["HUSB"]})["NAME"]
        last_name = full_name.split(" ")
        if len(last_name) > 1:
            last_name = last_name[1]
        else:
            with open("errors.txt", "a") as errorFile:
                errorFile.write(f"Error: US16: Husband has no last name \n")
                return
        for child_id in family["CHILDREN"]:
            child = people_collection.find_one({"uid":child_id})
            if(child["SEX"] != "M"):
                continue
            child_last_name = child["NAME"]
            child_last_name = child_last_name.split(" ")
            if len(last_name) > 1:
                child_last_name = child_last_name[1]
                if (last_name != child_last_name):
                    with open("errors.txt", "a") as errorFile:
                        errorFile.write(f"Error: US16: Child last name does not match father's last name \n")
            else:
                with open("errors.txt", "a") as errorFile:
                    errorFile.write(f"Error: US16: Child has no last name \n")


def print_ordered_children(people_collection, families_collection):

    for family in families_collection.find():
        if(family["CHILDREN"] == "NA"): 
            return "NA"
        children_pretty_table = PrettyTable()
        children_pretty_table.field_names = [
            "CHILD_ID",
            "CHILD_NAME",
            "CHILD_AGE"
        ]
        print(f"Family: {family['uid']}")
        for child_id in family["CHILDREN"]:
            child = people_collection.find_one({"uid":child_id})
            children_pretty_table.add_row(
            [
                child["uid"],
                child["NAME"],
                child["AGE"]
            ]
        )
        print(children_pretty_table)
    return children_pretty_table


people_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "additionalProperties": True,
        "required": [
            "uid",
            "NAME",
            "BIRT",
            "SEX",
            "FAMS",
            "DEAT",
            "FAMC",
            "ALIVE",
            "AGE",
        ],
        "properties": {"AGE": {"bsonType": "int"}},
    }
}

family_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        # "additionalProperties": True,
        # "required": [
        #     "uid",
        #     "MARR",
        #     "HUSB",
        #     "WIFE",
        #     "CHIL",
        #     "DIV",
        #     "HUS_NAME",
        #     "WIFE_NAME",
        #     "CHILDREN",
        # ],
        # "properties": {"AGE": {"bsonType": "int"}},
    }
}

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
