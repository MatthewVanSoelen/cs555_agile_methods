import unittest
from us07_21 import check_age, check_wife_gender, check_husband_gender
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

	# def tearDown(self):
	#    self.testfile.close()

	def test_husband_gender_false(self):
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
		gender_response = check_husband_gender(self.indi_table, self.fam_table)
		self.assertFalse(gender_response)

	def test_husband_gender_true(self):
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

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		husband_response = check_husband_gender(self.indi_table, self.fam_table)
		self.assertTrue(husband_response)

	def test_wife_gender_true(self):
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

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		wife_response = check_wife_gender(self.indi_table, self.fam_table)
		self.assertTrue(wife_response)

	def test_wife_gender_false(self):
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
			"arguments": "M",
			"original": "1 SEX M",
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

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		wife_response = check_wife_gender(self.indi_table, self.fam_table)
		self.assertFalse(wife_response)

	def test_both_gender_true(self):
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

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		wife_response = check_wife_gender(self.indi_table, self.fam_table)
		husband_response = check_husband_gender(self.indi_table, self.fam_table)
		self.assertTrue(wife_response)
		self.assertTrue(husband_response)

	def test_dead_over150(self):
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
		{"level": "0", "tag": "FAM", "arguments": "F23", "original": "0 F23 FAM"},
		{
			"level": "1",
			"tag": "HUSB",
			"arguments": "I00",
			"original": "1 HUSB I00",
		},
		]
		find_parent(self.input_list)

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		age_response = check_age(self.indi_table)
		self.assertFalse(age_response)


if __name__ == "__main__":
	unittest.main()
