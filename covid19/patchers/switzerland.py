# -*- coding: utf-8 -*-
from covid19.patcher import Patcher, registry


@registry("switzerland")
class PatcherSwitzerland(Patcher):
    def run(self):
        pass
