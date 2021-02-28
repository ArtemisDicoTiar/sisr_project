import torch
from torch.autograd import Variable
from scipy.ndimage import imread
from PIL import Image
import numpy as np
import cv2
import time
import os
from os.path import dirname, abspath
import sys

import matplotlib.pyplot as plt

from src.backend_api.processor.processor.InterpolationProcessor import Interpolator


import warnings
warnings.filterwarnings("ignore")


def getVDSRImg(interpolated_img,
               project_dir: str = '{cur_dir}/../../../../'.format(cur_dir=os.path.dirname(os.path.abspath(__file__))),
               vdsr_dir: str = 'src/resource/DeepLearningModels/pytorch-vdsr/model',
               model_name: str = 'model/model_epoch_50.pth'):

    def colorize(y, ycbcr):
        img = np.zeros((y.shape[0], y.shape[1], 3), np.uint8)
        img[:,:,0] = y
        img[:,:,1] = ycbcr[:,:,1]
        img[:,:,2] = ycbcr[:,:,2]
        img = Image.fromarray(img, "YCbCr").convert("RGB")
        return img

    im_b_ycbcr = interpolated_img
    im_b_y = im_b_ycbcr[:,:,0].astype(float)

    im_input = im_b_y/255.
    im_input = Variable(torch.from_numpy(im_input).float()).view(1, -1, im_input.shape[0], im_input.shape[1])

    vdsr_dir = dirname(abspath(project_dir + vdsr_dir))
    sys.path.insert(0, vdsr_dir)

    model = torch.load(vdsr_dir+'/'+model_name, map_location=lambda storage, loc: storage)["model"]
    model = model.cpu()
    out = model(im_input)
    out = out.cpu()

    im_h_y = out.data[0].numpy().astype(np.float32)

    im_h_y = im_h_y * 255.
    im_h_y[im_h_y < 0] = 0
    im_h_y[im_h_y > 255.] = 255.

    im_h = colorize(im_h_y[0,:,:], im_b_ycbcr)
    converted_img = cv2.cvtColor(np.array(im_h), cv2.COLOR_RGB2BGR)

    return converted_img


if __name__ == '__main__':
    getVDSRImg()
