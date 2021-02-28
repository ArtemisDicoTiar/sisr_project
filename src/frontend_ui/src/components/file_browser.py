from pathlib import Path
from shutil import copy

from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
import sys


class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'File Browser'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        self.opened_file_dir = ''

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.opened_file_dir = fileName

    def saveFileDialog(self, file_dir, file_type):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;"
                                                  "png (*.png);;jpg, Jpeg, JPG (*.jpg);;"
                                                  "csv (*.csv);;graph (*.html)", options=options)
        if file_type == 'img':
            ext = fileName.split('.')[-1].lower()
            if ext == 'png' or ext == 'jpg' or ext == 'jpeg':
                copy(file_dir, fileName)
            else:
                copy(file_dir, fileName+'.png')

        elif file_type == 'graph':
            ext = fileName.split('.')[-1].lower()
            if ext == 'html':
                copy(file_dir, fileName)
            else:
                copy(file_dir, fileName+'.html')

        elif file_type == 'table':
            ext = fileName.split('.')[-1].lower()
            if ext == 'csv':
                copy(file_dir, fileName)
            else:
                copy(file_dir, fileName+'.csv')
