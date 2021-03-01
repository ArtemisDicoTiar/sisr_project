import os
import sys
import time

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))

from src.backend_api.settings.ProgramSetting import ProgramSetting, ModelUsage

from src.frontend_ui.src.components.file_browser import FileBrowser
from src.frontend_ui.src.components.processing import ProcessWindow


class UI_Setting(QtWidgets.QDialog):
    def __init__(self, parent=None):
        os.system('mkdir ./{cur_dir}')
        self.program_setting = ProgramSetting()

        self.target_image = str()

        QtWidgets.QDialog.__init__(self, parent)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.ui = uic.loadUi(dir_path+"/../ui/ProgramSetting.ui", self)

        self.ImageSelect.clicked.connect(self.open_file_browser)

        self.Check_all.stateChanged.connect(lambda: self.checked_item(self.Check_all))

        self.Nearest.stateChanged.connect(lambda: self.checked_item(self.Nearest))
        self.Bilinear.stateChanged.connect(lambda: self.checked_item(self.Bilinear))
        self.Bicubic.stateChanged.connect(lambda: self.checked_item(self.Bicubic))
        self.Lanczos.stateChanged.connect(lambda: self.checked_item(self.Lanczos))
        self.INEDI.stateChanged.connect(lambda: self.checked_item(self.INEDI))
        self.ICBI.stateChanged.connect(lambda: self.checked_item(self.ICBI))
        self.DRCNN.stateChanged.connect(lambda: self.checked_item(self.DRCNN))
        self.EDSR.stateChanged.connect(lambda: self.checked_item(self.EDSR))
        self.ESPCN.stateChanged.connect(lambda: self.checked_item(self.ESPCN))
        self.FSRCNN.stateChanged.connect(lambda: self.checked_item(self.FSRCNN))
        self.VDSR_Nearest.stateChanged.connect(lambda: self.checked_item(self.VDSR_Nearest))
        self.VDSR_Bilinear.stateChanged.connect(lambda: self.checked_item(self.VDSR_Bilinear))
        self.VDSR_Bicubic.stateChanged.connect(lambda: self.checked_item(self.VDSR_Bicubic))
        self.VDSR_Lanczos.stateChanged.connect(lambda: self.checked_item(self.VDSR_Lanczos))
        self.LapSRN.stateChanged.connect(lambda: self.checked_item(self.LapSRN))

        self.ScaleRatio.activated.connect(lambda: self.factor(self.ScaleRatio))
        self.Mode.activated.connect(lambda: self.mode(self.Mode))

        self.OK.clicked.connect(lambda: self.progress(self.OK))
        self.Cancel.clicked.connect(lambda: self.progress(self.Cancel))

        self.program_setting.scaling_rate = 2
        self.program_setting.program_mode = 'Experiment'

        self.ICBI_available.setText('')
        self.INEDI_available.setText('')
        self.DRCNN_available.setText('')
        self.EDSR_available.setText('')
        self.ESPCN_available.setText('')
        self.FSRCNN_available.setText('')
        self.LapSRN_available.setText('')

        self.ui.show()

    @staticmethod
    def is_image(target_dir: str) -> bool:
        cur_img_ext = target_dir.lower().split('.')[-1]
        img_exts = ['jpg', 'jpeg',
                    'png', 'bmp']
        if cur_img_ext not in img_exts:
            return False
        return True

    def open_file_browser(self):
        file_browser = FileBrowser()
        file_browser.openFileNameDialog()
        self.target_image = file_browser.opened_file_dir
        if not self.is_image(self.target_image):
            QMessageBox.warning(self, "Warning", 'This file is not image')
        else:
            self.SelectedImageName.setText(self.target_image.split('/')[-1])

    def checked_item(self, looking_item):
        if looking_item.text() == '  Check All':
            self.Nearest.setChecked(self.Check_all.isChecked())
            self.Bilinear.setChecked(self.Check_all.isChecked())
            self.Bicubic.setChecked(self.Check_all.isChecked())
            self.Lanczos.setChecked(self.Check_all.isChecked())
            self.INEDI.setChecked(self.Check_all.isChecked())
            self.ICBI.setChecked(self.Check_all.isChecked())
            self.DRCNN.setChecked(self.Check_all.isChecked())
            self.EDSR.setChecked(self.Check_all.isChecked())
            self.ESPCN.setChecked(self.Check_all.isChecked())
            self.FSRCNN.setChecked(self.Check_all.isChecked())
            self.VDSR_Nearest.setChecked(self.Check_all.isChecked())
            self.VDSR_Bilinear.setChecked(self.Check_all.isChecked())
            self.VDSR_Bicubic.setChecked(self.Check_all.isChecked())
            self.VDSR_Lanczos.setChecked(self.Check_all.isChecked())
            self.LapSRN.setChecked(self.Check_all.isChecked())

            self.program_setting.model_usage['Interpolation']['nearest'] = self.Nearest.isChecked()
            self.program_setting.model_usage['Interpolation']['bilinear'] = self.Bilinear.isChecked()
            self.program_setting.model_usage['Interpolation']['bicubic'] = self.Bicubic.isChecked()
            self.program_setting.model_usage['Interpolation']['lanczos'] = self.Lanczos.isChecked()
            self.program_setting.model_usage['EdgePreserve']['INEDI'] = self.INEDI.isChecked()
            self.program_setting.model_usage['EdgePreserve']['ICBI'] = self.ICBI.isChecked()
            self.program_setting.model_usage['DeepLearning']['DRCNN'] = self.DRCNN.isChecked()
            self.program_setting.model_usage['DeepLearning']['EDSR'] = self.EDSR.isChecked()
            self.program_setting.model_usage['DeepLearning']['ESPCN'] = self.ESPCN.isChecked()
            self.program_setting.model_usage['DeepLearning']['VDSR_Nearest'] = self.VDSR_Nearest.isChecked()
            self.program_setting.model_usage['DeepLearning']['VDSR_Bilinear'] = self.VDSR_Bilinear.isChecked()
            self.program_setting.model_usage['DeepLearning']['VDSR_Bicubic'] = self.VDSR_Bicubic.isChecked()
            self.program_setting.model_usage['DeepLearning']['VDSR_Lanczos'] = self.VDSR_Lanczos.isChecked()
            self.program_setting.model_usage['DeepLearning']['LapSRN'] = self.LapSRN.isChecked()
            self.program_setting.model_usage['DeepLearning']['FSRCNN'] = self.FSRCNN.isChecked()

        elif looking_item.text() == '  Nearest':
            self.program_setting.model_usage['Interpolation']['nearest'] = self.Nearest.isChecked()
        elif looking_item.text() == '  Bilinear':
            self.program_setting.model_usage['Interpolation']['bilinear'] = self.Bilinear.isChecked()
        elif looking_item.text() == '  Bicubic':
            self.program_setting.model_usage['Interpolation']['bicubic'] = self.Bicubic.isChecked()
        elif looking_item.text() == '  Lanczos':
            self.program_setting.model_usage['Interpolation']['lanczos'] = self.Lanczos.isChecked()
        elif looking_item.text() == '  iNEDI':
            self.program_setting.model_usage['EdgePreserve']['INEDI'] = self.INEDI.isChecked()
        elif looking_item.text() == '  iCBI':
            self.program_setting.model_usage['EdgePreserve']['ICBI'] = self.ICBI.isChecked()
        elif looking_item.text() == '  DRCNN':
            self.program_setting.model_usage['DeepLearning']['DRCNN'] = self.DRCNN.isChecked()
        elif looking_item.text() == '  EDSR':
            self.program_setting.model_usage['DeepLearning']['EDSR'] = self.EDSR.isChecked()
        elif looking_item.text() == '  ESPCN':
            self.program_setting.model_usage['DeepLearning']['ESPCN'] = self.ESPCN.isChecked()
        elif looking_item.text() == '  VDSR_Nearest':
            self.program_setting.model_usage['DeepLearning']['VDSR_Nearest'] = self.VDSR_Nearest.isChecked()
        elif looking_item.text() == '  VDSR_Bilinear':
            self.program_setting.model_usage['DeepLearning']['VDSR_Bilinear'] = self.VDSR_Bilinear.isChecked()
        elif looking_item.text() == '  VDSR_Bicubic':
            self.program_setting.model_usage['DeepLearning']['VDSR_Bicubic'] = self.VDSR_Bicubic.isChecked()
        elif looking_item.text() == '  VDSR_Lanczos':
            self.program_setting.model_usage['DeepLearning']['VDSR_Lanczos'] = self.VDSR_Lanczos.isChecked()
        elif looking_item.text() == '  LapSRN':
            self.program_setting.model_usage['DeepLearning']['LapSRN'] = self.LapSRN.isChecked()
        elif looking_item.text() == '  FSRCNN':
            self.program_setting.model_usage['DeepLearning']['FSRCNN'] = self.FSRCNN.isChecked()

    def factor(self, dropdown):
        self.program_setting.scaling_rate = int(dropdown.currentText())
        if self.program_setting.scaling_rate == 3:
            self.ICBI.setChecked(False)
            self.INEDI.setChecked(False)
            self.LapSRN.setChecked(False)

            self.ICBI_available.setText('X')
            self.INEDI_available.setText('X')
            self.LapSRN_available.setText('X')

            self.ICBI.setCheckable(False)
            self.INEDI.setCheckable(False)
            self.LapSRN.setCheckable(False)

        elif self.program_setting.scaling_rate == 8:
            self.DRCNN.setChecked(False)
            self.EDSR.setChecked(False)
            self.ESPCN.setChecked(False)
            self.FSRCNN.setChecked(False)
            self.LapSRN.setChecked(False)

            self.DRCNN_available.setText('X')
            self.EDSR_available.setText('X')
            self.ESPCN_available.setText('X')
            self.FSRCNN_available.setText('X')
            self.LapSRN_available.setText('X')

            self.DRCNN.setCheckable(False)
            self.EDSR.setCheckable(False)
            self.ESPCN.setCheckable(False)
            self.FSRCNN.setCheckable(False)
            self.LapSRN.setCheckable(False)

        else:
            self.ICBI_available.setText('')
            self.INEDI_available.setText('')
            self.DRCNN_available.setText('')
            self.EDSR_available.setText('')
            self.ESPCN_available.setText('')
            self.FSRCNN_available.setText('')
            self.LapSRN_available.setText('')

            self.ICBI.setCheckable(True)
            self.INEDI.setCheckable(True)
            self.DRCNN.setCheckable(True)
            self.EDSR.setCheckable(True)
            self.ESPCN.setCheckable(True)
            self.FSRCNN.setCheckable(True)
            self.LapSRN.setCheckable(True)

    def mode(self, dropdown):
        self.program_setting.program_mode = dropdown.currentText()

    def progress(self, button):
        if button.text() == 'OK':
            if self.target_image == '':
                QMessageBox.about(self, "Warning", 'Please Select image.')

            elif set(self.program_setting.model_usage['Interpolation'].values()) == {False} and \
                    set(self.program_setting.model_usage['DeepLearning'].values()) == {False} and \
                    set(self.program_setting.model_usage['EdgePreserve'].values()) == {False}:
                QMessageBox.about(self, "Warning", 'Please Select models/methods to run.')

            else:
                self.close()

                self.processWindow = ProcessWindow(target_img=self.target_image,
                                                   scale_factor=self.program_setting.scaling_rate,
                                                   mode=self.program_setting.program_mode,
                                                   models=self.program_setting.model_usage)

                self.processWindow.show()

        if button.text() == 'Cancel':
            self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = UI_Setting()
    app.exec()
