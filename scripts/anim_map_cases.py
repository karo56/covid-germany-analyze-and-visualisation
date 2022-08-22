import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import numpy as np 
import matplotlib
import warnings
import geopandas as gpd
warnings.filterwarnings("ignore")


lands = gpd.read_file('../data/archive/de_state.shp')
lands.drop(columns=['ADE', 'RS', 'RS_0'], inplace=True)
lands['GEN'] = lands['GEN'].str.replace(u"ü", "ue")

df = pd.read_csv('../data/archive/covid_de.csv')
days = list(df.groupby(['date'])['cases'].sum().index)
daily_cases = df.groupby(['date', 'state'])['cases'].sum().reset_index()

df = pd.read_csv('../data/archive/demographics_de.csv')
df = df.groupby(['state'])['population'].sum().reset_index()
population = {}
for index, row in df.iterrows():
    population[row['state']] = row['population']

daily_cases['cases_per_100k'] = daily_cases['state'].map(population)
daily_cases['cases_per_100k'] = daily_cases['cases'] / daily_cases['cases_per_100k'] * 100000
daily_cases.set_index('state', inplace=True)


fig, axes = plt.subplots(1, 2, figsize=(10,6))
last7_100 = []
last7 = []
time_interval = 0

def anim_frame(day):
    global last7
    global last7_100
    global time_interval
    plt.clf()
    plt.suptitle('Covid-19 cases (7-day moving average)\n'+ day)
    land_cases = lands.join(daily_cases[daily_cases['date']==day][['cases','cases_per_100k']], on='GEN').fillna(0)
    last7_100.append(land_cases['cases_per_100k'])
    last7.append(land_cases['cases'])
    if len(last7)==8:
        last7 = last7[1:]
        last7_100 = last7_100[1:]
    last7_matrix = np.array(last7)
    last7_100_matrix = np.array(last7_100)
    land_cases['cases_avg'] = np.mean(last7_matrix, axis=0)
    land_cases['cases_per_100k_avg'] = np.mean(last7_100_matrix, axis=0)
    ax = plt.subplot(121)
    land_cases.plot(column='cases_avg', ax=ax, legend=True,
                    cmap='magma_r', edgecolor='black', linewidth=0.5,
                    norm=matplotlib.colors.PowerNorm(gamma=0.5, vmin=0, vmax=7000))
    ax.set_axis_off()
    ax.annotate('Cases', xy=(0.5, -0.05), xycoords='axes fraction', ha='center')
    ax = plt.subplot(122)
    land_cases.plot(column='cases_per_100k_avg', ax=ax, legend=True,
                    cmap='magma_r', edgecolor='black', linewidth=0.5,
                    norm=matplotlib.colors.PowerNorm(gamma=0.5, vmin=0, vmax=100))
    ax.set_axis_off()
    ax.annotate('Cases per 100k inhabitants', xy=(0.5, -0.05), xycoords='axes fraction', ha='center')
    if day in ['2020-03-09', '2020-05-01', '2020-10-01', '2021-02-01', '2021-03-10']:
        time_interval+=1
    if time_interval==1:
        ax.annotate('I wave', xy=(-0.2, -0.2), xycoords='axes fraction', ha='center', fontsize='large', fontfamily='serif')
    elif time_interval==3:
        ax.annotate('II wave', xy=(-0.2, -0.2), xycoords='axes fraction', ha='center', fontsize='large', fontfamily='serif')
    elif time_interval==5:
        ax.annotate('III wave', xy=(-0.2, -0.2), xycoords='axes fraction', ha='center', fontsize='large', fontfamily='serif')

anim = animation.FuncAnimation(fig, func=anim_frame, frames=days)

anim.save('../plots/animated/map_cases.gif',writer='imagemagick', fps=10, dpi=100)
plt.close()