import unittest
from axxess_8520_smdr_util import clean_line
from axxess_8520_smdr_util import file_to_cdr
from axxess_8520_smdr_util import line_to_cdr
from axxess_8520_smdr_util import insert_cdr_record
import os
import shutil
import sqlite3

class test_smdr_functions(unittest.TestCase):

    CDR_FILE = "test_cdr.log"

    def test_clean_line(self):
        dirty_line = "R\0\0 Sample line with prefix R"
        cleaned_line = clean_line(dirty_line)
        self.assertEqual(cleaned_line, " Sample line with prefix R")
        dirty_line = "Q\0\0 Sample line with prefix Q"
        cleaned_line = clean_line(dirty_line)
        self.assertEqual(cleaned_line, " Sample line with prefix Q")

    def test_file_to_cdr(self):

        cdr = file_to_cdr(self.CDR_FILE, None)
        self.assertEqual(len(cdr), 173)

    def test_line_to_cdr(self):
        header_1 = "Station Message Detailed Recording                          00:00:04 07-03-2012"
        header_2 = "TYP EXT#  TRUNK DIALED DIGITS                START ELAPSED   COST  ACCOUNT CODE"
        self.assertFalse(line_to_cdr(header_1, None))
        self.assertFalse(line_to_cdr(header_2, None))

        ring_1 = "    ***** 94129 RG 612-804-4082         8907 00:29      S=5                    *"
        ring_2 = "    181   94129 RING......0063               06:46      S=9                     "
        ring_3 = "    110   94129 RG 525530894016         0061 08:34      S=4                     "
        self.assertTrue(line_to_cdr(ring_1, None))
        self.assertTrue(line_to_cdr(ring_2, None))
        self.assertTrue(line_to_cdr(ring_3, None))

        outgoing_1 = "TLC 104   94151 952-474-1742                 08:52    S=226 $00.00              "
        outgoing_2 = "O/I 104   94151 011-49618296260              09:00    S=193 $00.00             *"
        outgoing_3 = "TLD 116   94151 1-631-220-3707               09:33     S=65 $00.00              "
        outgoing_4 = "LOC 104   94151 1-877-244-1771               11:03    S=649 $00.00              "
        self.assertTrue(line_to_cdr(outgoing_1, None))
        self.assertTrue(line_to_cdr(outgoing_2, None))
        self.assertTrue(line_to_cdr(outgoing_3, None))
        self.assertTrue(line_to_cdr(outgoing_4, None))

        incoming_1 = "IN  110   94129 525530894016            0061 08:48      S=1 $00.00             *"
        incoming_2 = "IN  181   94129 0063                         09:19     S=80 $00.00              "
        self.assertTrue(line_to_cdr(incoming_1, None))
        self.assertTrue(line_to_cdr(incoming_2, None))

class test_db_functions(unittest.TestCase):

    EMPTY_DATABASE = "test_sqdatabase_empty.db"
    DATABASE = "test_sqdatabase.db"
    CDR_FILE = "test_cdr.log"

    def setUp(self):

        shutil.copyfile(self.EMPTY_DATABASE, self.DATABASE)
        self.conn = sqlite3.connect(self.DATABASE)

    def test_insert_db(self):

        cdr = file_to_cdr(self.CDR_FILE, None)

        for record in cdr:
            rowcount = insert_cdr_record(record, self.conn.cursor())
            self.assertEqual(rowcount, 1)

        self.conn.commit()
        rows = self.conn.cursor().execute("SELECT * FROM logviewer_phonerecord").fetchall()
        self.assertEqual(len(rows), 173)

    def tearDown(self):

        self.conn.close()
        os.remove(self.DATABASE)
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_smdr_functions)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(test_db_functions)
    unittest.TextTestRunner(verbosity=2).run(suite)

