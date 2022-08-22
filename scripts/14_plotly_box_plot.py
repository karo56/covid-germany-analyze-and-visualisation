import pandas as pd
import plotly.express as px


covid_file = '../data/archive/covid_de.csv'


df = pd.read_csv(covid_file)
daily_cases = df.groupby(['date'])['cases'].sum().reset_index()


# I from 01.03.2020 to 1.05.2020
# II from 1.10.2020 to  1.02.2021
# III from  10.03.2021


# df = daily_cases[(daily_cases['date'] >= 99) & (daily_cases['date'] <= 101)]
fala_I = daily_cases[(daily_cases['date'] < '2020-05-01')]
fala_I['date'] = 'I'

fala_II = daily_cases[(daily_cases['date'] >= '2020-10-01') & (daily_cases['date'] < '2021-02-01')]
fala_II['date'] = 'II'

fala_III = daily_cases[(daily_cases['date'] > '2021-03-10')]
fala_III['date'] = 'III'

to_plot = pd.concat([fala_I, fala_II, fala_III])
to_plot = to_plot.rename(columns={"date": "wave"})


fig = px.box(to_plot,x='wave', y="cases", points="all", color="wave")
fig.update_layout(
    title={'text': 'Distribution for waves',
           'y':0.95,
           'x':0.5,
           'xanchor': 'center',
           'yanchor': 'top'},
    autosize=False,
    xaxis_title="Wave",
    yaxis_title="Cases",
    width=900,
    height=550,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    xaxis=dict(titlefont=dict(size=15)),
    titlefont=dict(size=15),
    title_x=0.5
)
fig.write_html('../plots/interactive/14_plotly_box_plot.html', include_plotlyjs='cdn')
fig.show()