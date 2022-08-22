import pandas as pd
import plotly.graph_objects as go


vaccines_file = '../data/archive/covid_de_vaccines.csv'


df = pd.read_csv(vaccines_file)
df = df.rename(columns={"pfizer_cumul": "pfizer", "astrazeneca_cumul": "astrazeneca", "moderna_cumul": "moderna"})


df['pfizer_new'] = df['pfizer'] + df['astrazeneca'] + df['moderna']
df['astrazeneca_new'] = df['astrazeneca'] + df['moderna']


df = df.drop(['pfizer', 'astrazeneca'], axis=1)

df = df.rename(columns={"pfizer_new": "pfizer", "astrazeneca_new": "astrazeneca"})
fig = go.Figure()

things_to_plot = ['pfizer', 'astrazeneca', 'moderna']

for element in things_to_plot:
    fig.add_trace(go.Scatter(x=df['date'], y=df[element], fill='tozeroy', name=element))
fig.update_layout(
    title='Total number of COVID-19 vaccinations in Germany',
    autosize=False,
    xaxis_title="Date",
    yaxis_title="Number of vaccines",
    width=900,
    height=500,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    titlefont=dict(size=15),
    title_x=0.5,
    xaxis=dict(tickfont=dict(size=15),
               titlefont=dict(size=15),
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
fig.write_html('../plots/interactive/06_plotly_vaccinations.html', include_plotlyjs='cdn')
fig.show()