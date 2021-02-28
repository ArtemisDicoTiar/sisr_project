import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

import cv2

import pathlib

import math

"""
A  B  C  D
E  F  G  H
I  J  K  L
M  N  O  P

-> 2* down-sampling
A  C 
I  K
"""


class DownSampler:
    def __init__(self,
                 scale_factor: int,
                 color_type: str
                 ):
        self.img_array = None
        self.scale_factor = scale_factor
        self.color_type = color_type

        self.result_image = None

    def load_image(self,
                   img_dir: [str, pathlib.Path]):
        self.img_array = cv2.imread(img_dir)

    def process_down_sample(self, show=False):
        global target_color_range

        if self.color_type in ['gray', 'black']:
            target_color_range = cv2.COLOR_BGR2GRAY
            color_map = 'gray'
        elif self.color_type == 'color':
            target_color_range = cv2.COLOR_BGR2RGB
            color_map = None
        else:
            raise ValueError('Wrong Color Type')

        target_image = cv2.cvtColor(self.img_array, target_color_range)

        shape = target_image.shape
        img_X = shape[1]
        img_Y = shape[0]

        if len(shape) == 3:
            target_shape = [math.ceil(img_X/self.scale_factor), math.ceil(img_Y/self.scale_factor), 3]
        elif len(shape) == 2:
            target_shape = [math.ceil(img_X/self.scale_factor), math.ceil(img_Y/self.scale_factor)]
        else:
            raise UnboundLocalError('Wrong Image Array Shape')

        result_img = []

        for x in range(img_X):
            if x % self.scale_factor == 0:
                for y in range(img_Y):
                    if y % self.scale_factor == 0:
                        result_img.append(target_image[y][x].tolist())

        squeezed_array = np.array(result_img, dtype=np.uint8)
        transposed_array = np.reshape(squeezed_array, target_shape)

        result_array = np.transpose(transposed_array, (1, 0, 2))

        if show:
            plt.imshow(result_array, cmap=color_map)
            plt.show()

        self.result_image = result_array

    def save_img(self,
                 save_name: str):
        im = Image.fromarray(self.result_image)

        im.save(save_name)


if __name__ == '__main__':
    downSampler = DownSampler(scale_factor=2, color_type='color')

    downSampler.load_image('../../test_images/originalImage.jpg')
    downSampler.process_down_sample()
    downSampler.save_img('../../test_images/downSampled.jpg')


