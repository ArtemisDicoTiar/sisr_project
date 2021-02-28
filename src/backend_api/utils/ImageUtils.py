import numpy as np
from typing import Type
from os.path import exists
import cv2

from src.backend_api.utils.base_utils import load_image


class ImageLoader:
    def __init__(self):
        self.__img_dir = str()
        self.__img_ary = np.ndarray

    # getters and setters
    # image directory
    @property
    def image_directory(self) -> str:
        return self.__img_dir

    @image_directory.setter
    def image_directory(self, target_dir: str):
        self.__img_dir = target_dir

    # image in array
    @property
    def image_array(self) -> Type[np.ndarray]:
        return self.__img_ary

    @image_array.setter
    def image_array(self, ary):
        self.__img_ary = ary

    #
    @staticmethod
    def is_exist(target_dir: str) -> bool:
        return exists(target_dir)

    @staticmethod
    def is_image(target_dir) -> bool:
        cur_img_ext = target_dir.split('.')[-1]
        img_exts = ['jpg', 'jpeg',
                    'png', 'bmp', 'JPG']
        if cur_img_ext not in img_exts:
            return False
        return True

    def load_image(self):
        if not self.is_exist(self.image_directory):
            raise FileExistsError("File not exist.")

        if not self.is_image(self.image_directory):
            raise TypeError("This file is not Image.")

        self.image_array = load_image(self.image_directory)


def ImageSaver(save_dir: str,
               result_img):
    cv2.imwrite(save_dir, result_img)
