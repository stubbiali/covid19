# -*- coding: utf-8 -*-
from covid19.patcher import Patcher, ledger


if __name__ == "__main__":
    for name in ledger:
        patcher = Patcher.factory(name, update_data=True)
        patcher.run()
