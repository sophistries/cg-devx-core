"""Global parameter store."""
import os

import yaml

from common.const.common_path import LOCAL_STATE_FILE
from common.const.const import STATE_INPUT_PARAMS, STATE_CHECKPOINTS, STATE_INTERNAL_PARAMS, \
    STATE_PARAMS
from common.const.parameter_names import CLOUD_PROVIDER, GIT_PROVIDER, DNS_REGISTRAR
from common.enums.cloud_providers import CloudProviders
from common.enums.dns_registrars import DnsRegistrars
from common.enums.git_providers import GitProviders


class StateStore:
    __store: dict = {}

    def __init__(self, input_params: None | dict = None):
        if input_params is None:
            input_params = {}
        self.__store[STATE_CHECKPOINTS] = []
        self.__store[STATE_PARAMS] = {}
        self.__store[STATE_INTERNAL_PARAMS] = {}
        self.__store[STATE_INPUT_PARAMS] = {}

        if os.path.exists(LOCAL_STATE_FILE):
            with open(LOCAL_STATE_FILE, "r+") as infile:
                config = yaml.safe_load(infile)
                try:
                    self.__store[STATE_CHECKPOINTS] = config[STATE_CHECKPOINTS]
                    self.__store[STATE_PARAMS] = config[STATE_PARAMS]
                    self.__store[STATE_INTERNAL_PARAMS] = config[STATE_INTERNAL_PARAMS]
                    self.__store[STATE_INPUT_PARAMS] = config[STATE_INPUT_PARAMS]
                except KeyError as error:
                    # ToDo: Handle missing parameters
                    pass
        self.__store[STATE_INPUT_PARAMS].update(input_params)

    @property
    def cloud_provider(self) -> CloudProviders:
        return self.__store[STATE_INPUT_PARAMS][CLOUD_PROVIDER]

    @property
    def git_provider(self) -> GitProviders:
        return self.__store[STATE_INPUT_PARAMS][GIT_PROVIDER]

    @property
    def dns_registrar(self) -> DnsRegistrars:
        return self.__store[STATE_INPUT_PARAMS][DNS_REGISTRAR]

    @dns_registrar.setter
    def dns_registrar(self, value):
        self.__store[STATE_INPUT_PARAMS][DNS_REGISTRAR] = value

    @classmethod
    def get_input_param(self, key):
        if key in self.__store[STATE_INPUT_PARAMS]:
            return self.__store[STATE_INPUT_PARAMS].get(key)
        else:
            return None

    @classmethod
    def update_input_params(self, input_params: dict):
        self.__store[STATE_INPUT_PARAMS].update(input_params)

    @property
    def input_param(self):
        return self.__store[STATE_INPUT_PARAMS]

    @classmethod
    def validate_input_params(self, validator):
        return validator(self)

    # def __getitem__(self, key: str) -> Any:
    #     return self.__store[STATE_INPUT_PARAMS].__getitem__(key)
    #
    # def __setitem__(self, key: str, value) -> None:
    #     return self.__store[STATE_INPUT_PARAMS].__setitem__(key, [value])

    @property
    def parameters(self):
        return self.__store[STATE_PARAMS]

    @property
    def internals(self):
        return self.__store[STATE_INTERNAL_PARAMS]

    @classmethod
    def set_parameter(self, key, value):
        self.__store[STATE_INTERNAL_PARAMS][key] = value

    @classmethod
    def set_checkpoint(self, name: str):
        self.__store[STATE_CHECKPOINTS].append(name)

    @classmethod
    def has_checkpoint(self, name: str):
        return name in self.__store[STATE_CHECKPOINTS]

    @classmethod
    def save_checkpoint(self):
        os.makedirs(os.path.dirname(LOCAL_STATE_FILE), exist_ok=True)
        with open(LOCAL_STATE_FILE, "w+") as outfile:
            yaml.dump(self.__store, outfile, default_flow_style=False)


def param_validator(paras: StateStore) -> bool:
    return True