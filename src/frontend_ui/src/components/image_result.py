# coding: utf-8

import os
import pandas as pd
import plotly.offline as po
import plotly.express as px
import sys
from PyQt5 import QtWidgets, uic, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

from src.frontend_ui.src.components.file_browser import FileBrowser


class ImageResult(QtWidgets.QDialog):
    def __init__(self, scale_factor: int, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.scale_factor = scale_factor
        self.dict_result_imgs = dict()
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.base_iqa_df = pd.read_csv(dir_path + '/../iqa_result.csv') \
            .drop('OCR', axis=1) \
            .rename({'Unnamed: 0': 'method'}, axis=1)

        self.iqa_metrics = self.base_iqa_df.sort_values(by='PSNR', axis=0, ascending=False)

        self.ui = uic.loadUi(dir_path + "/../../ui/result_window.ui", self)
        self.dict_img_obj = {
            'LR': self.ui.imgModelLR,
            'Model1': self.ui.imgModel1,
            'Model2': self.ui.imgModel2,
            'Model3': self.ui.imgModel3,
            'Model4': self.ui.imgModel4,
            'Model5': self.ui.imgModel5,
            'Model6': self.ui.imgModel6,
            'Model7': self.ui.imgModel7,
            'Model8': self.ui.imgModel8,
            'Model9': self.ui.imgModel9,
            'Model10': self.ui.imgModel10,
            'Model11': self.ui.imgModel11,
            'Model12': self.ui.imgModel12,
            'Model13': self.ui.imgModel13,
            'Model14': self.ui.imgModel14,
            'Model15': self.ui.imgModel15
        }

        self.model_order = []

        self.saveButtonModel1.clicked.connect(lambda: self.save_target(self.saveButtonModel1))
        self.saveButtonModel2.clicked.connect(lambda: self.save_target(self.saveButtonModel2))
        self.saveButtonModel3.clicked.connect(lambda: self.save_target(self.saveButtonModel3))
        self.saveButtonModel4.clicked.connect(lambda: self.save_target(self.saveButtonModel4))
        self.saveButtonModel5.clicked.connect(lambda: self.save_target(self.saveButtonModel5))
        self.saveButtonModel6.clicked.connect(lambda: self.save_target(self.saveButtonModel6))
        self.saveButtonModel7.clicked.connect(lambda: self.save_target(self.saveButtonModel7))
        self.saveButtonModel8.clicked.connect(lambda: self.save_target(self.saveButtonModel8))
        self.saveButtonModel9.clicked.connect(lambda: self.save_target(self.saveButtonModel9))
        self.saveButtonModel10.clicked.connect(lambda: self.save_target(self.saveButtonModel10))
        self.saveButtonModel11.clicked.connect(lambda: self.save_target(self.saveButtonModel11))
        self.saveButtonModel12.clicked.connect(lambda: self.save_target(self.saveButtonModel12))
        self.saveButtonModel13.clicked.connect(lambda: self.save_target(self.saveButtonModel13))
        self.saveButtonModel14.clicked.connect(lambda: self.save_target(self.saveButtonModel14))
        self.saveButtonModel15.clicked.connect(lambda: self.save_target(self.saveButtonModel15))

        self.PSNR_GraphExport.clicked.connect(lambda: self.save_graph(self.PSNR_GraphExport))
        self.RMSE_GraphExport.clicked.connect(lambda: self.save_graph(self.RMSE_GraphExport))
        self.SSIM_GraphExport.clicked.connect(lambda: self.save_graph(self.SSIM_GraphExport))
        self.FSIM_GraphExport.clicked.connect(lambda: self.save_graph(self.FSIM_GraphExport))

        self.PSNR_TableExport.clicked.connect(lambda: self.save_table(self.PSNR_TableExport))
        self.RMSE_TableExport.clicked.connect(lambda: self.save_table(self.RMSE_TableExport))
        self.SSIM_TableExport.clicked.connect(lambda: self.save_table(self.SSIM_TableExport))
        self.FSIM_TableExport.clicked.connect(lambda: self.save_table(self.FSIM_TableExport))

        self.CloseWindow.clicked.connect(self.finish_program)
        self.SortBy.activated.connect(lambda: self.update_render(self.SortBy))
        self.update_iqa_df(sort_by=self.SortBy)

    def render_graph(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        px.bar(self.iqa_metrics.set_index('method')[['PSNR']]) \
            .update_yaxes(range=[min(self.iqa_metrics['PSNR']), max(self.iqa_metrics['PSNR'])]) \
            .update_layout(showlegend=False) \
            .write_html(dir_path + '/PSNR_graph.html',
                        include_plotlyjs='cdn',
                        config=dict(displayModeBar=False))

        px.bar(self.iqa_metrics.set_index('method')[['RMSE']]) \
            .update_yaxes(range=[min(self.iqa_metrics['RMSE']), max(self.iqa_metrics['RMSE'])]) \
            .update_layout(showlegend=False) \
            .write_html(dir_path + '/RMSE_graph.html',
                        include_plotlyjs='cdn',
                        config=dict(displayModeBar=False))

        px.bar(self.iqa_metrics.set_index('method')[['FSIM']]) \
            .update_yaxes(range=[min(self.iqa_metrics['FSIM']), max(self.iqa_metrics['FSIM'])]) \
            .update_layout(showlegend=False) \
            .write_html(dir_path + '/FSIM_graph.html',
                        include_plotlyjs='cdn',
                        config=dict(displayModeBar=False))

        px.bar(self.iqa_metrics.set_index('method')[['SSIM']]) \
            .update_yaxes(range=[min(self.iqa_metrics['SSIM']), max(self.iqa_metrics['SSIM'])]) \
            .update_layout(showlegend=False) \
            .write_html(dir_path + '/SSIM_graph.html',
                        include_plotlyjs='cdn',
                        config=dict(displayModeBar=False))

        self.PSNR_Graph.load(QtCore.QUrl.fromLocalFile(dir_path + '/PSNR_graph.html'))
        self.RMSE_Graph.load(QtCore.QUrl.fromLocalFile(dir_path + '/RMSE_graph.html'))
        self.FSIM_Graph.load(QtCore.QUrl.fromLocalFile(dir_path + '/FSIM_graph.html'))
        self.SSIM_Graph.load(QtCore.QUrl.fromLocalFile(dir_path + '/SSIM_graph.html'))

    def inject_metrics(self, dict_metrics: dict):
        self.dict_result_imgs = dict_metrics
        self.update_img_dict()

    def update_iqa_df(self, sort_by):
        ascending_bool = True if sort_by.currentText() == 'RMSE' else False
        self.iqa_metrics.sort_values(by=sort_by.currentText(), axis=0, ascending=ascending_bool, inplace=True)
        self.model_order = self.iqa_metrics['method'].to_list()

    def update_table_name(self):
        for idx, model in enumerate(self.model_order):
            if idx == 0:
                self.labelModel1.setText(model)
            elif idx == 1:
                self.labelModel2.setText(model)
            elif idx == 2:
                self.labelModel3.setText(model)
            elif idx == 3:
                self.labelModel4.setText(model)
            elif idx == 4:
                self.labelModel5.setText(model)
            elif idx == 5:
                self.labelModel6.setText(model)
            elif idx == 6:
                self.labelModel7.setText(model)
            elif idx == 7:
                self.labelModel8.setText(model)
            elif idx == 8:
                self.labelModel9.setText(model)
            elif idx == 9:
                self.labelModel10.setText(model)
            elif idx == 10:
                self.labelModel11.setText(model)
            elif idx == 11:
                self.labelModel12.setText(model)
            elif idx == 12:
                self.labelModel13.setText(model)
            elif idx == 13:
                self.labelModel14.setText(model)
            elif idx == 14:
                self.labelModel15.setText(model)

    def update_img_dict(self):
        for idx, model in enumerate(self.model_order):
            directory = self.dict_result_imgs['Model{num}'.format(num=idx + 1)].split('/')[0]
            file_name = self.dict_result_imgs['Model{num}'.format(num=idx + 1)].split('/')[1]
            img_name = file_name.split('_')[0]
            self.dict_result_imgs['Model{num}'.format(num=idx + 1)] = \
                "{directory}/{img_name}_{method}.png".format(directory=directory, img_name=img_name, method=model)

    def update_whole_data(self, sort_by):
        self.update_iqa_df(sort_by)
        self.update_table_name()
        self.update_img_dict()
        self.render_graph()

    def update_render(self, sort_by):
        self.update_whole_data(sort_by)
        base = QPixmap(self.dict_result_imgs['LR'])
        x, y = base.width()/self.scale_factor, base.height()/self.scale_factor
        for name, path in self.dict_result_imgs.items():
            if name != 'Original':
                pix = QPixmap(path)
                self.dict_img_obj[name].setPixmap(pix.scaled(x, y, Qt.KeepAspectRatio))
                QApplication.processEvents()

    def save_file_browser(self, target_file, file_type):
        file_browser = FileBrowser()
        file_browser.saveFileDialog(target_file, file_type=file_type)

    def save_table(self, target):
        iqa_name = target.objectName().split('_')[0]
        save_name = './{iqa}.csv'.format(iqa=iqa_name)
        self.iqa_metrics.set_index('method')[[iqa_name]].to_csv(save_name)

        self.save_file_browser(target_file=save_name, file_type='table')

    def save_graph(self, target):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        iqa_name = target.objectName().split('_')[0]
        ref_img = dir_path + '/' + iqa_name + '_graph.html'

        self.save_file_browser(target_file=ref_img, file_type='graph')

    def save_target(self, target):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        idx = target.objectName().split('Model')[-1]
        ref_img = dir_path + '/' + self.dict_result_imgs['Model{num}'.format(num=idx)]

        print(ref_img)
        self.save_file_browser(target_file=ref_img, file_type='img')

    def finish_program(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Warning!")
        msg.setInformativeText("You are closing this program\nAre you sure close and remove all temporary process?")
        msg.setWindowTitle("Program Termination\n")
        msg.setDetailedText('All temporary process will be removed '
                            'and this process should be run again.\n'
                            'Please save processed data you need.')
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        msg.buttonClicked.connect(self.terminate)
        msg.exec()

    def terminate(self, button_name):
        if button_name.text() == '&Yes':
            self.close()
            for _, path in self.dict_result_imgs.items():
                os.system('rm ' + path)

            for path in ['PSNR_graph.html', 'RMSE_graph.html', 'FSIM_graph.html', 'SSIM_graph.html',
                         'downSampled.png', 'iqa_result.csv']:
                os.system('rm ' + path)
            sys.exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    imageResult = ImageResult(scale_factor=2)
    mode = 'Experiment'
    original_img = '../../../dataset/GroundTruth/Set5/head.JPG'
    target_img = '../downSampled.png'
    image_name = 'head'

    imageResult.inject_metrics({
        'LR': target_img,
        'Model1': '../{image_name}_{method}.png'.format(image_name=image_name, method='bilinear'),
        'Model2': '../{image_name}_{method}.png'.format(image_name=image_name, method='bicubic'),
        'Model3': '../{image_name}_{method}.png'.format(image_name=image_name, method='lanczos'),
        'Model4': '../{image_name}_{method}.png'.format(image_name=image_name, method='nearest'),
        'Model5': '../{image_name}_{method}.png'.format(image_name=image_name, method='DRCNN'),
        'Model6': '../{image_name}_{method}.png'.format(image_name=image_name, method='EDSR'),
        'Model7': '../{image_name}_{method}.png'.format(image_name=image_name, method='ESPCN'),
        'Model8': '../{image_name}_{method}.png'.format(image_name=image_name, method='FSRCNN'),
        'Model9': '../{image_name}_{method}.png'.format(image_name=image_name, method='LapSRN'),
        'Model10': '../{image_name}_{method}.png'.format(image_name=image_name, method='VDSR_Bicubic'),
        'Model11': '../{image_name}_{method}.png'.format(image_name=image_name, method='VDSR_Bilinear'),
        'Model12': '../{image_name}_{method}.png'.format(image_name=image_name, method='VDSR_Nearest'),
        'Model13': '../{image_name}_{method}.png'.format(image_name=image_name, method='VDSR_Lanczos'),
        'Model14': '../{image_name}_{method}.png'.format(image_name=image_name, method='ICBI'),
        'Model15': '../{image_name}_{method}.png'.format(image_name=image_name, method='INEDI'),
    })
    imageResult.update_render(sort_by=imageResult.SortBy)
    imageResult.show()

    sys.exit(app.exec())
