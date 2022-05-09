import pandas as pd
import matplotlib.pyplot as plt


class Chart:
    chartType = ""
    dataX = []
    dataY = []
    title = ""
    labelX = []
    labelY = []
    PieLabel = []
    PieLabelSize = []

    def setPieLabel(self, labelPie: []):
        self.PieLabel = labelPie

    def getPieLabel(self) -> PieLabel:
        return self.PieLabel

    def setPieLabelSize(self, PieLabelSize: []):
        self.PieLabelSize = PieLabelSize

    def getPieLabelSize(self):
        return self.PieLabelSize

    def setTitle(self, title: str):
        self.title = title

    def getTitle(self):
        return self.title

    def setDataX(self, data):
        self.dataX = data

    def getDataX(self):
        return self.dataX

    def setDataY(self, data):
        self.dataY = data

    def getDataY(self):
        return self.dataY

    def setLabelX(self, labelX: str):
        self.labelX = labelX

    def getLabelX(self, labelX: str):
        return self.labelX

    def setLabelY(self, labelY: str):
        self.labelY = labelY

    def getLabelY(self, labelY: str):
        return self.labelY

    def getDataFromSQL(self):
        pass

    def setChartType(self, chartType: str):
        """
        :param chartType: The art of chart the user wants to get visualized (Linien-, Balken- oder Torte)
        :return None
        """
        self.chartType = chartType

    def getChartType(self):
        """"
        :return chartType: The art of chart the user wants to get visualized
        """
        return self.chartType

    def makeLineDiagramm(self):
        plt.plot(self.dataX, self.dataY)
        plt.title(self.title)
        plt.xlabel(self.labelX)
        plt.ylabel(self.labelY)
        plt.show()

    def makePieDiagramm(self):
        fig1, ax1 = plt.subplots()
        ax1.pie(self.PieLabelSize, labels=self.PieLabel, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
        plt.savefig("PieDiagramm.png")

    def makeBarDiagramm(self):
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(self.dataX, self.dataY)
        plt.show()
        plt.savefig("BarDiagramm.png")
