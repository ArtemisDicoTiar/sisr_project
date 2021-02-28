# coding: utf-8

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import *


class IQAMetrics(QtWidgets.QDialog):
    def __init__(self, parent=None):

        self.metrics = dict()

        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("../../ui/metrics.ui", self)

        self.ui.show()

    def inject_metrics(self, dict_metrics: dict):
        self.metrics = dict_metrics

    def clear_metrics(self):
        self.metrics = {
            'Bilinear': '',
            'Bicubic': '',
            'Lanczos': '',
            'Nearest': '',
            'Model1': '',
            'Model2': '',
            'Model3': '',
            'Model4': '',
            'Model5': '',
            'Model6': '',
            'Model7': '',
            'Model8': '',
            'Model9': '',
        }

    def get_aqi_type(self):
        print(self.ui.comboBox.currentText())
        return self.ui.comboBox.currentText()

    @pyqtSlot()
    def update_metrics(self):
        if str(self.get_aqi_type()) == '':
            self.clear_metrics()

        for idx, mets in enumerate(self.metrics.items()):
            met, val = mets
            cell_info = QTableWidgetItem(str(val))
            self.ui.tableWidget.setItem(0, idx, cell_info)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = IQAMetrics()
    tmp = {
        'Bilinear': 10,
        'Bicubic': 20,
        'Lanczos': 40,
        'Nearest': -10,
        'Model1': 0,
        'Model2': 0,
        'Model3': 0,
        'Model4': 0,
        'Model5': 0,
        'Model6': 0,
        'Model7': 0,
        'Model8': 0,
        'Model9': 0,
    }
    w.inject_metrics(tmp)
    sys.exit(app.exec())
