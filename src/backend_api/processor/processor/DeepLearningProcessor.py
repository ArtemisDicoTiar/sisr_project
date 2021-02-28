import cv2
from cv2 import dnn_superres
import os

from src.resource.DeepLearningModels.DRCNN.test import drcnn
from src.backend_api.utils.ImageUtils import ImageLoader, ImageSaver
from src.backend_api.processor.processor.vdsr import getVDSRImg
from src.backend_api.processor.processor.InterpolationProcessor import Interpolator


class DeepLearningProcessor:
    def __init__(self,
                 scale_factor: int,
                 method: str,
                 pre_interpolation: str = None):
        self._image = None
        self._scale_factor = scale_factor
        self._method = method
        self.imageLoader = ImageLoader()
        self.pre_interpolation = pre_interpolation
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, target: str):
        self._image = target

    def processed_result(self):
        if self._method == 'DRCNN':
            return self._DRCNN_processor()

        elif self._method in ['EDSR', 'ESPCN', 'FSRCNN']:
            return self._DNN_SR_processor()

        elif self._method == 'LapSRN':
            if self._scale_factor not in [2, 4, 8]:
                raise ValueError("LapSRN only accepts 2, 4, 8 for scale factor.")
            return self._DNN_SR_processor()

        elif self._method == 'VDSR':
            if self.pre_interpolation is None:
                raise ValueError("VDSR requires pre_interpolation, specify the interpolation.")
            return self._VDSR_processor()

        else:
            raise ValueError("This method is not available for DeepLearning.")

    def _DRCNN_processor(self):
        pure_img_name = self.image.split('/')[-1].split('.')[0]
        img_format = self.image.split('/')[-1].split('.')[-1]
        save_dir = '{cur_dir}/../../../images/drcnn'
        model_dir = '{cur_dir}/../../../resource/DeepLearningModels/DRCNN/model'.format(cur_dir=self.current_dir)

        drcnn([
            self.image,
            save_dir,
            model_dir,
            self._scale_factor
        ])

        self.imageLoader.image_directory = '{save_dir}/{name}_result.{img_format}' \
            .format(save_dir=save_dir, name=pure_img_name, img_format=img_format)
        self.imageLoader.load_image()

        os.system('cd {save_dir}/../../; rm -rf images'.format(save_dir=save_dir))

        return self.imageLoader.image_array

    def _DNN_SR_processor(self):
        # Create an SR object
        sr = dnn_superres.DnnSuperResImpl_create()

        # Read image
        self.imageLoader.image_directory = self.image
        self.imageLoader.load_image()
        image = self.imageLoader.image_array

        # Read the desired model
        sr.readModel('{cur_dir}/../../../resource/DeepLearningModels/{method_folder}/{method_name}_x{scale_factor}.pb'
                     .format(method_folder=self._method, method_name=self._method, scale_factor=self._scale_factor,
                             cur_dir=self.current_dir)
                     )

        # Set the desired model and scale to get correct pre- and post-processing
        sr.setModel(self._method.lower(), self._scale_factor)

        # Upscale the image
        result = sr.upsample(image)

        return result

    def _VDSR_processor(self):
        interpolator = Interpolator(scale_factor=self._scale_factor)
        interpolator.load_image(self.image)
        interpolator.set_method(self.pre_interpolation)
        interpolated = cv2.cvtColor(interpolator.get_interpolated_img(), cv2.COLOR_BGR2YCR_CB)

        return getVDSRImg(interpolated_img=interpolated)


if __name__ == '__main__':
    test = DeepLearningProcessor(
        scale_factor=2,
        method='DRCNN',
    )
    test.image = '../../../dataset/DownSampled/Set5/babyx2.png'
    print('DONE')
    tmp = test.processed_result()
    ImageSaver('./test.jpg', tmp)
