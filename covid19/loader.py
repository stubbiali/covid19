# -*- coding: utf-8 -*-
import abc
import numpy as np
import os
import pandas as pd
import pathlib

from covid19 import config
from covid19.patcher import Patcher
from covid19.updater import Updater
from covid19.utils import convert_string_to_datetime


ledger = {}


def registry(name):
    def wrapper(cls):
        ledger[name] = cls
        return cls
    return wrapper


class Loader(abc.ABC):
    def __init__(self, name, update_data, apply_patches):
        if update_data:
            updater = Updater.factory(name)
            updater.run()
        if apply_patches:
            patcher = Patcher.factory(name, update_data=False)
            patcher.run()

    @abc.abstractmethod
    def run(self, field, province=None, region=None, country=None):
        pass

    @staticmethod
    def factory(name, update_data=True, apply_patches=False, *args, **kwargs):
        if name not in ledger:
            raise RuntimeError(f"Loader {name} does not exist.")
        return ledger[name](name, update_data, apply_patches, *args, **kwargs)


class LoaderItaly:
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

    def __new__(cls):
        if LoaderItaly.instance is None:
            LoaderItaly.instance = super().__new__(cls)
        return LoaderItaly.instance

    def __init__(self, update_data=True, apply_patches=False):
        if not hasattr(self, "data_updated"):
            # lazy patching and loading
            self.data_updated = not update_data
            self.data_patched = not apply_patches
            self.data_country = None
            self.data_regions = None
            self.data_provinces = None

            # auxiliary variable used to compute increments
            self.old = None

    def fetch_time_and_datum(self, df_idx, df_row, field, columns):
        time = df_row["data"].item()[:10]

        error = RuntimeError("Sorry, don't know how to retrieve '{}'.".format(field))

        if field in columns:
            if field == "data":
                datum = convert_string_to_datetime(df_row["data"].item())
            else:
                datum = df_row[field].item()
        elif "incremento_" in field:
            if "incremento_relativo_percentuale_" in field:
                col = field[32:]
            elif "incremento_relativo_" in field:
                col = field[20:]
            else:
                col = field[11:]

            if col not in columns or col in ("data", "stato"):
                raise error

            if df_idx == 0:
                datum = 0.0
                self.old = float(df_row[col].item())
            else:
                assert self.old is not None

                new = float(df_row[col].item())

                if "incremento_relativo_percentuale_" in field:
                    datum = (
                        100 * (new - self.old) / self.old
                        if not np.isclose(self.old, 0.0)
                        else 0.0
                    )
                elif "incremento_relativo_" in field:
                    datum = (new - self.old) / self.old if not np.isclose(self.old, 0.0) else 0.0
                else:
                    datum = new - self.old

                self.old = new
        else:
            raise error

        return time, datum

    def load(self, field, region=None, province=None):
        if not self.data_updated:
            update_italy()
            self.data_updated = True

        if not self.data_patched:
            patcher = PatcherItaly()
            patcher.run()
            self.data_patched = True

        if region is not None and province is not None:
            raise ValueError("Either region or province or both must be None.")
        elif region is not None:
            return self.load_region(field, region)
        elif province is not None:
            return self.load_province(field, province)
        else:
            return self.load_country(field)

    def mount_country(self):
        print("Mount data concerning Italy ... ")

        dir = os.path.join(config.repo_italy_dir, "dati-andamento-nazionale")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-andamento-nazionale-*.csv")
        filenames = sorted(filenames)

        self.data_country = []

        for filename in filenames:
            self.data_country.append(pd.read_csv(str(filename), delimiter=","))

    def load_country(self, field):
        if self.data_country is None:
            self.mount_country()

        print("Load data concerning Italy ...")

        time = []
        data = []

        for idx, df in enumerate(self.data_country):
            t, d = self.fetch_time_and_datum(idx, df, field, LoaderItaly.columns_country)
            time.append(t)
            data.append(d)

        return time, data

    def mount_regions(self):
        print("Mount data concerning the Italian regions ... ")

        dir = os.path.join(config.repo_italy_dir, "dati-regioni")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-regioni-*.csv")
        filenames = sorted(filenames)

        self.data_regions = []

        for filename in filenames:
            self.data_regions.append(pd.read_csv(str(filename), delimiter=","))

    def load_region(self, field, region):
        if self.data_regions is None:
            self.mount_regions()

        print("Load data concerning {} ... ".format(region))

        time = []
        data = []

        for idx, df in enumerate(self.data_regions):
            row = df.loc[df["denominazione_regione"] == region]
            if len(row) == 0:
                raise RuntimeError("Sorry, region '{}' does not exist.".format(region))

            t, d = self.fetch_time_and_datum(idx, row, field, LoaderItaly.columns_region)
            time.append(t)
            data.append(d)

        return time, data

    def mount_provinces(self):
        print("Mount data concerning the Italian provinces ... ")

        dir = os.path.join(config.repo_italy_dir, "dati-province")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-province-*.csv")
        filenames = sorted(filenames)

        self.data_provinces = []

        for filename in filenames:
            self.data_provinces.append(pd.read_csv(str(filename), delimiter=","))

    def load_province(self, field, province):
        if self.data_provinces is None:
            self.mount_provinces()

        print("Load data concerning {} ...".format(province))

        columns = LoaderItaly.columns_province

        time = []
        data = []

        for idx, df in enumerate(self.data_provinces):
            row = df.loc[df["denominazione_provincia"] == province]
            if len(row) == 0:
                raise RuntimeError(
                    "Sorry, province '{}' does not exist.".format(province)
                )

            t, d = self.fetch_time_and_datum(idx, row, field, LoaderItaly.columns_province)
            time.append(t)
            data.append(d)

        return time, data


