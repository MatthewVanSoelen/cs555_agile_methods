import unittest

from helper import *


# Use Case 04: Marriage should occur before divorce of spouses, and divorce can only occur after marriage
class Test_US_04(unittest.TestCase):
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

        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US04:" in line):
                    self.assertTrue(False)
            self.assertTrue(True)

    def test_ValidDivBeforeMarr_1(self):

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
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1970', 'original': '2 DATE 14 FEB 1970'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)

        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US04:" in line):
                    self.assertTrue(True)
            self.assertTrue(False)

    def test_ValidDivBeforeMarr_2(self):

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
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1979', 'original': '2 DATE 14 FEB 1979'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)

        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US04:" in line):
                    self.assertTrue(True)
            self.assertTrue(False)


    def test_ValidDivwithoputMarr_1(self):

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
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1979', 'original': '2 DATE 14 FEB 1979'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)

        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US04:" in line):
                    self.assertTrue(True)
            self.assertTrue(False)

    def test_ValidDivwithoputMarr_2(self):

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
            {'level': '1', 'tag': 'DIV', 'arguments': '', 'original': '1 DIV'},
            {'level': '2', 'tag': 'DATE', 'arguments': '14 FEB 1979', 'original': '2 DATE 14 FEB 1979'},
            {'level': '1', 'tag': 'HUSB', 'arguments': 'I01', 'original': '1 HUSB I01'},
            {'level': '1', 'tag': 'WIFE', 'arguments': 'I02', 'original': '1 WIFE I02'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I03', 'original': '1 CHIL I03'},
            {'level': '1', 'tag': 'CHIL', 'arguments': 'I04', 'original': '1 CHIL I04'},
        ]

        find_parent(self.input_list)
        self.indi_table = create_individual_table(self.input_list, valid_tags)

        db_insert(self.db_indi_col, self.indi_table)

        with open("errors.txt", "r") as fstream:
            for line in fstream:
                if("US04:" in line):
                    self.assertTrue(True)
            self.assertTrue(False)
    
    def tearDown(self) -> None:
        errorFile = open("errors.txt", "w")
        errorFile.close()
        return super().tearDown()

    @classmethod
    def tearDownClass(self):
        self.client.drop_database("cs555_db_testing")
        return super().tearDown(self)

if __name__ == "__main__":
    unittest.main()
