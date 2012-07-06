import unittest
from axxess_8520_smdr_util import clean_line
from axxess_8520_smdr_util import line_to_cdr

class test_smdr_functions(unittest.TestCase):

    def test_clean_line(self):
        dirty_line = "R\0\0 Sample line with prefix R"
        cleaned_line = clean_line(dirty_line)
        self.assertEqual(cleaned_line, " Sample line with prefix R")
        dirty_line = "Q\0\0 Sample line with prefix Q"
        cleaned_line = clean_line(dirty_line)
        self.assertEqual(cleaned_line, " Sample line with prefix Q")

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

if __name__ == '__main__':
    unittest.main()

