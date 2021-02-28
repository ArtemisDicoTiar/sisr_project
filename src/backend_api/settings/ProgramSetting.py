from typing import Type
from dacite import from_dict
from pprint import pprint as pp
import json
from collections import OrderedDict


from src.backend_api.settings.configs.ProgramConfig import \
    ScalingRate, ScaleDirection, \
    ProgramMode, \
    ModelUsage
from src.backend_api.utils.logBack import __get_logger

logger = __get_logger()


class ProgramSetting:
    def __init__(self):
        self.__mode = None
        self.__scales = 0
        self.__models = None

        self.program_mode = ProgramMode.Experiment.UpScale.ONCE

        self.__models = OrderedDict({
            "Interpolation": OrderedDict({
                "nearest": False,
                "bilinear": False,
                "bicubic": False,
                "lanczos": False
            }),
            "DeepLearning": OrderedDict({
                "DRCNN": False,
                "EDSR": False,
                "ESPCN": False,
                "FSRCNN": False,
                "LapSRN": False,
                "VDSR_Nearest": False,
                "VDSR_Bilinear": False,
                "VDSR_Bicubic": False,
                "VDSR_Lanczos": False
            }),
            "EdgePreserve": OrderedDict({
                "ICBI": False,
                "INEDI": False
            })
        })

    @property
    def program_mode(self):
        return self.__mode

    @program_mode.setter
    def program_mode(self, mode: str):
        self.__mode = mode

    @property
    def scaling_rate(self) -> int:
        return self.__scales

    @scaling_rate.setter
    def scaling_rate(self, scaling_rates: int):
        self.__scales = scaling_rates

    @property
    def model_usage(self) -> dict:
        return self.__models

    @model_usage.setter
    def model_usage(self, model: dict):
        self.__models = model






if __name__ == '__main__':
    test = ProgramSetting()
    test.program_mode = ProgramMode.Experiment.UpScale.ONCE

    test.scaling_rate = ScalingRate(
        scale_direction=ScaleDirection.UP,
        first_scale=2,
        # second_scale=4
    )

    with open('./configs/config.json', 'r') as f:
        ModelList = json.load(f)

    model1 = ModelList

    test.model_usage = ModelUsage(
        first_model=model1
    )

    test.setting_conflict_check()
