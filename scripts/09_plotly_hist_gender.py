import pandas as pd
import plotly.express as px


covid_file = '../data/archive/covid_de.csv'


df = pd.read_csv(covid_file)
cases_gender_age = df.groupby(['age_group','gender'])[['cases']].sum().reset_index()


fig = px.bar(cases_gender_age, x="age_group", y="cases",color="gender")
fig.update_xaxes(type='category')

fig.update_layout(
    title='Total number of COVID-19 cases by age',
    autosize=False,
    xaxis_title="Age group",
    yaxis_title="Number of cases",
    width=800,
    height=500,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    xaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    legend = dict(font = dict(size = 15)),
    legend_title = dict(font = dict(size = 15)),
    titlefont=dict(size=15),
    title_x=0.5
             )
fig.write_html('../plots/interactive/09_plotly_hist_gender.html', include_plotlyjs='cdn')
fig.show()