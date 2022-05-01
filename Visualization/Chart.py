import pandas as pd
import matplotlib.pyplot as plt


def makeLineDiagramm(dataForX, dataForY, title="", xlabel="", ylabel=""):
    plt.plot(dataForX, dataForY)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig("diagramm.png")


def makePieDiagramm():
    pass


def makeBarDiagramm():
    pass


class Chart:
    chartType = ""
    columnsPerFile = 0
    linesPerFile = 0

    def getDataFromSQL(self):
        pass

    def setSpecificLinesForChart(self, lines):
        pass

    def setSpecificColumnsForChart(self, columns):
        pass

    def setAmoutOfColumnsPerFile(self, columns: int) -> int:
        """
        :param columns: Represents the amount of selected columns in the given list
        :return int:  Return - 1 if the amount of columns equals 0
        """
        if columns == 0:
            return -1
        self.columnsPerFile = columns

    def getColumnsPerFile(self):
        return self.columnsPerFile

    def setAmountOfLinesPerFile(self, lines: int) -> int:
        """
        :param lines: Represents the amount of selected lines in the given list
        :return int:  Return - 1 if the amount of lines equals 0
        """
        if lines == 0:
            return -1
        self.linesPerFile = lines

    def getLinesPerFile(self):
        return self.linesPerFile

    def setChartType(self, chartType: str) -> None:
        """
        :param chartType: The art of chart the user wants to get visualized (Linien-, Balken- oder Torte)
        :return None
        """
        self.chartType = chartType

    def getChartType(self) -> chartType:
        """"
        :return chartType: The art of chart the user wants to get visualized
        """
        return self.chartType
