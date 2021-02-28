import math
import cv2

from src.resource.EdgeSpecificMethods.icbi.icbi_matlab2python import ICBI_py
from src.resource.EdgeSpecificMethods.inedi.inedi_matlab2python import INEDI_py

from src.backend_api.utils.ImageUtils import ImageSaver, ImageLoader


class EdgePreserveProcessor:
    def __init__(self,
                 scale_factor: int,
                 method: str):
        self._image = None
        self._zk = math.log(scale_factor, 2)
        self._method = method
        self.imageLoader = ImageLoader()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, target):
        self._image = target

    def processed_result(self):
        if self._method == 'ICBI':
            return self._ICBI_processor()

        elif self._method == 'INEDI':
            return self._INEDI_processor()

        else:
            raise ValueError("This method is not available for EdgePreserve.")

    def _ICBI_processor(self):
        # issue: size -> 72*20 -> 143 * 39

        self.imageLoader.image_directory = self.image
        self.imageLoader.load_image()
        ary = self.imageLoader.image_array

        tar = cv2.copyMakeBorder(ary, 0, 1, 0, 1, borderType=cv2.BORDER_DEFAULT)
        ImageSaver('./test.png', tar)

        ICBI_py(IM='./test.png',
                ZK=self._zk,
                SV='./tmp_ICBI.jpg',
                VR=False)

        self.imageLoader.image_directory = './tmp_ICBI.jpg'
        self.imageLoader.load_image()

        return self.imageLoader.image_array[:-1, :-1, :]

    def _INEDI_processor(self):
        INEDI_py(IM=self.image,
                 ZK=self._zk,
                 SV='./tmp_INEDI.jpg',
                 VR=False)

        self.imageLoader.image_directory = './tmp_INEDI.jpg'
        self.imageLoader.load_image()

        return self.imageLoader.image_array


if __name__ == '__main__':
    test = EdgePreserveProcessor(
        scale_factor=2,
        method='ICBI'
    )
    test.image = '../../../images/downSampled.jpg'
    tmp = test.processed_result()
    print('DONE')
    ImageSaver('./test.jpg', tmp)
