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
		self.db_fam_col = self.database.create_collection(
			"family"
		)

		self.db_indi_col.create_index(["uid"], unique=True)
		self.db_indi_col.create_index(["NAME", "BIRT"], unique=True)
		errorFile = open("errors.txt", "w")
		errorFile.close()
		return super().setUpClass()

	def test_more_than_5_births(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 2025', 'original': '2 DATE 15 JUL 2025'},
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
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I05', 'original': '0 I05 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Damon /Smith/', 'original': '1 NAME Damon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 14 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I06', 'original': '0 I06 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brian /Smith/', 'original': '1 NAME Brian /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I07', 'original': '0 I07 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brendon /Smith/', 'original': '1 NAME Brendon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I08', 'original': '0 I08 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Derick /Smith/', 'original': '1 NAME Derick /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
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
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I05', 'original': '1 CHIL I05'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I06', 'original': '1 CHIL I06'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I07', 'original': '1 CHIL I07'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I08', 'original': '1 CHIL I08'},
		]
		find_parent(self.input_list)

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		birth_response = validate_multi_births(self.db_fam_col, self.db_indi_col)
		self.assertTrue(birth_response)

	def test_more_than_10_births(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 2025', 'original': '2 DATE 15 JUL 2025'},
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
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I05', 'original': '0 I05 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Damon /Smith/', 'original': '1 NAME Damon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 14 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I06', 'original': '0 I06 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brian /Smith/', 'original': '1 NAME Brian /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I07', 'original': '0 I07 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brendon /Smith/', 'original': '1 NAME Brendon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I08', 'original': '0 I08 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Derick /Smith/', 'original': '1 NAME Derick /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I09', 'original': '0 I09 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Shana /Smith/', 'original': '1 NAME Shana /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I10', 'original': '0 I10 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Hana /Smith/', 'original': '1 NAME Hana /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I11', 'original': '0 I11 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Natasha /Smith/', 'original': '1 NAME Natasha /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I12', 'original': '0 I12 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Valery /Smith/', 'original': '1 NAME Valery /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
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
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I05', 'original': '1 CHIL I05'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I06', 'original': '1 CHIL I06'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I07', 'original': '1 CHIL I07'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I08', 'original': '1 CHIL I08'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I09', 'original': '1 CHIL I09'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I10', 'original': '1 CHIL I10'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I11', 'original': '1 CHIL I11'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I12', 'original': '1 CHIL I12'},
		]
		find_parent(self.input_list)

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		birth_response = validate_multi_births(self.db_fam_col, self.db_indi_col)
		self.assertTrue(birth_response)

	def test_less_than_5_births(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 2025', 'original': '2 DATE 15 JUL 2025'},
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
			{'level': '2', 'tag': 'DATE', 'arguments': '13 MAR 1981', 'original': '2 DATE 13 MAR 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 JUN 1981', 'original': '2 DATE 13 JUN 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I05', 'original': '0 I05 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Damon /Smith/', 'original': '1 NAME Damon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 14 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I06', 'original': '0 I06 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brian /Smith/', 'original': '1 NAME Brian /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I07', 'original': '0 I07 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brendon /Smith/', 'original': '1 NAME Brendon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I08', 'original': '0 I08 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Derick /Smith/', 'original': '1 NAME Derick /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
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
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I05', 'original': '1 CHIL I05'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I06', 'original': '1 CHIL I06'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I07', 'original': '1 CHIL I07'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I08', 'original': '1 CHIL I08'},
		]
		find_parent(self.input_list)

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		birth_response = validate_multi_births(self.db_fam_col, self.db_indi_col)
		self.assertFalse(birth_response)

	def test_5_births(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 2025', 'original': '2 DATE 15 JUL 2025'},
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
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I05', 'original': '0 I05 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Damon /Smith/', 'original': '1 NAME Damon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 14 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I06', 'original': '0 I06 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brian /Smith/', 'original': '1 NAME Brian /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I07', 'original': '0 I07 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Brendon /Smith/', 'original': '1 NAME Brendon /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
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
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I05', 'original': '1 CHIL I05'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I06', 'original': '1 CHIL I06'},
			{'level': '1', 'tag': 'CHIL', 'arguments': 'I07', 'original': '1 CHIL I07'},
		]
		find_parent(self.input_list)

		self.indi_table = create_individual_table(self.input_list, valid_tags)
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		birth_response = validate_multi_births(self.db_fam_col, self.db_indi_col)
		self.assertFalse(birth_response)

	def test_only_2_births(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 2025', 'original': '2 DATE 15 JUL 2025'},
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
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
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
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		birth_response = validate_multi_births(self.db_fam_col, self.db_indi_col)
		self.assertFalse(birth_response)

	def test_mom_60_years_false(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1955', 'original': '2 DATE 15 JUL 1955'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
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
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 1981', 'original': '2 DATE 13 FEB 1981'},
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
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		parent_response = parent_age_check(self.db_fam_col, self.db_indi_col)
		self.assertFalse(parent_response)

	def test_mom_60_years_true(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1955', 'original': '2 DATE 15 JUL 1955'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
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
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
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
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		parent_response = parent_age_check(self.db_fam_col, self.db_indi_col)
		self.assertTrue(parent_response)
  
	def test_dad_80_years_true(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1955', 'original': '2 DATE 15 JUL 1955'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
			{'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1950', 'original': '2 DATE 23 SEP 1950'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
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
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		parent_response = parent_age_check(self.db_fam_col, self.db_indi_col)
		self.assertTrue(parent_response)
  
	def test_dad_80_years_false(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1950', 'original': '2 DATE 15 JUL 1950'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
			{'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1970', 'original': '2 DATE 23 SEP 1970'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
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
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		parent_response = parent_age_check(self.db_fam_col, self.db_indi_col)
		self.assertFalse(parent_response)
  
	def test_both_valid_age_range(self):

		self.input_list = [
			{'level': '0', 'tag': 'INDI', 'arguments': 'I01', 'original': '0 I01 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Joe /Smith/', 'original': '1 NAME Joe /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '15 JUL 1960', 'original': '2 DATE 15 JUL 1960'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
			{'level': '0', 'tag': 'NOTE', 'arguments': 'define Jennifer Smith', 'original': '0 NOTE define Jennifer Smith'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I02', 'original': '0 I02 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jennifer /Smith/', 'original': '1 NAME Jennifer /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '23 SEP 1970', 'original': '2 DATE 23 SEP 1970'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'F', 'original': '1 SEX F'},
			{'level': '1', 'tag': 'FAMS', 'arguments': 'F23', 'original': '1 FAMS F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I03', 'original': '0 I03 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Dick /Smith/', 'original': '1 NAME Dick /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
			{'level': '1', 'tag': 'SEX', 'arguments': 'M', 'original': '1 SEX M'},
			{'level': '1', 'tag': 'FAMC', 'arguments': 'F23', 'original': '1 FAMC F23'},
			{'level': '0', 'tag': 'INDI', 'arguments': 'I04', 'original': '0 I04 INDI'},
			{'level': '1', 'tag': 'NAME', 'arguments': 'Jane /Smith/', 'original': '1 NAME Jane /Smith/'},
			{'level': '1', 'tag': 'BIRT', 'arguments': '', 'original': '1 BIRT'},
			{'level': '2', 'tag': 'DATE', 'arguments': '13 FEB 2020', 'original': '2 DATE 13 FEB 2020'},
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
		self.fam_table = create_family_table(self.input_list, valid_tags, self.indi_table)
		db_insert(self.db_indi_col, self.indi_table)
		db_insert(self.db_fam_col, self.fam_table)

		parent_response = parent_age_check(self.db_fam_col, self.db_indi_col)
		self.assertFalse(parent_response)

	def tearDown(self) -> None:
		errorFile = open("errors.txt", "w")
		errorFile.close()
		self.client.drop_database("cs555_db_testing")
		return super().tearDown()

if __name__ == "__main__":
	unittest.main()
