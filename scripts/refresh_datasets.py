# -*- coding: utf-8 -*-
from covid19.updater import Updater, ledger


if __name__ == "__main__":
    for name in ledger:
        updater = Updater.factory(name)
        updater.run()
