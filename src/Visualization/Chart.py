import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Chart:
    dataX = []
    dataY = []
    title = ""
    labelX = []
    labelY = []

    def __init__(self, dataX, dataY):
        self.dataX = dataX
        self.dataY = dataY

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


class PieChart(Chart):
    PieLabel = []
    PieLabelSize = []

    def __init__(self, PieLabel, PieLabelSize, dataX, dataY):
        super().__init__(dataX, dataY)
        self.PieLabel = PieLabel
        self.PieLabelSize = PieLabelSize

    def setPieLabel(self, labelPie: []):
        self.PieLabel = labelPie

    def getPieLabel(self):
        return self.PieLabel

    def setPieLabelSize(self, PieLabelSize: []):
        self.PieLabelSize = PieLabelSize

    def getPieLabelSize(self):
        return self.PieLabelSize

    def makePieChart(self):
        fig1, ax1 = plt.subplots()
        ax1.pie(self.PieLabelSize, labels=self.PieLabel, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        return plt.show()


class BarChart(Chart):
    labelX = []
    labelY = []

    def __init__(self, labelX: [], labelY: [], dataX, dataY):
        self.labelX = labelX
        self.labelY = labelY
        super().__init__(dataX, dataY)

    def setLabelX(self, labelX: str):
        self.labelX = labelX

    def getLabelX(self, labelX: str):
        return self.labelX

    def setLabelY(self, labelY: str):
        self.labelY = labelY

    def getLabelY(self, labelY: str):
        return self.labelY

    def makeBarChart(self):
        plt.bar(x=self.dataX, height=self.dataY)
        plt.title(self.title)
        plt.xlabel(self.labelX)
        plt.ylabel(self.labelY)
        return plt.show()


class LineChart(Chart):
    labelX = ""
    labelY = ""

    def __init__(self, labelX, labelY, dataX, dataY):
        self.labelX = labelX
        self.labelY = labelY
        super().__init__(dataX, dataY)

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

    def makeLineChart(self):
        plt.plot(self.dataX, self.dataY)
        plt.title(self.title)
        plt.xlabel(self.labelX)
        plt.ylabel(self.labelY)
        return plt.show()