class LoaderWorld:
    columns = {
        "Province/State": 0,
        "Country/Region": 1,
        "Last Update": 2,
        "Confirmed": 3,
        "Deaths": 4,
        "Recovered": 5,
        "Latitude": 6,
        "Longitude": 7,
    }

    instance = None

    def __new__(cls):
        if LoaderWorld.instance is None:
            LoaderWorld.instance = super().__new__(cls)
        return LoaderWorld.instance

    def __init__(self, update_data=True, apply_patches=False):
        if not hasattr(self, "data_updated"):
            # lazy patching and loading
            self.data_updated = not update_data
            self.data_patched = not apply_patches
            self.data = None

            # auxiliary variable used to compute increments
            self.old = None

    def load(self, field, province=None, country=None):
        if not self.data_updated:
            update_world()
            self.data_updated = True

        if not self.data_patched:
            patcher = PatcherWorld()
            patcher.run()
            self.data_patched = True

        if province is not None:
            return self.load_province(field, province)
        elif country is not None:
            return self.load_country(field, country)
        else:
            raise RuntimeError("Either province or country must be not None.")

    def mount(self):
        print("Mount global data ... ")

        dir = os.path.join(
            config.repo_world_dir, "csse_covid_19_data/csse_covid_19_daily_reports"
        )
        filenames = pathlib.Path(dir).glob("*.csv")
        filenames = sorted(filenames)

        self.data = []

        for filename in filenames:
            self.data.append(pd.read_csv(str(filename), delimiter=","))

    def load_province(self, field, province):
        if self.data is None:
            self.mount()

        print("Load data concerning {} ...".format(province))

        columns = LoaderWorld.columns

        error = RuntimeError(
            "Sorry, don't know how to retrieve '{}'.".format(field)
        )

        time = []
        data = []

        for idx, df in enumerate(self.data):
            row = df.loc[df["Province/State"] == province]
            if len(row) == 0:
                raise RuntimeError(
                    "Sorry, province '{}' does not exist.".format(province)
                )

            time.append(row["Last Update"].item()[:10])

            if field in columns:
                if field == "Last Update":
                    data.append(convert_string_to_datetime(row["Last Update"].item()))
                else:
                    data.append(row[field].item())
            elif "increase_" in field:
                if "relative_percentage_increase_" in field:
                    col = field[29:]
                elif "relative_increase_" in field:
                    col = field[18:]
                else:
                    col = field[9:]

                if col not in ("Confirmed", "Deaths", "Recovered"):
                    raise error

                if idx == 0:
                    data.append(0.0)
                    self.old = float(row[field].item())
                else:
                    assert self.old is not None

                    new = float(row[field].item())

                    if "relative_percentage_increase_" in field:
                        data.append(100 * (new - self.old) / self.old if not np.isclose(self.old, 0.0) else 0.0)
                    elif "relative_increase_" in field:
                        data.append((new - self.old) / self.old if not np.isclose(self.old, 0.0) else 0.0)
                    else:
                        data.append(new - self.old)

                    self.old = new
            else:
                raise error

        return time, data

    def load_country(self, field, country):
        if self.data is None:
            self.mount()

        print("Load data concerning {} ...".format(country))

        columns = LoaderWorld.columns

        time = []
        data = []

        for df in self.data:
            rows = df.loc[df["Country/Region"] == country]
            if len(rows) == 0:
                raise RuntimeError(
                    "Sorry, country '{}' does not exist.".format(country)
                )

            time.append(rows["Last Update"][rows.index[0]][:10])

            if field in columns:
                if field == "Last Update":
                    data.append(
                        convert_string_to_datetime(rows["Last Update"][rows.index[0]])
                    )
                elif field in ("Confirmed", "Deaths", "Recovered"):
                    data.append(rows.sum(axis=0)[field])
                else:
                    data.append(rows[field][rows.index[0]])
            else:
                raise RuntimeError(
                    "Sorry, don't know how to retrieve '{}'.".format(field)
                )

        return time, data


if __name__ == "__main__":
    ld = LoaderItaly(update_data=False, apply_patches=False)
    ld.load_country("incremento_relativo_percentuale_totale_casi")
    ld.load_region("incremento_relativo_percentuale_totale_attualmente_positivi", "Lombardia")
    ld.load_province("totale_casi", "Bergamo")
    ld.load_province("totale_casi", "Brescia")

    ld = LoaderWorld(update_data=False, apply_patches=False)
    ld.load("Confirmed", province="Hubei")
    # ld.load("Latitude", country="Italy")

    # time, data = ld.load("incremento_relativo_percentuale")
    # print("")
    # for t, d in zip(time, data):
    #     print("{}: {}".format(t, d))

    # ld = LoaderWorld()
    # time, data = ld.load("Confirmed", country="France")
    # print("")
    # for t, d in zip(time, data):
    #     print("{}: {}".format(t, d))
