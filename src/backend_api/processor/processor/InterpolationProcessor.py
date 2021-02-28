import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import pathlib


class Interpolator:
    def __init__(self,
                 scale_factor: int):
        self.image = None

        self.scale_factor = scale_factor
        self.method = None
        self.method_name = ''

        self.methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
                        'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
                        'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

    def load_image(self,
                   image_dir: [str, pathlib.Path]):
        self.image = cv2.cvtColor(cv2.imread(image_dir), cv2.COLOR_BGR2RGB)

    def get_original_img(self, show=True):
        plt.imshow(self.image)
        plt.title('Original Image')

        if show:
            plt.show()

    def set_method(self, method: str):
        if method == 'nearest':
            self.method = cv2.INTER_NEAREST
            self.method_name = 'nearest'
        elif method == 'bilinear':
            self.method = cv2.INTER_LINEAR
            self.method_name = 'bilinear'
        elif method == 'cubic' or method == 'bicubic':
            self.method = cv2.INTER_CUBIC
            self.method_name = 'cubic'
        elif method == 'lanczos':
            self.method = cv2.INTER_LANCZOS4
            self.method_name = 'lanczos'
        else:
            raise ValueError('INVALID METHOD')

    def get_interpolated_img(self):
        width = int(self.image.shape[1] * self.scale_factor)
        height = int(self.image.shape[0] * self.scale_factor)

        # resize image
        resized = cv2.resize(self.image, (width, height), interpolation=self.method)

        return resized

    def show_interpolated_img(self):
        plt.imshow(self.get_interpolated_img())
        plt.title(str(self.method_name))
        plt.show()

    def save_interpolated_img(self, save_dir: str):
        self.save_img(target_image=self.get_interpolated_img(), save_name=save_dir)

    def show_multiple_method_results(self, methods: [list, None] = None, save_dir=None):
        fig, axs = plt.subplots(nrows=2, ncols=2,
                                # figsize=(9, 6),
                                subplot_kw={'xticks': [], 'yticks': []})
        if methods is None:
            methods = ['nearest', 'bilinear', 'cubic', 'lanczos']

        for ax, interp_method in zip(axs.flat, methods):
            self.set_method(interp_method)
            cur_resized = self.get_interpolated_img()
            ax.imshow(cur_resized)
            ax.set_title(str(interp_method))

        plt.tight_layout()

        if save_dir is None:
            plt.show()
        else:
            plt.savefig(save_dir)

    @staticmethod
    def save_img(target_image,
                 save_name: str):
        im = Image.fromarray(target_image)

        im.save(save_name)


if __name__ == "__main__":
    interpolator = Interpolator(scale_factor=2)
    interpolator.load_image('../../test_images/downSampled.jpg')

    interpolator.set_method('bilinear')
    interpolator.save_interpolated_img('../../test_images/Interpolations/bilinear.jpg')
    interpolator.set_method('nearest')
    interpolator.save_interpolated_img('../../test_images/Interpolations/nearest.jpg')
    interpolator.set_method('cubic')
    interpolator.save_interpolated_img('../../test_images/Interpolations/cubic.jpg')
    interpolator.set_method('lanczos')
    interpolator.save_interpolated_img('../../test_images/Interpolations/lanczos.jpg')

    interpolator.show_multiple_method_results(save_dir='../../test_images/Interpolations/allResults.jpg')
