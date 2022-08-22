import pandas as pd
import plotly.express as px


covid_file = '../data/archive/covid_de.csv'


df = pd.read_csv(covid_file)

df_demographics = pd.read_csv('../data/archive/demographics_de.csv')


cases_gender_age = df.groupby(['age_group'])[['cases','deaths']].sum().reset_index()


age_demographic = df_demographics.groupby(['age_group'])[['population']].sum().reset_index()
age_demographic = age_demographic.drop(['age_group'], axis=1)

demographic_and_cases = pd.concat([cases_gender_age, age_demographic], axis=1)
demographic_and_cases['percent_infected'] = demographic_and_cases['cases'] / demographic_and_cases['population'] * 100
demographic_and_cases['percent_death'] = demographic_and_cases['deaths'] / demographic_and_cases['population'] * 100



fig = px.bar(demographic_and_cases, x="age_group", y=["percent_infected",'percent_death'])
fig.update_xaxes(type='category')

fig.update_layout(
    title='Percentage of COVID-19 cases and deaths by age',
    autosize=False,
    xaxis_title="Age group",
    yaxis_title="Percentage",
    width=900,
    height=500,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    xaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    titlefont=dict(size=15),
    title_x=0.5,
    legend = dict(font = dict(size = 13)),
    legend_title = dict(font = dict(size = 13))
             )
fig.write_html('../plots/interactive/11_plotly_hist_percent.html', include_plotlyjs='cdn')
fig.show()