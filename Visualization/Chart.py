import pandas as pd
import matplotlib.pyplot as plt


class Chart:
    chartType = ""
    dataX = 0
    dataY = 0
    title = ""
    labelX = []
    labelY = []
    labelPie = []
    labelSizePie = []
    data = 0

    def setLabelPie(self, labelPie: []):
        self.labelPie = labelPie

    def getLabelPie(self) -> labelPie:
        return self.labelPie

    def setLabelSizePie(self, labelSizePie: []):
        self.labelSizePie = labelSizePie

    def getLabelSizePie(self):
        return self.labelSizePie

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
        self.labelX = labelY

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
        plt.plot(self.dataX, self.dataY, self.title, self.labelX, self.labelY)
        plt.title(self)
        plt.xlabel(self.labelX)
        plt.ylabel(self.labelY)
        plt.savefig("diagramm.png")

    def makePieDiagramm(self):
        fig1, ax1 = plt.subplots()
        ax1.pie(self.labelSizePie, labels=self.labelPie, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

    def makeBarDiagramm(self):
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.bar(self.dataX, self.dataY)
        plt.show()
