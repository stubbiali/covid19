# -*- coding: utf-8 -*-
import numpy as np
import os
import pandas as pd
import pathlib

from covid19 import config
from covid19.loader import Loader, registry
from covid19.utils import convert_string_to_datetime


@registry("world")
class LoaderWorld(Loader):
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

    def __new__(cls, *args, **kwargs):
        if LoaderWorld.instance is None:
            LoaderWorld.instance = super().__new__(cls)
            LoaderWorld.instance.initialized = False
        return LoaderWorld.instance

    def __init__(self, name, update_data, apply_patches):
        if not self.initialized:
            super().__init__(name, update_data, apply_patches)

            # lazy loading
            self.data = None

            self.initialized = True

    def run(self, field, province=None, region=None, country=None):
        if province is not None:
            return self.load_province(field, province)
        elif country is not None:
            return self.load_country(field, country)
        else:
            raise RuntimeError("Either province or country must be not None.")

    def mount(self):
        print("Mount global data ...")

        dir = os.path.join(
            config.repo_world_dir, "csse_covid_19_data/csse_covid_19_daily_reports"
        )
        filenames = pathlib.Path(dir).glob("*.csv")
        filenames = sorted(filenames)

        self.data = []

        for filename in filenames:
            self.data.append(pd.read_csv(str(filename), delimiter=","))

    def fetch_time_and_data(self, field, dfs):
        error = RuntimeError(f"Don't know how to retrieve '{field}'.")

        if field in LoaderWorld.columns:
            time = []
            data = []

            for df in dfs:
                time.append(df["Last Update"][df.index[0]][:10])

                if field == "Last Update":
                    data.append(
                        convert_string_to_datetime(df["Last Update"][df.index[0]])
                    )
                elif field in ("Confirmed", "Deaths", "Recovered"):
                    data.append(df.sum(axis=0)[field])
                else:
                    data.append(df[field][df.index[0]])
        elif "increase_" in field:
            if "relative_percentage_increase_" in field:
                column_field = field[29:]
            elif "relative_increase_" in field:
                column_field = field[18:]
            else:
                column_field = field[9:]

            if column_field not in ("Confirmed", "Deaths", "Recovered"):
                raise error

            time, data = self.fetch_time_and_data(column_field, dfs)

            n = len(data)

            if "relative_percentage_increase_" in field:
                data[1:] = [
                    100.0 * (data[i + 1] - data[i]) / data[i]
                    if not np.isclose(data[i], 0.0)
                    else 0.0
                    for i in range(n - 1)
                ]
                data[0] = 0.0
            elif "relative_increase_" in field:
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
        else:
            raise error

        return time, data

    def load_province(self, field, province):
        if self.data is None:
            self.mount()

        print(f"Load data concerning {province} ...")

        rows = []

        for df in self.data:
            row = df.loc[df["Province/State"] == province]
            if len(row) == 0:
                raise RuntimeError(f"Sorry, province '{province}' does not exist.")

            rows.append(row)

        return self.fetch_time_and_data(field, rows)

    def load_country(self, field, country):
        if self.data is None:
            self.mount()

        print(f"Load data concerning {country} ...")

        subdfs = []

        for df in self.data:
            subdf = df.loc[df["Country/Region"] == country]
            if len(subdf) == 0:
                raise RuntimeError(f"Sorry, country '{country}' does not exist.")

            subdfs.append(subdf)

        return self.fetch_time_and_data(field, subdfs)
