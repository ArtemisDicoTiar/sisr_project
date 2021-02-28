import os
import sys
from time import sleep

import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDialog
)
from PyQt5 import uic

from src.backend_api.processor.pre_process.downsampling import DownSampler

from src.backend_api.processor.processor.InterpolationProcessor import Interpolator
from src.backend_api.processor.processor.DeepLearningProcessor import DeepLearningProcessor, ImageSaver
from src.backend_api.processor.processor.EdgePreserveProcessor import EdgePreserveProcessor

from src.frontend_ui.src.components.image_result import ImageResult

from src.backend_api.utils.ImageUtils import ImageLoader
from src.backend_api.utils.IQA_utils import IQA_metrics


class ThreadWorker(QObject):
    finished = pyqtSignal()
    current_model_signal = pyqtSignal(str)
    process_level_signal = pyqtSignal(int)

    def __init__(self, original_img, target_img, scale_factor, mode, models):
        super().__init__()
        self.downSampler = DownSampler(scale_factor=scale_factor, color_type='color')
        self.imageLoader = ImageLoader()
        self.iqa_metrics = IQA_metrics()

        self.original_img = original_img
        self.target_img = target_img
        self.scale_factor = scale_factor
        self.mode = mode
        self.models = models
        self.image_name = self.target_img.split('/')[-1].split('.')[0]

        self.total_models = 0
        self.counter = 0
        self.current_process_level = 0

    def pre_processor(self):
        if self.mode == 'Experiment':
            self.downSampler.load_image(self.target_img)

            self.downSampler.process_down_sample()
            self.downSampler.save_img('./downSampled.png')
            self.target_img = './downSampled.png'

    def cal_total_model_num(self):
        for category, methods_dict in self.models.items():
            for method, status in methods_dict.items():
                if status:
                    self.total_models += 1

    def processor(self, category, method, status, save_name):
        if category.lower() == 'interpolation':
            interpolator = Interpolator(
                scale_factor=self.scale_factor
            )
            if status:
                interpolator.set_method(method)
                interpolator.load_image(self.target_img)
                interpolator.save_interpolated_img(save_name)

        elif category.lower() == 'deeplearning':
            if status:
                if method.lower().split('_')[0] == 'vdsr':
                    pre_interpolation = method.lower().split('_')[-1]
                    method = 'VDSR'

                deepLearningProcessor = DeepLearningProcessor(
                    scale_factor=self.scale_factor,
                    method=method
                )

                deepLearningProcessor.image = self.target_img

                if method.lower() == 'vdsr':
                    deepLearningProcessor.pre_interpolation = pre_interpolation
                    processed_img = deepLearningProcessor.processed_result()
                    ImageSaver(save_name, processed_img)

                else:
                    processed_img = deepLearningProcessor.processed_result()
                    ImageSaver(save_name, processed_img)

        elif category.lower() == 'edgepreserve':
            if status:
                edgePreserveProcessor = EdgePreserveProcessor(
                    scale_factor=self.scale_factor,
                    method=method
                )
                edgePreserveProcessor.image = self.target_img
                processed_img = edgePreserveProcessor.processed_result()
                ImageSaver(save_name, processed_img)

    def sub_process(self, category, method, status, save_name):
        if status:
            self.current_model_signal.emit("{method} in {category}".format(method=method, category=category))
            self.processor(category=category, method=method, status=status, save_name=save_name)

    def main_process(self):
        self.pre_processor()
        self.cal_total_model_num()

        iqa_result = dict()
        if self.original_img is not None:
            self.imageLoader.image_directory = self.original_img
            self.imageLoader.load_image()
            self.iqa_metrics.originalImage = self.imageLoader.image_array

        for category, methods_dict in self.models.items():
            for method, status in methods_dict.items():
                if status:
                    save_name = './{name}_{method}.png'.format(name=self.image_name, method=method)
                    self.sub_process(category, method, status, save_name)
                    if self.original_img is None and method == 'nearest':
                        self.imageLoader.image_directory = save_name
                        self.imageLoader.load_image()
                        self.iqa_metrics.originalImage = self.imageLoader.image_array

                    self.imageLoader.image_directory = save_name
                    self.imageLoader.load_image()
                    self.iqa_metrics.predictedImage = self.imageLoader.image_array

                    iqa_result[method] = self.iqa_metrics.get_result(_with='dict')

                    self.counter += 1
                    self.current_process_level = int(self.counter / self.total_models * 100)
                    self.process_level_signal.emit(self.current_process_level)
        pd.DataFrame(iqa_result).transpose().to_csv('./iqa_result.csv')

        self.finished.emit()

    def run(self):
        self.main_process()


