from flask import render_template,  Blueprint, request, redirect, url_for
import pandas as pd
import requests
import json
import plotly.express as px
import plotly.io as pio
import numpy as np
import os

path = os.getcwd()

principlesProject = Blueprint("principlesProject", __name__, static_folder = "static", template_folder = "templates")

happy_df = pd.read_csv(path + "/FunSite/happiness_data.csv").drop("Unnamed: 0", axis=1)
noodle_df = pd.read_csv(path + "/FunSite/noodles.csv")


url = "https://www3.nd.edu/~skumar5/teaching/additional/countries_data.txt"
response_text = requests.get(url).text
data_json_list = json.loads(response_text)

replace_name_dict = {
    "Korea (Republic of)": "South Korea",
    "Iran (Islamic Republic of)": "Iran",
    "Russian Federation": "Russia",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Republic of Kosovo": "Kosovo",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Moldova (Republic of)": "Moldova",
    "Viet Nam": "Vietnam",
    "Macedonia (the former Yugoslav Republic of)": "Macedonia",
    "Lao People's Democratic Republic": "Laos",
    "Palestine, State of": "Palestine",
    "Tanzania, United Republic of": "Tanzania",
    "Syrian Arab Republic": "Syria"
    }

all_countries = []
for country_dict in data_json_list:
  if country_dict['name'] in replace_name_dict.keys():
    name = replace_name_dict[country_dict['name']]
  else:
    name = country_dict['name']
  continent = country_dict['region']
  pop = country_dict['population']
  area = country_dict['area']
  iso_alpha_code = country_dict['alpha3Code']
  langs_list = country_dict['languages']
  languages_num = len(langs_list)
  country_entry_list = [name, continent, pop, area, languages_num, iso_alpha_code]
  all_countries.append(country_entry_list)

# 2d list of lists to DataFrame
df = pd.DataFrame(all_countries, columns=[ 'name', 'continent',  'population',
                                          'area',  'languages_num', 'iso_alpha'])

replace_happy = {
    "United States": "United States of America",
    "Taiwan Province of China": "Taiwan",
    "North Cyprus": "Cyprus",
    "Hong Kong S.A.R. of China": "Hong Kong",
    "Somaliland region": "Somalia",
    "North Macedonia": "Macedonia",
    "Palestinian Territories": "Palestine",
    "Congo (Kinshasa)": "Congo (Democratic Republic of the)",
    "Congo (Brazzaville)": "Congo",
    "Ivory Coast": "Côte d'Ivoire",
    "Somaliland Region": "Somalia",
    "Czechia": "Czech Republic",
    "Eswatini": "Swaziland",
    "State of Palestine": "Palestine",
    "Turkiye": "Turkey"
}

for key, value in replace_happy.items():
  happy_df.loc[happy_df["country"]==key, ["country"]] = value

happy_df = df.loc[df["name"].isin(happy_df['country'])][["name", "iso_alpha"]].merge(happy_df, how='left', left_on='name', right_on='country')

noodle_df_new = pd.read_html("https://instantnoodles.org/en/noodles/demand/table/")[0]
noodle_df_new = noodle_df_new.drop("Unnamed: 0", axis=1)
replace_noodle_dict = {
    "China/ Hong Kong": "China",
    "USA": "United States of America",
    "Republic of Korea": "South Korea",
    "UK": "United Kingdom",
    "Viet Nam": "Vietnam"
}
for key, value in replace_noodle_dict.items():
  noodle_df_new.loc[noodle_df_new["Country/Region"]==key, ["Country/Region"]] = value

noodle_df = df.loc[df["name"].isin(noodle_df_new['Country/Region'])][["name", "iso_alpha", "continent"]].merge(noodle_df_new, how='left', left_on='name', right_on='Country/Region')

# checking for null values
noodle_df.isnull().sum()

# dropping null values and saving to original name
noodle_df = noodle_df.dropna()

#average column
noodle_df['Avg'] = (noodle_df['2018']+noodle_df['2019']+noodle_df['2020']+noodle_df['2021']+noodle_df['2022'])/5

# percent change
noodle_df['Pct_Change'] = ((noodle_df['2022'] - noodle_df['2018']) / noodle_df['2018']) * 100

combined_df = happy_df.merge(noodle_df[['iso_alpha', 'continent']], how="inner", on="iso_alpha")
years_in_both = ["2018", "2019", "2020", "2021", "2022"]

for index, row in combined_df.iterrows():
    this_year = str(row.year)
    if this_year in years_in_both:
        noodle_value = noodle_df.loc[noodle_df.iso_alpha == row.iso_alpha, this_year].item()
        combined_df.loc[index, 'noodle_consumption'] = noodle_value
    else:
      combined_df = combined_df.drop(index)


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
