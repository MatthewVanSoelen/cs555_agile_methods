import unittest

from helper import *


# Use Case 27: Must Include Individual Ages
class Test_US_27(unittest.TestCase):
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
        return super().setUpClass()

    def test_ValidAge(self):

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
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)
        person = self.db_indi_col.find_one({"uid": "I00"})
        self.assertTrue("AGE" in person.keys())
        self.assertIsInstance(person["AGE"], int)

    def test_ValidAge2(self):

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
        person = self.db_indi_col.find_one({"uid": "I01"})
        self.assertTrue("AGE" in person.keys())
        self.assertIsInstance(person["AGE"], int)

    def test_InvalidAge(self):

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
                "arguments": "23 SEP 1960",
                "original": "2 DATE 23 SEP 1959",
            },
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)
        person = self.db_indi_col.find_one({"uid": "I02"})
        self.assertTrue("AGE" in person.keys())
        self.assertIsInstance(person["AGE"], int)

    def test_MissingBirthDate(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I03", "original": "0 I03 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jennifer /Smith/",
                "original": "1 NAME Jennifer /Smith/",
            },
            {"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
            {"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
            {"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
        ]

        find_parent(self.input_list)
        with self.assertRaises(ValueError):
            self.indi_table = create_individual_table(self.input_list, valid_tags)

    def test_MissingBirth(self):

        self.input_list = [
            {"level": "0", "tag": "INDI", "arguments": "I04", "original": "0 I04 INDI"},
            {
                "level": "1",
                "tag": "NAME",
                "arguments": "Jennifer /Smith/",
                "original": "1 NAME Jennifer /Smith/",
            },
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
        with self.assertRaises(pymongo.errors.WriteError):
            db_insert(self.db_indi_col, self.indi_table)

    # self.assertRaises(pymongo.errors.DuplicateKeyError)

    @classmethod
    def tearDownClass(self):
        self.client.drop_database("cs555_db_testing")
        return super().tearDown(self)


if __name__ == "__main__":
    unittest.main()
