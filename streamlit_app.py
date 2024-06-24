import streamlit as st
import pandas as pd
## Requests is the default library for asking python to talk to the web
import numpy as np
import requests
## PPrint is 'Pretty Print' Which lets us print less offensive JSON
from pprint import pprint

import matplotlib.pyplot as plt # visualisation!

import plotly.express as px
import plotly.graph_objects as go

st.title("Pokemon Research Centre")

pokemon_number = st.sidebar.text_input("Enter Pokemon ID / Name", "1")

url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number}/'
response = requests.get(url)
pokemon = response.json()

poke_name = pokemon['name']
poke_image = pokemon['sprites']['front_default']
poke_audio = pokemon['cries']['latest']
poke_height = pokemon["height"]
poke_weight = pokemon["weight"]
poke_exp = pokemon["base_experience"]
poke_species = [x["type"]["name"] for x in pokemon["types"]]
poke_image_other = pokemon['sprites']['other']["official-artwork"]["front_default"]
pokemon_stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon["stats"]}

st.title(poke_name.title())
# Creating columns with a small gap
col1, col2 = st.columns(2, gap="small")
with col1:
    col1.write('Abilities')  # dm for decimeters
    for i in poke_species:
        col1.subheader(i.title())
    
with col2:
    st.metric(label="Height", value=f"{poke_height} m")  # dm for decimeters
    st.metric(label="Weight", value=f"{poke_weight} kg")  # hg for hectograms


#st.write(poke_exp)
st.audio(poke_audio)
#st.image(poke_image_other)

stats_container = st.container(border = True)
col1, col2, col3= stats_container.columns(3)
col1.image(poke_image_other, width = 220)
# Loop through the dictionary and add stats to col1 and col2 alternately
for i, (stat, val) in enumerate(pokemon_stats.items()):
    if i % 2 == 0:
        col2.metric(label=stat.capitalize(), value=val)
    else:
        col3.metric(label=stat.capitalize(), value=val)


#stats chart 
# Create a polar plot with Plotly

st.header('Radar Chart of Base Stats')
# Mapping the stats to the desired column names
stats_mapping = {
    'hp': 'HP',
    'attack': 'Attack',
    'defense': 'Defense',
    'special-attack': 'Special Attack',
    'special-defense': 'Special Defense',
    'speed': 'Speed'
}


# Create a DataFrame with the mapped stats
df_stats = pd.DataFrame([pokemon_stats]).rename(columns=stats_mapping)

# Melt the DataFrame for Plotly polar plot
df_stats_melted = df_stats.melt(var_name='Stat', value_name='Value')

# Add a column for Pokemon name
df_stats_melted['Pokemon'] = poke_name

def plotRadar():
    # use plotly express to plot out radar char of stats
    fig = px.line_polar(df_stats_melted, r='Value', theta='Stat', line_close=True, range_r=[0, 250],color='Pokemon')
    st.plotly_chart(fig)

plotRadar()

#st.write(df_stats_melted)
pokemon_number2 = st.text_input(f"Compare {poke_name.title()} with:", placeholder = "Enter Pokemon ID / Name")

if pokemon_number2:
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_number2}/'
    response2 = requests.get(url)
    pokemon2 = response2.json()
    poke_name2 = pokemon2['name']
    pokemon_stats2 = {stat['stat']['name']: stat['base_stat'] for stat in pokemon2["stats"]}
    # Create a DataFrame with the mapped stats
    df_stats2 = pd.DataFrame([pokemon_stats2]).rename(columns=stats_mapping)

    # Melt the DataFrame for Plotly polar plot
    df_stats_melted2 = df_stats2.melt(var_name='Stat', value_name='Value')

    # Add a column for Pokemon name
    df_stats_melted2['Pokemon'] = poke_name2

    # Concatenate DataFrames for both Pokemon
    df_stats_melted = pd.concat([df_stats_melted, df_stats_melted2])
    
    plotRadar()

