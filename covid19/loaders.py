# -*- coding: utf-8 -*-
import csv
import numpy as np
import os
import pathlib

from covid19 import config
from covid19.update_data import update_italy, update_world
from covid19.utils import convert_string_to_datetime


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

    def __init__(self):
        self.data_updated = False

    def load(self, field, region=None, province=None):
        if not self.data_updated:
            update_italy()
            self.data_updated = True

        if region is not None and province is not None:
            raise ValueError("Either region or province or both must be None.")
        elif region is not None:
            return self.load_region(field, region)
        elif province is not None:
            return self.load_province(field, province)
        else:
            return self.load_country(field)

    @staticmethod
    def load_country(field):
        print("Loading data concerning Italy ...")

        columns = LoaderItaly.columns_country

        dir = os.path.join(config.repo_italy_dir, "dati-andamento-nazionale")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-andamento-nazionale-*.csv")
        filenames = sorted(filenames)

        time = []
        data = []

        for filename in filenames:
            with open(str(filename), "r") as file:
                csvdata = csv.reader(file, delimiter=",")

                for row in csvdata:
                    if csvdata.line_num == 2:
                        # time.append(convert_time_string(row[LoaderItaly.columns_country["data"]]))
                        time.append(row[columns["data"]][:10])

                        if field in columns:
                            if field == "data":
                                data.append(convert_string_to_datetime(row[columns[field]]))
                            elif field == "stato":
                                data.append(row[columns[field]])
                            else:
                                data.append(int(row[columns[field]]))
                        elif field == "incremento_relativo":
                            x = float(row[columns["totale_attualmente_positivi"]])
                            y = float(row[columns["nuovi_attualmente_positivi"]])
                            if not np.isclose(x, y):
                                data.append(y / (x - y))
                            else:
                                data.append(0.0)
                        elif field == "incremento_relativo_percentuale":
                            x = float(row[columns["totale_attualmente_positivi"]])
                            y = float(row[columns["nuovi_attualmente_positivi"]])
                            if not np.isclose(x, y):
                                data.append(100 * y / (x - y))
                            else:
                                data.append(0.0)
                        else:
                            raise RuntimeError(
                                "Sorry, don't know how to retrieve '{}'.".format(field)
                            )

        print("Load completed successfully.")

        return time, data

    @staticmethod
    def load_region(field, region):
        print("Loading data concerning {} ...".format(region))

        columns = LoaderItaly.columns_region

        dir = os.path.join(config.repo_italy_dir, "dati-regioni")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-regioni-*.csv")
        filenames = sorted(filenames)

        time = []
        data = []

        for filename in filenames:
            with open(str(filename), "r") as file:
                csvdata = csv.reader(file, delimiter=",")

                found = False

                for row in csvdata:
                    if (
                        csvdata.line_num > 1
                        and row[columns["denominazione_regione"]] == region
                    ):
                        found = True

                        # time.append(convert_time_string(row[LoaderItaly.columns["data"]]))
                        time.append(row[columns["data"]][:10])

                        if field in columns:
                            if field == "data":
                                data.append(convert_string_to_datetime(row[columns[field]]))
                            elif field == "stato":
                                data.append(row[columns[field]])
                            elif field in ("lat", "long"):
                                data.append(float(columns[field]))
                            else:
                                data.append(int(row[columns[field]]))
                        elif field == "incremento_relativo":
                            x = float(row[columns["totale_attualmente_positivi"]])
                            y = float(row[columns["nuovi_attualmente_positivi"]])
                            if not np.isclose(x, y):
                                data.append(y / (x - y))
                            else:
                                data.append(0.0)
                        elif field == "incremento_relativo_percentuale":
                            x = float(row[columns["totale_attualmente_positivi"]])
                            y = float(row[columns["nuovi_attualmente_positivi"]])
                            if not np.isclose(x, y):
                                data.append(100 * y / (x - y))
                            else:
                                data.append(0.0)
                        else:
                            raise RuntimeError(
                                "Sorry, don't know how to retrieve '{}'.".format(field)
                            )

                        break

                if not found:
                    raise RuntimeError(
                        "Sorry, region '{}' does not exist.".format(region)
                    )

        print("Load completed successfully.")

        return time, data

    @staticmethod
    def load_province(field, province):
        print("Loading data concerning {} ...".format(province))

        columns = LoaderItaly.columns_province

        dir = os.path.join(config.repo_italy_dir, "dati-province")
        filenames = pathlib.Path(dir).glob("dpc-covid19-ita-province-*.csv")
        filenames = sorted(filenames)

        time = []
        data = []

        for filename in filenames:
            with open(str(filename), "r") as file:
                csvdata = csv.reader(file, delimiter=",")

                found = False

                for row in csvdata:
                    if (
                        csvdata.line_num > 1
                        and row[columns["denominazione_provincia"]] == province
                    ):
                        found = True

                        # time.append(convert_time_string(row[LoaderItaly.columns["data"]]))
                        time.append(row[columns["data"]][:10])

                        if field in columns:
                            if field == "data":
                                data.append(convert_string_to_datetime(row[columns[field]]))
                            elif field in (
                                "stato",
                                "denominazione_regione",
                                "denominazione_provincia",
                                "sigla_provincia",
                            ):
                                data.append(row[columns[field]])
                            elif field in ("lat", "long"):
                                data.append(float(columns[field]))
                            else:
                                data.append(int(row[columns[field]]))
                        else:
                            raise RuntimeError(
                                "Sorry, don't know how to retrieve '{}'.".format(field)
                            )

                        break

                if not found:
                    raise RuntimeError(
                        "Sorry, province '{}' does not exist.".format(province)
                    )

        print("Load completed successfully.")

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

    def __init__(self):
        self.data_updated = False

    def load(self, field, province=None, country=None):
        if not self.data_updated:
            update_world()
            self.data_updated = True

        if province is not None:
            return self.load_province(field, province)
        elif country is not None:
            return self.load_country(field, country)
        else:
            raise RuntimeError("Either province or country must be not None.")

    @staticmethod
    def load_province(field, province):
        print("Loading data concerning {} ...".format(province))

        columns = LoaderWorld.columns

        dir = os.path.join(
            config.repo_world_dir, "csse_covid_19_data/csse_covid_19_daily_reports"
        )
        filenames = pathlib.Path(dir).glob("*.csv")
        filenames = sorted(filenames)

        time = []
        data = []

        for filename in filenames:
            with open(str(filename), "r") as file:
                csvdata = csv.reader(file, delimiter=",")

                found = False

                for row in csvdata:
                    if (
                        csvdata.line_num > 1
                        and row[columns["Province/State"]] == province
                    ):
                        found = True

                        # time.append(convert_time_string(row[LoaderWorld.columns_country["data"]]))
                        time.append(row[columns["Last Update"]][:10])

                        if field in columns:
                            if field == "Last Update":
                                data.append(convert_string_to_datetime(row[columns[field]]))
                            elif field in ("Province/State", "Country/Region"):
                                data.append(row[columns[field]])
                            elif field in ("Latitude", "Longitude"):
                                data.append(float(row[columns[field]]))
                            else:
                                data.append(int(row[columns[field]]))
                        else:
                            raise RuntimeError(
                                "Sorry, don't know how to retrieve '{}'.".format(field)
                            )

                        break

                if not found:
                    raise RuntimeError(
                        "Sorry, province '{}' does not exist.".format(province)
                    )

        print("Load completed successfully.")

        return time, data

    @staticmethod
    def load_country(field, country):
        print("Loading data concerning {} ...".format(country))

        columns = LoaderWorld.columns

        dir = os.path.join(
            config.repo_world_dir, "csse_covid_19_data/csse_covid_19_daily_reports"
        )
        filenames = pathlib.Path(dir).glob("*.csv")
        filenames = sorted(filenames)

        time = []
        data = []

        for index, filename in enumerate(filenames):
            with open(str(filename), "r") as file:
                csvdata = csv.reader(file, delimiter=",")

                found = False

                for row in csvdata:
                    if (
                        csvdata.line_num > 1
                        and row[columns["Country/Region"]] == country
                    ):
                        found = True

                        # time.append(convert_time_string(row[LoaderWorld.columns_country["data"]]))
                        time.append(row[columns["Last Update"]][:10])

                        if field in columns:
                            if field == "Last Update":
                                data.append(convert_string_to_datetime(row[columns[field]]))
                            elif field in ("Province/State", "Country/Region"):
                                data.append(row[columns[field]])
                            elif field in ("Latitude", "Longitude"):
                                data.append(float(row[columns[field]]))
                            else:
                                if row[columns[field]] == "":
                                    data.append(0.0)
                                else:
                                    data.append(int(row[columns[field]]))
                        else:
                            raise RuntimeError(
                                "Sorry, don't know how to retrieve '{}'.".format(field)
                            )

                        if field not in ("Confirmed", "Deaths", "Recovered"):
                            break

                if not found:
                    time.append(index)
                    data.append(0.0)
                    # raise RuntimeError(
                    #     "Sorry, country '{}' does not exist.".format(country)
                    # )

                if field in ("Confirmed", "Deaths", "Recovered"):
                    new_datum = sum(data[index:])
                    data = data[:index] + [new_datum]
                    time = time[: index + 1]

        print("Load completed successfully.")

        return time, data


if __name__ == "__main__":
    # ld = LoaderItaly()
    # time, data = ld.load("incremento_relativo_percentuale")
    # print("")
    # for t, d in zip(time, data):
    #     print("{}: {}".format(t, d))

    ld = LoaderWorld()
    time, data = ld.load("Confirmed", country="France")
    print("")
    for t, d in zip(time, data):
        print("{}: {}".format(t, d))
