# -*- coding: utf-8 -*-
from covid19.patcher import Patcher, registry


@registry("italy")
class PatcherItaly(Patcher):
    columns_country = {
        "data": 0,
        "stato": 1,
        "ricoverati_con_sintomi": 2,
        "terapia_intensiva": 3,
        "totale_ospedalizzati": 4,
        "isolamento_domiciliare": 5,
        "totale_attualmente_positivi": 6,
        "nuovi_attualmente_positivi": 7,
        "dimessi_guariti": 8,
        "deceduti": 9,
        "totale_casi": 10,
        "tamponi": 11,
    }
    columns_region = {
        "data": 0,
        "stato": 1,
        "codice_regione": 2,
        "denominazione_regione": 3,
        "lat": 4,
        "long": 5,
        "ricoverati_con_sintomi": 6,
        "terapia_intensiva": 7,
        "totale_ospedalizzati": 8,
        "isolamento_domiciliare": 9,
        "totale_attualmente_positivi": 10,
        "nuovi_attualmente_positivi": 11,
        "dimessi_guariti": 12,
        "deceduti": 13,
        "totale_casi": 14,
        "tamponi": 15,
    }
    columns_province = {
        "data": 0,
        "stato": 1,
        "codice_regione": 2,
        "denominazione_regione": 3,
        "codice_provincia": 4,
        "denominazione_provincia": 5,
        "sigla_provincia": 6,
        "lat": 7,
        "long": 8,
        "totale_casi": 9,
    }

    def run(self):
        pass


