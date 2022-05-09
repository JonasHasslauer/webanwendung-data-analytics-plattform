from pandas import pandas as pd
import matplotlib.pyplot as plt


def getDataFrameFromCSV(path: str) -> pd.DataFrame:
    col_list = ['Gebiet', 'Umsatz', 'Status']
    file = pd.read_csv(path, usecols=col_list)
    df = pd.DataFrame(file)
    return df


class OrganizeDF:
    """
    Class for reorganizing the DF to extract data in the right way
    """

    pathToCSV = ""
    dataframe = ""

    def __init__(self, pathToCSV):
        self.pathToCSV = pathToCSV
        self.dataframe = getDataFrameFromCSV(self.pathToCSV)
