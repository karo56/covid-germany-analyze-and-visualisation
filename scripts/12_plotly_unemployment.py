import pandas as pd
import plotly.express as px


df = pd.read_csv('../data/unemployment.csv')
df = df.loc[df['LOCATION'] == 'DEU']
df = df.loc[df['TIME'] > '2015']

daily_unemployment = df.groupby(['TIME'])['Value'].mean().reset_index()


fig = px.line(daily_unemployment, x='TIME', y='Value')

fig.update_layout(
    title='Unemployment in Germany',
    autosize=False,
    width=900,
    height=500,
    xaxis_title="Date",
    yaxis_title="Unemployment rate",
    yaxis=dict(tickfont=dict(size=13),
               titlefont=dict(size=15),
               ticksuffix="%"),
    titlefont=dict(size=15),
    title_x=0.5,
    yaxis_range=[0,5.5],
    xaxis=dict(tickfont=dict(size=13),
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
fig.update_xaxes(ticks="outside")
fig.update_yaxes(ticks="outside")
fig.add_vline(x='2020-03', line_width=3, line_dash="dash", line_color="red")
fig.add_annotation(x='2019-08', y=4.8,
            text="<b>Pandemic starts</b>",
            showarrow=False,
            arrowhead=1,
                   font_size=15
                  )
fig.write_html('../plots/interactive/12_plotly_unemployment.html', include_plotlyjs='cdn')
fig.show()