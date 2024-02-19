import unittest

from helper import *


# Use Case 29: List all deceased individuals in a GEDCOM file
class Test_US_29(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.client.drop_database("cs555_db_testing")
        self.database = self.client["cs555_db_testing"]

        self.db_indi_col = self.database.create_collection(
            "people", validator=people_schema
        )

        self.db_indi_col.create_index(["uid"], unique=True)
        self.db_indi_col.create_index(["NAME", "BIRT"], unique=True)
        errorFile = open("errors.txt", "w")
        errorFile.close()
        return super().setUpClass()

    def test_Valid_Deceased1(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Cameron /Sonn/",
                "original": "1 NAME Cameron /Sonn/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)
        #print(self.indi_table)
        deceased = list_all_deceased(self.indi_table)
        with open("errors.txt", "r") as errorFile:
             self.assertTrue("List of all deceased individuals US29: " in errorFile.read())
        self.assertTrue(len(deceased) == 0)

    def test_Valid_Deceased2(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I01", "original": "0 I01 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "May /Smith/",
                "original": "1 NAME May /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "DEAT", "arguments": "", "original": "1 DEAT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)
        deceased = list_all_deceased(self.indi_table)
        with open("errors.txt", "r") as errorFile:
             self.assertTrue("List of all deceased individuals US29: " in errorFile.read())
        self.assertTrue("May /Smith/" in deceased)

    def test_Valid_Deceased3(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I02", "original": "0 I02 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Sarah /Smith/",
                "original": "1 NAME May /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "DEAT", "arguments": "", "original": "1 DEAT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1959",
                "original": "2 DATE 23 SEP 1959",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)
        deceased = list_all_deceased(self.indi_table)
        with open("errors.txt", "r") as errorFile:
             self.assertTrue("List of all deceased individuals US29: " in errorFile.read())
        self.assertTrue("Sarah /Smith/" in deceased)

    def test_NoBirthDate(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I02", "original": "0 I02 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Maggie /Marson/",
                "original": "1 NAME Maggie /Marson/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F27", "original": "1 FAMS F27"},
        ]

        find_parent(self.input_list)
        with self.assertRaises(ValueError):
            self.indi_table = create_individual_table(self.input_list, valid_tags)
    
    def test_Multiple_Deceased(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I02", "original": "0 I02 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Sarah /Smith/",
                "original": "1 NAME May /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "DEAT", "arguments": "", "original": "1 DEAT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1959",
                "original": "2 DATE 23 SEP 1959",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},

            {"level": "0", "tag": "INDI", "arguments": "I01", "original": "0 I01 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "May /Smith/",
                "original": "1 NAME May /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "DEAT", "arguments": "", "original": "1 DEAT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)
        deceased = list_all_deceased(self.indi_table)
        with open("errors.txt", "r") as errorFile:
             self.assertTrue("List of all deceased individuals US29: " in errorFile.read())
        self.assertTrue("Sarah /Smith/" in deceased)
        self.assertTrue("May /Smith/" in deceased)


# Use Case 22: All individual IDs should be unique and all family IDs should be unique
class Test_US_22(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.client.drop_database("cs555_db_testing")
        self.database = self.client["cs555_db_testing"]

        self.db_indi_col = self.database.create_collection(
            "people", validator=people_schema
        )

        self.db_indi_col.create_index(["uid"], unique=True)
        self.db_indi_col.create_index(["NAME", "BIRT"], unique=True)

        errorFile = open("errors.txt", "w")
        errorFile.close()
        return super().setUpClass()

    def test_Unique_UID(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jennifer /Smith/",
                "original": "1 NAME Jennifer /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
            {"level": "0", "tag": "INDI", "arguments": "I01", "original": "0 I01 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jeff /Smith/",
                "original": "1 NAME Jeff /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1964",
                "original": "2 DATE 23 SEP 1964",
            },
            {"level": "1", "tag": "SEX", "arguments": "M", "original": "1 SEX M"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        self.indi_table = create_individual_table(self.input_list, valid_tags)
        self.assertFalse(detect_duplicate_uid(self.indi_table))

    def test_Unique_UID2(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jennifer /Smith/",
                "original": "1 NAME Jennifer /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I01 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jeff /Smith/",
                "original": "1 NAME Jeff /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1964",
                "original": "2 DATE 23 SEP 1964",
            },
            {"level": "1", "tag": "SEX", "arguments": "M", "original": "1 SEX M"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        self.indi_table = create_individual_table(self.input_list, valid_tags)
        self.assertTrue(detect_duplicate_uid(self.indi_table))

    def test_Unique_UID3(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jennifer /Smith/",
                "original": "1 NAME Jennifer /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I01 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jeff /Smith/",
                "original": "1 NAME Jeff /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1964",
                "original": "2 DATE 23 SEP 1964",
            },
            {"level": "1", "tag": "SEX", "arguments": "M", "original": "1 SEX M"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
        ]

        self.indi_table = create_individual_table(self.input_list, valid_tags)
        self.assertTrue(detect_duplicate_uid(self.indi_table))

    def test_Unique_UID4(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "", "original": "0 I00 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jennifer /Smith/",
                "original": "1 NAME Jennifer /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
            {"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I01 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jeff /Smith/",
                "original": "1 NAME Jeff /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1964",
                "original": "2 DATE 23 SEP 1964",
            },
            {"level": "1", "tag": "SEX", "arguments": "M", "original": "1 SEX M"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
            {"level": "0", "tag": "INDI", "arguments": "I09", "original": "0 I00 INDI"},
        ]

        self.indi_table = create_individual_table(self.input_list, valid_tags)
        self.assertFalse(detect_duplicate_uid(self.indi_table))

    def test_Unique_UID5(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "", "original": "0 I00 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jennifer /Smith/",
                "original": "1 NAME Jennifer /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {
                "level": "2",
                "tag": "DATE",
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1960",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        self.indi_table = create_individual_table(self.input_list, valid_tags)
        self.assertFalse(detect_duplicate_uid(self.indi_table))

    @classmethod
    def tearDownClass(self):
        self.client.drop_database("cs555_db_testing")
        return super().tearDown(self)


if __name__ == "__main__":
    unittest.main()
