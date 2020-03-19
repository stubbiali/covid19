# -*- coding: utf-8 -*-
from datetime import datetime
import csv
import numpy as np
import os
import pathlib

from covid19 import config
from covid19.update_data import update_italy, update_world


def convert_time_string(time_string):
    year = int(time_string[:4])
    month = int(time_string[5:7])
    day = int(time_string[8:10])
    return datetime(year=year, month=month, day=day)


class PatcherItaly:
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


class PatcherWorld:
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
        update_world()

    @staticmethod
    def check_date():
        columns = PatcherWorld.columns

        dir = os.path.join(
            config.repo_world_dir, "csse_covid_19_data/csse_covid_19_daily_reports"
        )
        filenames = pathlib.Path(dir).glob("*.csv")
        filenames = sorted(filenames)

        for filename in filenames:
            filename = str(filename)
            date = filename[-14:-4]

            # read data from file
            with open(filename, "r") as file:
                csv_reader = csv.reader(file, delimiter=",")
                csv_data = list(csv_reader)

            # modify date
            for row in csv_data[1:]:
                row[columns["Last Update"]] = date

            # write back to file
            with open(filename, "w") as file:
                csv_writer = csv.writer(file, delimiter=",")
                csv_writer.writerows(csv_data)

    @staticmethod
    def fill_data():
        columns = PatcherWorld.columns

        dir = os.path.join(
            config.repo_world_dir, "csse_covid_19_data/csse_covid_19_daily_reports"
        )
        filenames = pathlib.Path(dir).glob("*.csv")
        filenames = sorted(filenames)

        province_and_country = set()

        # get all province and country pairs
        for filename in filenames:
            with open(str(filename), "r") as file:
                csv_reader = csv.reader(file, delimiter=",")
                for row in csv_reader:
                    if csv_reader.line_num > 1:
                        province = row[columns["Province/State"]]
                        country = row[columns["Country/Region"]]
                        province_and_country.add((province, country))

        for filename in filenames:
            filename = str(filename)
            date = filename[:10]

            province_and_country_dc = province_and_country.copy()

            # catch the province and country pairs already in the file
            with open(filename, "r") as file:
                csv_reader = csv.reader(file, delimiter=",")
                for row in csv_reader:
                    if csv_reader.line_num > 1:
                        province = row[columns["Province/State"]]
                        country = row[columns["Country/Region"]]
                        try:
                            province_and_country_dc.remove((province, country))
                        except KeyError:
                            pass

            # write the province and country pairs missing
            with open(filename, "a") as file:
                csv_writer = csv.writer(file, delimiter=",")
                for elem in province_and_country_dc:
                    csv_writer.writerow([elem[0], elem[1], date, 0, 0, 0, 0.0, 0.0])


if __name__ == "__main__":
    pw = PatcherWorld()
    pw.check_date()
    pw.fill_data()
