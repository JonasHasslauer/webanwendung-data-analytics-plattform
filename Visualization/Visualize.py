from pandas import pandas


class Visualize:
    chartType = ""
    formattedFile = ""

    def setChart(self, chartType: str) -> None:
        """
        :param chartType: The art of chart the user wants to get visualized
        :return None
        """
        self.chartType = chartType

    def getChart(self) -> chartType:
        """"
        :return chartType: The art of chart the user wants to get visualized
        """
        return self.chartType