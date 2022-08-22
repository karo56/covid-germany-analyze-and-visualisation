import pandas as pd
import plotly.express as px


covid_file = '../data/archive/covid_de.csv'

df = pd.read_csv(covid_file)
daily_deaths = df.groupby(['date'])['deaths'].sum().reset_index()
daily_deaths['deaths'] = daily_deaths['deaths'].cumsum()


fig = px.line(daily_deaths, x='date', y='deaths')

fig.update_layout(
    title='Total number of COVID-19 deaths in Germany',
    autosize=False,
    xaxis_title="Date",
    yaxis_title="Deaths",
    width=900,
    height=500,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    titlefont=dict(size=15),
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

fig.write_html('../plots/interactive/02_plotly_total_deaths.html', include_plotlyjs='cdn')
fig.show()