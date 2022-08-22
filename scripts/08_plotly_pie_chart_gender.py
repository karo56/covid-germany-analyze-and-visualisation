import pandas as pd
import plotly.express as px


covid_file = '../data/archive/covid_de.csv'


df = pd.read_csv(covid_file)
cases_gender = df.groupby(['gender'])[['cases']].sum().reset_index()


fig = px.pie(cases_gender, values='cases', names='gender')

fig.update_layout(
    title='Total number of COVID-19 cases by gender',
    autosize=False,
    width=900,
    height=500,
    titlefont=dict(size=18),
    font=dict(size=18),
    title_x=0.5,
    legend=dict(x=0.41, y=-0.1, font=dict(size=15)),
    legend_orientation="h"
             )
fig.write_html('../plots/interactive/08_plotly_pie_chart_gender.html', include_plotlyjs='cdn')
fig.show()