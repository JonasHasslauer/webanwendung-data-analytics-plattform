from unittest import TestCase
import pandas as pd
from pandas.testing import assert_frame_equal
from filtern import *

class Test(TestCase):
    def test_wordarten_analyse(self):
        self.fail()


class Test(TestCase):
    def test_wordarten_analyse(self):
        #arrange
        test_df = {'Tiere': ['Maus', 'Affe', 'Huhn']}
        test_df = pd.DataFrame(test_df)

        test_df2 = {'Dollar': ['$']}
        test_df2 = pd.DataFrame(test_df2)

        expected=pd.DataFrame({
            'Wortarten:':['nounProperSingular'],
            'Werte_Wortarten:':[3]
        })
        #act
        #assert
        assert_frame_equal(expected,wortartenAnalyse(test_df))
