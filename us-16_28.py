import unittest

from helper import *
import pdb
import numpy as np
import re


# Use Case 16: All male members of a family should have the same last name
class Test_US_16(unittest.TestCase):
    def setUp(self) -> None:
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.client.drop_database("cs555_db_testing")
        self.database = self.client["cs555_db_testing"]

        self.db_indi_col = self.database.create_collection(
            "people", validator=people_schema
        )

        self.db_indi_col.create_index(["uid"], unique=True)
        self.db_indi_col.create_index(["NAME", "BIRT"], unique=True)

        self.db_fam_col = self.database.create_collection("families", validator=family_schema)
        self.db_fam_col.create_index(["uid"], unique=True)

        errorFile = open("errors.txt", "w")
        errorFile.close()
        return super().setUp()

    def test_ValidInput(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '2 JUN 1983', 'original': '2 DATE 2 JUN 1983'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)

        check_male_last_names(self.db_indi_col, self.db_fam_col)

        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US16:" in line):
                    self.assertTrue(False)
                    return
            self.assertTrue(True) 

    def test_ValidInput_Daugther_diff_name(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jane Shawn', 'original': '1 NAME Jane Shawn'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '2 JUN 1983', 'original': '2 DATE 2 JUN 1983'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)

        check_male_last_names(self.db_indi_col, self.db_fam_col)

        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US16:" in line):
                    self.assertTrue(False)
                    return
            self.assertTrue(True) 

    def test_ValidInput_Son_diff_name(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick Shawn', 'original': '1 NAME Dick Shawn'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '2 JUN 1983', 'original': '2 DATE 2 JUN 1983'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)

        check_male_last_names(self.db_indi_col, self.db_fam_col)
        with open("errors.txt", "r") as fstream:
            for line in fstream:
                print(line)
                if("US16:" in line):
                    self.assertTrue(True)
                    return
            self.assertTrue(False) 

    def test_ValidInput_Son2_diff_name(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick Shawn', 'original': '1 NAME Dick Shawn'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jake Shawn', 'original': '1 NAME Jake Shawn'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '2 JUN 1983', 'original': '2 DATE 2 JUN 1983'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)

        check_male_last_names(self.db_indi_col, self.db_fam_col)
        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US16:" in line):
                    self.assertTrue(True)
                    return
            self.assertTrue(False) 

    
    def tearDown(self) -> None:
        errorFile = open("errors.txt", "w")
        errorFile.close()
        self.client.drop_database("cs555_db_testing")
        return super().tearDown()

# Use Case 28: List siblings in families by decreasing age, i.e. oldest siblings first
class Test_US_28(unittest.TestCase):
    def setUp(self) -> None:
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.client.drop_database("cs555_db_testing")
        self.database = self.client["cs555_db_testing"]

        self.db_indi_col = self.database.create_collection(
            "people", validator=people_schema
        )

        self.db_indi_col.create_index(["uid"], unique=True)
        self.db_indi_col.create_index(["NAME", "BIRT"], unique=True)

        self.db_fam_col = self.database.create_collection("families", validator=family_schema)
        self.db_fam_col.create_index(["uid"], unique=True)

        errorFile = open("errors.txt", "w")
        errorFile.close()
        return super().setUp()

    def test_Order1(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '2 JUN 1983', 'original': '2 DATE 2 JUN 1983'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)
        result_table = print_ordered_children(self.db_indi_col, self.db_fam_col)
        if result_table == "NA":
            self.assertTrue(True)
            return
        temp = np.array(re.split(',|\\r\\n', result_table.get_formatted_string('csv')))[:-1]
        temp = np.reshape(temp, (-1, 3))[:,2][1:]
        temp = temp.astype(int)
        temp = np.flip(temp)
        self.assertTrue(all(a <= b for a, b in zip(temp, temp[1:])))

    def test_Order2(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1985', 'original': '2 DATE 13 FEB 1985'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '2 JUN 1983', 'original': '2 DATE 2 JUN 1983'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)
        result_table = print_ordered_children(self.db_indi_col, self.db_fam_col)
        if result_table == "NA":
            self.assertTrue(True)
            return
        temp = np.array(re.split(',|\\r\\n', result_table.get_formatted_string('csv')))[:-1]
        temp = np.reshape(temp, (-1, 3))[:,2][1:]
        temp = temp.astype(int)
        temp = np.flip(temp)
        self.assertTrue(all(a <= b for a, b in zip(temp, temp[1:])))

    def test_Same_Age(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1985', 'original': '2 DATE 13 FEB 1985'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '2 JUN 1985', 'original': '2 DATE 2 JUN 1985'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)
        result_table = print_ordered_children(self.db_indi_col, self.db_fam_col)
        if result_table == "NA":
            self.assertTrue(True)
            return
        temp = np.array(re.split(',|\\r\\n', result_table.get_formatted_string('csv')))[:-1]
        temp = np.reshape(temp, (-1, 3))[:,2][1:]
        temp = temp.astype(int)
        temp = np.flip(temp)
        self.assertTrue(all(a <= b for a, b in zip(temp, temp[1:])))

    def test_one_child(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1985', 'original': '2 DATE 13 FEB 1985'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)
        result_table = print_ordered_children(self.db_indi_col, self.db_fam_col)
        if result_table == "NA":
            self.assertTrue(True)
            return
        temp = np.array(re.split(',|\\r\\n', result_table.get_formatted_string('csv')))[:-1]
        temp = np.reshape(temp, (-1, 3))[:,2][1:]
        temp = temp.astype(int)
        temp = np.flip(temp)
        self.assertTrue(all(a <= b for a, b in zip(temp, temp[1:])))

    def test_zero_children(self):

        self.input_list = [
            {'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '1', 'tag': 'DEAT', 'arguments': '', 'original': '1 DEAT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '31 DEC 2013', 'original': '2 DATE 31 DEC 2013'},
            {'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
            {'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
            {'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
            {'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
            {'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1960', 'original': '2 DATE 23 SEP 1960'},
            {'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
            {'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
            {'level': '0', 'tag': 'FAM', 'arguments': 'F23', 'original': '0 F23 FAM'},
            {'level': '1', 'tag': 'MARR', 'arguments': '', 'original': '1 MARR'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1980', 'original': '2 DATE 14 FEB 1980'},
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1990', 'original': '2 DATE 14 FEB 1990'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)
        db_insert(self.db_indi_col, self.indi_table)

        self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
        db_insert(self.db_fam_col, self.fam_table)
        result_table = print_ordered_children(self.db_indi_col, self.db_fam_col)
        if result_table == "NA":
            self.assertTrue(True)
            return
        temp = np.array(re.split(',|\\r\\n', result_table.get_formatted_string('csv')))[:-1]
        temp = np.reshape(temp, (-1, 3))[:,2][1:]
        temp = temp.astype(int)
        temp = np.flip(temp)
        self.assertTrue(all(a <= b for a, b in zip(temp, temp[1:])))

    def tearDown(self) -> None:
        errorFile = open("errors.txt", "w")
        errorFile.close()
        self.client.drop_database("cs555_db_testing")
        return super().tearDown()
    
if __name__ == "__main__":
    unittest.main()
