# -*- coding: utf-8 -*-
from covid19.patchers import PatcherItaly, PatcherWorld


if __name__ == "__main__":
    pi = PatcherItaly()
    pi.run()

    pw = PatcherWorld()
    pw.run()
