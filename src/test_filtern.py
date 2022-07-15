from unittest import TestCase
import pandas as pd
from pandas.testing import assert_frame_equal
from filtern import *

class Test(TestCase):
    def test_wordarten_analyse(self):
        self.fail()

#dadruch, dass Wortartenanalyse nun ein png zuückgibt ist
# dieser Test leider nicht mehr funktionstüchtig


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
        expected_2 =pd.DataFrame({
            'Wortarten:':['Dollarzeichen'],
            'Werte_Wortarten:':[1]
        })
        #act
        #assert
        assert_frame_equal(expected_2,wortartenAnalyse(test_df2))
