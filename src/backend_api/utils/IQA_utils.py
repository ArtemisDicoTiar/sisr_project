import pandas as pd
import cv2
from PIL import Image
import pytesseract

from image_similarity_measures.quality_metrics import rmse, psnr, fsim, ssim, uiq, sre
# https://pypi.org/project/image-similarity-measures/
"""
Müller, M. U., Ekhtiari, N., Almeida, R. M., and Rieke, C.: 
SUPER-RESOLUTION OF MULTISPECTRAL SATELLITE IMAGES USING CONVOLUTIONAL NEURAL NETWORKS, 
ISPRS Ann. Photogramm. Remote Sens. Spatial Inf. Sci., V-1-2020, 33–40, 
https://doi.org/10.5194/isprs-annals-V-1-2020-33-2020, 2020.
"""


class IQA_metrics:
    def __init__(self, OCR_target_lang=''):
        self._original_img = None
        self._pred_img = None
        self.OCR_target_lang = OCR_target_lang

    @property
    def originalImage(self):
        return self._original_img

    @originalImage.setter
    def originalImage(self, org_img_ary):
        self._original_img = org_img_ary

    @property
    def predictedImage(self):
        return self._pred_img

    @predictedImage.setter
    def predictedImage(self, pred_img_ary):
        if self.originalImage.shape == pred_img_ary.shape:
            self._pred_img = pred_img_ary
        else:
            (x, y, _) = self.originalImage.shape
            self._pred_img = pred_img_ary[:x, :y, :]

    def size_compare(self):
        return self.originalImage.shape == self.predictedImage.shape

    @property
    def RMSE(self):
        if not self.size_compare():
            return -1
        return rmse(org_img=self.originalImage, pred_img=self.predictedImage)

    @property
    def PSNR(self):
        if not self.size_compare():
            return -1
        return psnr(org_img=self.originalImage, pred_img=self.predictedImage)

    @property
    def FSIM(self):
        if not self.size_compare():
            return -1
        return fsim(org_img=self.originalImage, pred_img=self.predictedImage)

    @property
    def SSIM(self):
        if not self.size_compare():
            return -1
        return ssim(org_img=self.originalImage, pred_img=self.predictedImage)

    @property
    def UIQ(self):
        if not self.size_compare():
            return -1
        return uiq(org_img=self.originalImage, pred_img=self.predictedImage)

    @property
    def SRE(self):
        if not self.size_compare():
            return -1
        return sre(org_img=self.originalImage, pred_img=self.predictedImage)

    @property
    def OCR(self):
        if self.OCR_target_lang == '':
            return None
        org_char = pytesseract.image_to_string(self.originalImage, lang=self.OCR_target_lang)
        pred_char = pytesseract.image_to_string(self.predictedImage, lang=self.OCR_target_lang)
        result = "original: {org_char}, predicted: {pred_char}".format(org_char=org_char, pred_char=pred_char)
        return result

    def get_result(self, _with: str):
        result_dict = {
            'RMSE': self.RMSE,
            'PSNR': self.PSNR,
            'FSIM': self.FSIM,
            'SSIM': self.SSIM,
            # 'UIQ': self.UIQ,
            # 'SRE': self.SRE,
            'OCR': self.OCR
        }
        if _with == 'dict':
            return result_dict
        elif _with == 'df':
            return pd.DataFrame.from_dict(result_dict, columns=['RMSE', 'PSNR', 'FSIM', 'SSIM', 'OCR'], orient='index')
        else:
            raise TypeError("Unsupporting type")
