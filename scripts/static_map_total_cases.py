import matplotlib.pyplot as plt
import matplotlib.colors
import geopandas as gpd
import pandas as pd

lands = gpd.read_file('../data/archive/de_state.shp')
lands.drop(columns=['ADE', 'RS', 'RS_0'], inplace=True)
lands['GEN'] = lands['GEN'].str.replace(u"ü", "ue")

df = pd.read_csv('../data/archive/covid_de.csv')
data = df.groupby(['date', 'state'])['cases'].sum().reset_index()
data = data.groupby(['state'])['cases'].sum().reset_index()

df = pd.read_csv('../data/archive/demographics_de.csv')
df = df.groupby(['state'])['population'].sum().reset_index()
population = {}
for index, row in df.iterrows():
    population[row['state']] = row['population']
data['cases'] = data['cases']
data['cases_per_100k'] = data['state'].map(population)
data['cases_per_100k'] = data['cases'] / data['cases_per_100k'] * 100000
data.set_index('state', inplace=True)

land_cases = lands.join(data[['cases','cases_per_100k']], on='GEN').fillna(0)
ax = land_cases.plot(column='cases_per_100k', legend=True,
                legend_kwds=dict(label="Cases per 100k inhabitants",
                                 orientation="vertical", shrink=0.9),
                cmap='magma_r', edgecolor='black', linewidth=0.5,
                figsize=(5,5), vmax=7000)

plt.title('Number of confirmed cases by state', size=12)
plt.axis('off')
plt.savefig('../plots/static/map_total_cases.png', dpi=150)
plt.close()