class ProcessWindow(QDialog):
    def __init__(self,
                 target_img, scale_factor, mode, models,
                 parent=None):
        super().__init__(parent)

        self.target_img = target_img
        self.scale_factor = scale_factor
        self.mode = mode
        self.models = models
        self.image_name = self.target_img.split('/')[-1].split('.')[0]
        self.original_img = self.target_img if self.mode == 'Experiment' else None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.ui = uic.loadUi(dir_path + "/../../ui/ProcessBar.ui", self)

        self.CloseWindow.clicked.connect(self.close_window)
        self.Start.clicked.connect(self.start_process)

    def countChanged(self, value):
        self.ProgressBar.setValue(value)

    def modelChanged(self, model_name):
        self.CurrentModel.setText(model_name)

    def start_process(self):
        # Step 2: Create a QThread object
        self.thread = QThread()

        # Step 3: Create a worker object
        self.process = ThreadWorker(
            original_img=self.original_img, target_img=self.target_img,
            scale_factor=self.scale_factor, mode=self.mode, models=self.models
        )

        # Step 4: Move worker to the thread
        self.process.moveToThread(self.thread)

        # Step 5: Connect signals and slots
        self.thread.started.connect(self.process.run)
        self.process.finished.connect(self.thread.quit)
        self.process.finished.connect(self.process.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.process.process_level_signal.connect(self.countChanged)
        self.process.current_model_signal.connect(self.modelChanged)

        # Step 6: Start the thread
        self.thread.start()
        sleep(5)

        self.Start.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.Start.setEnabled(True)
        )

        self.thread.finished.connect(
            lambda: self.show_result_page()
        )

    def show_result_page(self):
        self.imageResult = ImageResult(scale_factor=self.scale_factor)
        self.imageResult.inject_metrics({
            'LR': self.target_img,
            'Model1': './{image_name}_{method}.png'.format(image_name=self.image_name, method='bilinear'),
            'Model2': './{image_name}_{method}.png'.format(image_name=self.image_name, method='bicubic'),
            'Model3': './{image_name}_{method}.png'.format(image_name=self.image_name, method='lanczos'),
            'Model4': './{image_name}_{method}.png'.format(image_name=self.image_name, method='nearest'),
            'Model5': './{image_name}_{method}.png'.format(image_name=self.image_name, method='DRCNN'),
            'Model6': './{image_name}_{method}.png'.format(image_name=self.image_name, method='EDSR'),
            'Model7': './{image_name}_{method}.png'.format(image_name=self.image_name, method='ESPCN'),
            'Model8': './{image_name}_{method}.png'.format(image_name=self.image_name, method='FSRCNN'),
            'Model9': './{image_name}_{method}.png'.format(image_name=self.image_name, method='LapSRN'),
            'Model10': './{image_name}_{method}.png'.format(image_name=self.image_name, method='VDSR_Bicubic'),
            'Model11': './{image_name}_{method}.png'.format(image_name=self.image_name, method='VDSR_Bilinear'),
            'Model12': './{image_name}_{method}.png'.format(image_name=self.image_name, method='VDSR_Nearest'),
            'Model13': './{image_name}_{method}.png'.format(image_name=self.image_name, method='VDSR_Lanczos'),
            'Model14': './{image_name}_{method}.png'.format(image_name=self.image_name, method='ICBI'),
            'Model15': './{image_name}_{method}.png'.format(image_name=self.image_name, method='INEDI'),
        })
        self.imageResult.update_render(sort_by=self.imageResult.SortBy)
        self.imageResult.show()

        self.close()

    def close_window(self):
        self.close()
