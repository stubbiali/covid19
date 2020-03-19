# -*- coding: utf-8 -*-
from covid19.patchers import PatcherWorld


if __name__ == "__main__":
    pw = PatcherWorld()
    pw.replace_mainland_china()
    pw.fill_data()
    pw.check_date()
