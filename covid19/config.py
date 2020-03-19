# -*- coding: utf-8 -*-
import csv
import os


root_dir = "/Users/subbiali/Desktop/covid19"
data_dir = os.path.join(root_dir, "data")

repo_italy_dir = os.path.join(data_dir, "italy")
repo_italy_remote = "https://github.com/pcm-dpc/COVID-19.git"
repo_italy_logfile = os.path.join(data_dir, "italy.log")

repo_world_dir = os.path.join(data_dir, "world")
repo_world_remote = "https://github.com/CSSEGISandData/COVID-19.git"
repo_world_logfile = os.path.join(data_dir, "world.log")

shorthands = {
    "Italy": "ITA",
    # regions
    "Abruzzo": "ABR",
    "Basilicata": "BAS",
    "P.A. Bolzano": "BZ",
    "Calabria": "CAL",
    "Campania": "CAM",
    "Emilia Romagna": "ER",
    "Friuli Venezia Giulia": "FVG",
    "Lazio": "LAZ",
    "Liguria": "LIG",
    "Lombardia": "LOM",
    "Marche": "MAR",
    "Molise": "MOL",
    "Piemonte": "PIE",
    "Puglia": "PUG",
    "Sardegna": "SAR",
    "Sicilia": "SIC",
    "Toscana": "TOS",
    "P.A. Trento": "TN",
    "Umbria": "UM",
    "Valle d'Aosta": "VDA",
    "Veneto": "VEN",
}
# provinces
filename = os.path.join(data_dir, "italy/dati-province/dpc-covid19-ita-province-20200224.csv")
with open(filename, "r") as csvfile:
    csvdata = csv.reader(csvfile, delimiter=",")
    for row in csvdata:
        if csvdata.line_num > 1:
            shorthands[row[5]] = row[6]
