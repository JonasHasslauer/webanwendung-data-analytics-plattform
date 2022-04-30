from pandas import pandas


class Visualize:
    chartType = ""
    """"
    :param chartType: The art of chart the user wants to get visualized 
    :return None
    """

    def setChart(self, chartType: str) -> None:
        self.chartType = chartType

    def getChart(self) -> chartType:
        return self.chartType

    def getColumns(self):
        pass

    def getLines(self):
        pass
