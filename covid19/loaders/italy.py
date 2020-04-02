# -*- coding: utf-8 -*-
import numpy as np
import os
import pandas as pd
import pathlib

from covid19 import config
from covid19.loader import Loader, registry
from covid19.utils import convert_string_to_datetime


@registry("italy")
class LoaderItaly(Loader):
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

    instance = None

    def __new__(cls, *args, **kwargs):
        if LoaderItaly.instance is None:
            LoaderItaly.instance = super().__new__(cls)
            LoaderItaly.instance.initialized = False
        return LoaderItaly.instance

    def __init__(self, name, update_data, apply_patches):
        if not self.initialized:
            super().__init__(name, update_data, apply_patches)

            # lazy loading
            self.data_country = None
            self.data_regions = None
            self.data_provinces = None

            self.initialized = True

    def run(self, field, province=None, region=None, country=None):
        if region is not None and province is not None:
            raise ValueError("Either region or province must be None.")
        elif region is not None:
            return self.load_region(field, region)
        elif province is not None:
            return self.load_province(field, province)
        else:
            return self.load_country(field)

    def fetch_time_and_data(self, field, columns, dfs):
        error = RuntimeError(f"Don't know how to retrieve '{field}'.")

        if field in columns:
            time = []
            data = []

            for df in dfs:
                time.append(df["data"].item()[5:10])
                if field == "data":
                    data.append(convert_string_to_datetime(df["data"].item()))
                else:
                    data.append(df[field].item())
        elif "incremento_" in field:
            if "incremento_relativo_percentuale_" in field:
                column_field = field[32:]
            elif "incremento_relativo_" in field:
                column_field = field[20:]
            else:
                column_field = field[11:]

            if column_field not in columns or column_field in ("data", "stato"):
                raise error

            time, data = self.fetch_time_and_data(column_field, columns, dfs)

            n = len(data)

            if "incremento_relativo_percentuale_" in field:
                data[1:] = [
                    100.0 * (data[i + 1] - data[i]) / data[i]
                    if not np.isclose(data[i], 0.0)
                    else 0.0
                    for i in range(n - 1)
                ]
                data[0] = 0.0
            elif "incremento_relativo_" in field:
                data[1:] = [
                    (data[i + 1] - data[i]) / data[i]
                    if not np.isclose(data[i], 0.0)
                    else 0.0
                    for i in range(n - 1)
                ]
                data[0] = 0.0
            else:
                data[1:] = [data[i + 1] - data[i] for i in range(n - 1)]
                data[0] = 0.0
        elif field == "frazione_tamponi_positivi":
            time, nums = self.fetch_time_and_data("totale_casi", columns, dfs)
            _, dens = self.fetch_time_and_data("tamponi", columns, dfs)
            data = [
                num / den if not np.isclose(den, 0.0) else 0.0
                for num, den in zip(nums, dens)
            ]
        elif field == "percentuale_tamponi_positivi":
            time, nums = self.fetch_time_and_data("totale_casi", columns, dfs)
            _, dens = self.fetch_time_and_data("tamponi", columns, dfs)
            data = [
                100.0 * num / den if not np.isclose(den, 0.0) else 0.0
                for num, den in zip(nums, dens)
            ]
        elif field == "frazione_nuovi_tamponi_positivi":
            time, nums = self.fetch_time_and_data(
                "incremento_totale_casi", columns, dfs
            )
            _, dens = self.fetch_time_and_data("incremento_tamponi", columns, dfs)
            data = [
                num / den if not np.isclose(den, 0.0) else 0.0
                for num, den in zip(nums, dens)
            ]
        elif field == "percentuale_nuovi_tamponi_positivi":
            time, nums = self.fetch_time_and_data(
                "incremento_totale_casi", columns, dfs
            )
            _, dens = self.fetch_time_and_data("incremento_tamponi", columns, dfs)
            data = [
                100.0 * num / den if not np.isclose(den, 0.0) else 0.0
                for num, den in zip(nums, dens)
            ]
        else:
            raise error

        return time, data

    def mount_country(self):
        print("Mount data concerning Italy ... ")

        dir = os.path.join(config.repo_italy_dir, "dati-andamento-nazionale")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-andamento-nazionale-*.csv")
        filenames = sorted(filenames)[:-1]

        self.data_country = []

        for filename in filenames:
            self.data_country.append(pd.read_csv(str(filename), delimiter=","))

    def load_country(self, field):
        if self.data_country is None:
            self.mount_country()

        print("Load data concerning Italy ...")

        return self.fetch_time_and_data(
            field, LoaderItaly.columns_country, self.data_country
        )

    def mount_regions(self):
        print("Mount data concerning the Italian regions ... ")

        dir = os.path.join(config.repo_italy_dir, "dati-regioni")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-regioni-*.csv")
        filenames = sorted(filenames)[:-1]

        self.data_regions = []

        for filename in filenames:
            self.data_regions.append(pd.read_csv(str(filename), delimiter=","))

    def load_region(self, field, region):
        if self.data_regions is None:
            self.mount_regions()

        print("Load data concerning {} ... ".format(region))

        rows = []

        for df in self.data_regions:
            row = df.loc[df["denominazione_regione"] == region]
            row.reset_index(drop=True)

            if len(row) == 0:
                raise RuntimeError(f"Region '{region}' does not exist.")

            rows.append(row)

        return self.fetch_time_and_data(field, LoaderItaly.columns_region, rows)

    def mount_provinces(self):
        print("Mount data concerning the Italian provinces ... ")

        dir = os.path.join(config.repo_italy_dir, "dati-province")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-province-*.csv")
        filenames = sorted(filenames)[:-1]

        self.data_provinces = []

        for filename in filenames:
            self.data_provinces.append(pd.read_csv(str(filename), delimiter=","))

    def load_province(self, field, province):
        if self.data_provinces is None:
            self.mount_provinces()

        print("Load data concerning {} ...".format(province))

        rows = []

        for df in self.data_provinces:
            row = df.loc[df["denominazione_provincia"] == province]
            row.reset_index(drop=True)

            if len(row) == 0:
                raise RuntimeError(f"Province '{province}' does not exist.")

            rows.append(row)

        return self.fetch_time_and_data(field, LoaderItaly.columns_province, rows)
