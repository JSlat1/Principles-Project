from flask import render_template,  Blueprint, send_file
import pandas as pd
import requests
import json
import numpy as np
import os

path = os.getcwd()

principlesProject = Blueprint("principlesProject", __name__, static_folder = "static", template_folder = "templates")

happy_df = pd.read_csv(path + "/FunSite/happiness_data.csv").drop("Unnamed: 0", axis=1)
noodle_df = pd.read_csv(path + "/FunSite/noodles.csv")


#################################################
######             Flask Routes             #####
#################################################
@principlesProject.route("/principles")
@principlesProject.route("/")
def projectMain():
    return render_template('base_noodle_proj.html')

@principlesProject.route("/noodles")
def projectNoodles():
    return render_template('noodles_page.html')

@principlesProject.route("/health")
def projectHealth():
    return render_template('noodles_health_page.html')

@principlesProject.route("/wealth")
def projectWealth():
    return render_template('noodles_wealth_page.html')

@principlesProject.route("/csv/noodles.csv")
def giveNoodleCsv():
    return send_file(path + "/FunSite/noodles.csv")

@principlesProject.route("/csv/happiness_data.csv")
def giveHappinessCsv():
    return send_file(path + "/FunSite/happiness_data.csv")
