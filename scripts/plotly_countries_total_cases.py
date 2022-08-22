import pandas as pd
import matplotlib.dates as mdates
import plotly.express as px
import datetime


df = pd.read_csv('../data/CONVENIENT_global_confirmed_cases.csv', index_col=0, header=[0,1])
df.index = pd.to_datetime(df.index)
data = pd.DataFrame()
countries = ['Germany', 'Poland', 'United Kingdom', 'Italy']
population = {'Germany':84.01*10**6, 'Poland':37.81*10**6, 'United Kingdom':68.2*10**6, 'Italy':60.39*10**6}
countries_col = [(country,'nan') for country in countries]
data = df[countries_col].droplevel(1, axis=1)
for country in countries:
    data[country] = data[country]/population[country]*100000
data = data.cumsum()
fig = px.line(data, x=data.index, y=countries,
              color_discrete_sequence=px.colors.qualitative.G10)

fig.update_layout(
    hoverlabel=dict(bgcolor="white"),
    title='Total number of Covid-19 cases per 100k inhabitants',
    autosize=False,
    xaxis_title='Date',
    yaxis_title='Number of cases',
    legend_title_text='Country',
    legend = dict(font = dict(size = 15)),
    legend_title = dict(font = dict(size = 15)),
    width=900,
    height=500,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    titlefont=dict(size=18),
    title_x=0.5,
    xaxis=dict(titlefont=dict(size=15),
               rangeselector=dict(buttons=list([
                          dict(count=7,
                               label="1w",
                               step="day",
                               stepmode="backward"),
                          dict(count=14,
                               label="2w",
                               step="day",
                               stepmode="backward"),
                          dict(count=1,
                               label="1m",
                               step="month",
                               stepmode="backward"),
                          dict(count=2,
                               label="2m",
                               step="month",
                               stepmode="backward"),
                          dict(count=3,
                               label="3m",
                               step="month",
                               stepmode="backward"),
                          dict(count=6,
                               label="6m",
                               step="month",
                               stepmode="backward"),
                          dict(step="all")
                      ])
                                 )
))
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")

fig.write_html('../plots/interactive/plotly_countries_total_cases.html', include_plotlyjs='cdn')
fig.show()