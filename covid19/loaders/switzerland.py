# -*- coding: utf-8 -*-
import numpy as np
import os
import pandas as pd
import pathlib

from covid19 import config
from covid19.loader import Loader, registry
from covid19.utils import convert_string_to_datetime


@registry("switzerland")
class LoaderSwitzerland(Loader):
    instance = None

    def __new__(cls, *args, **kwargs):
        if LoaderSwitzerland.instance is None:
            LoaderSwitzerland.instance = super().__new__(cls)
            LoaderSwitzerland.instance.initialized = False
        return LoaderSwitzerland.instance

    def __init__(self, name, update_data, apply_patches):
        if not self.initialized:
            super().__init__(name, update_data, apply_patches)
            self.initialized = True

    def run(self, field, province=None, region=None, country=None):
        pass
