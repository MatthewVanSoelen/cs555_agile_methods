import unittest
from helper import *


class Testing(unittest.TestCase):

	def setUp(self):
		# filename = "test_cases.ged"
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

	def test_invalid_death_true(self):
		self.input_list = [
		{"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
		{
			"level": "1",
			"tag": "NAME",
			"arguments": "Joe /Smith/",
			"original": "1 NAME Joe /Smith/",
		},
		{"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "31 DEC 2013",
			"original": "2 DATE 31 DEC 2013"
		},
		{"level": "1", "tag": "SEX", "arguments": "M", "original": "1 SEX M"},
			{ "level": "1",
			"tag": "DEAT",
			"arguments": "",
			"original": "1 DEAT"},
		{"level": "2",
			"tag": "DATE",
			"arguments": "15 JUL 1960",
			"original": "2 DATE 15 JUL 1960"},
			{"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
			{"level": "0", "tag": "FAM", "arguments": "F23", "original": "0 F23 FAM"},
		{
		"level": "1",
		"tag": "HUSB",
		"arguments": "I00",
		"original": "1 HUSB I00",
		}
			]
		find_parent(self.input_list)

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		db_insert(self.db_indi_col, self.indi_table)
		death_response = invalid_death(self.indi_table)
		self.assertTrue(death_response)

	def test_invalid_death_false(self):
		self.input_list = [
		{"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
		{
			"level": "1",
			"tag": "NAME",
			"arguments": "Joe /Smith/",
			"original": "1 NAME Joe /Smith/",
		},
		{"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "15 JUL 1960",
			"original": "2 DATE 15 JUL 1960"
		},
		{"level": "1", "tag": "SEX", "arguments": "M", "original": "1 SEX M"},
			{ "level": "1",
			"tag": "DEAT",
			"arguments": "",
			"original": "1 DEAT"},
		{"level": "2",
			"tag": "DATE",
			"arguments": "31 DEC 2013",
			"original": "2 DATE 31 DEC 2013"},
			{"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
			{"level": "0", "tag": "FAM", "arguments": "F23", "original": "0 F23 FAM"},
		{
		"level": "1",
		"tag": "HUSB",
		"arguments": "I00",
		"original": "1 HUSB I00",
		}
			]
		find_parent(self.input_list)

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		db_insert(self.db_indi_col, self.indi_table)
		death_response = invalid_death(self.indi_table)
		self.assertFalse(death_response)

	def test_invalid_marriage_true(self):
		self.input_list = [
		{"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
		{
			"level": "1",
			"tag": "NAME",
			"arguments": "Joe /Smith/",
			"original": "1 NAME Joe /Smith/",
		},
		{"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "15 JUL 1960",
			"original": "2 DATE 15 JUL 1960",
		},
		{"level": "1", "tag": "SEX", "arguments": "F", "original": "1 SEX F"},
		{"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
		{
			"level": "0",
			"tag": "INDI",
			"arguments": "I07",
			"original": "0 I07 INDI",
		},
		{
			"level": "1",
			"tag": "NAME",
			"arguments": "Jennifer /Smith/",
			"original": "1 NAME Jennifer /Smith/",
		},
		{
			"level": "1",
			"tag": "BIRT",
			"arguments": "",
			"original": "1 BIRT",
		},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "23 SEP 1960",
			"original": "2 DATE 23 SEP 1960",
		},
		{
			"level": "1",
			"tag": "SEX",
			"arguments": "F",
			"original": "1 SEX F",
		},
		{
			"level": "1",
			"tag": "FAMS",
			"arguments": "F23",
			"original": "1 FAMS F23",
		},
		{"level": "0", "tag": "FAM", "arguments": "F23", "original": "0 F23 FAM"},
		{
			"level": "1",
			"tag": "MARR",
			"arguments": "",
			"original": "1 MARR"
		},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "14 FEB 1930",
			"original": "2 DATE 14 FEB 1930"
		},
		{
			"level": "1",
			"tag": "HUSB",
			"arguments": "I00",
			"original": "1 HUSB I00",
		},
		{
			"level": "1",
			"tag": "WIFE",
			"arguments": "I07",
			"original": "1 WIFE I07",
		},
		]
		find_parent(self.input_list)
		# print(self.input_list)
		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		marriage_response = invalid_marriage(self.indi_table, self.fam_table)
		self.assertTrue(marriage_response)

	def test_invalid_marriage_false(self):
		self.input_list = [
		{"level": "0", "tag": "INDI", "arguments": "I00", "original": "0 I00 INDI"},
		{
			"level": "1",
			"tag": "NAME",
			"arguments": "Joe /Smith/",
			"original": "1 NAME Joe /Smith/",
		},
		{"level": "1", "tag": "BIRT", "arguments": "", "original": "1 BIRT"},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "15 JUL 1960",
			"original": "2 DATE 15 JUL 1960",
		},
		{"level": "1", "tag": "SEX", "arguments": "M", "original": "1 SEX M"},
		{"level": "1", "tag": "FAMS", "arguments": "F23", "original": "1 FAMS F23"},
		{
			"level": "0",
			"tag": "INDI",
			"arguments": "I07",
			"original": "0 I07 INDI",
		},
		{
			"level": "1",
			"tag": "NAME",
			"arguments": "Jennifer /Smith/",
			"original": "1 NAME Jennifer /Smith/",
		},
		{
			"level": "1",
			"tag": "BIRT",
			"arguments": "",
			"original": "1 BIRT",
		},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "23 SEP 1960",
			"original": "2 DATE 23 SEP 1960",
		},
		{
			"level": "1",
			"tag": "SEX",
			"arguments": "F",
			"original": "1 SEX F",
		},
		{
			"level": "1",
			"tag": "FAMS",
			"arguments": "F23",
			"original": "1 FAMS F23",
		},
		{"level": "0", "tag": "FAM", "arguments": "F23", "original": "0 F23 FAM"},
		{
			"level": "1",
			"tag": "MARR",
			"arguments": "",
			"original": "1 MARR"
		},
		{
			"level": "2",
			"tag": "DATE",
			"arguments": "14 FEB 1980",
			"original": "2 DATE 14 FEB 1980"
		},
		{
			"level": "1",
			"tag": "HUSB",
			"arguments": "I00",
			"original": "1 HUSB I00",
		},
		{
			"level": "1",
			"tag": "WIFE",
			"arguments": "I07",
			"original": "1 WIFE I07",
		},
		]
		find_parent(self.input_list)
		# print(self.input_list)
		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		marriage_response = invalid_marriage(self.indi_table, self.fam_table)
		self.assertFalse(marriage_response)

if __name__ == "__main__":
	unittest.main()
