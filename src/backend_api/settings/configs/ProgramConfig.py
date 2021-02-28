from dataclasses import dataclass
from dacite import from_dict
from enum import Enum
import json
import os


def ModelList():
    with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json', 'r') as f:
        ModelList_f = json.load(f)
    return ModelList_f


@dataclass
class ModelUsage:
    first_model: dict
    second_model: dict = None


class BaseConfig:
    UpScaleRange = [2, 3, 4]


class ScaleDirection(Enum):
    UP = 1
    DOWN = -1


@dataclass
class ScalingRate:
    scale_direction: ScaleDirection
    first_scale: int
    second_scale: int = None


class ProgramMode:
    ONCE = 1  # LR img -> up sample (one methods)
    TWICE = 2  # LR img -> up sample 1 -> up sample 2
    DOWN = -1  # HR img -> LR img

    class Experiment:
        class UpScale(Enum):
            ONCE = 1  # LR img -> up sample (one methods)
            TWICE = 2  # LR img -> up sample 1 -> up sample 2

        class DownScale(Enum):
            DOWN = -1  # HR img -> LR img
            NULL = None

    class Produce:
        class UpScale(Enum):
            ONCE = 1  # LR img -> up sample (one methods)
            TWICE = 2  # LR img -> up sample 1 -> up sample 2


if __name__ == '__main__':
    test_dict = {
        'Interpolation': {
            'nearest': True,
            'bilinear': True,
            'bicubic': True,
            'lanczos': True,
        },
        'DeepLearning': {
            'DRCNN': True,
            'EDSR': True,
            'ESPCN': True,
            'FSRCNN': True,
            'LapSRN': True,
            'VDSR': True,
        },
        'EdgePreserve': {
            'ICBI': True,
            'INEDI': True,
        }
    }
    test = from_dict(data_class=Models, data=test_dict)
    print(test)
