import numpy as np
import pandas as pd
import plotly.express as px


covid_file = '../data/archive/covid_de.csv'


df = pd.read_csv(covid_file)


daily_cases = df.groupby(['date'])['cases'].sum().reset_index()
cases_avg = [0]
for i in range(1,len(daily_cases['cases'])):
    cases_avg.append(np.mean(daily_cases['cases'][max(0,i-7):i]))


growth = [0]
for i in range (1,len(cases_avg)):
    if cases_avg[i-7] == 0:
        growth.append(cases_avg[i] / cases_avg[i-8])
    else:
        growth.append(cases_avg[i]/cases_avg[i-7])
daily_cases['growth'] = growth
daily_cases = daily_cases[(daily_cases['date'] >= '2020-04-01')]



fig = px.line(daily_cases, x='date', y='growth')

fig.update_layout(
    title='Growth factor of daily new cases in Germany',
    autosize=False,
    xaxis_title="Date",
    yaxis_title="Growth factor",
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
fig.add_hline(y=1, line_width=2, line_dash="dash", line_color="red")
fig.add_annotation(x='2020-05-01',
                   y=1.005,
                   text="no growth",
                   arrowhead=1,
                   arrowwidth=1.5,
                   arrowcolor='red',
                   font_size=14,
                   font_color="red",
                   align="right")
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")

fig.write_html('../plots/interactive/05_plotly_growth_factor.html', include_plotlyjs='cdn')
fig.show()