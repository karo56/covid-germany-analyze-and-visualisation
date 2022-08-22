import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv('../data/2020_DE_Region_Mobility_Report.csv')

mobility = df.groupby(['date'])['retail_and_recreation_percent_change_from_baseline'
, 'grocery_and_pharmacy_percent_change_from_baseline'
, 'parks_percent_change_from_baseline'
, 'transit_stations_percent_change_from_baseline'
, 'workplaces_percent_change_from_baseline'
, 'residential_percent_change_from_baseline'].mean().reset_index()

mobility = mobility.rename(columns={"date": "date"
    , "retail_and_recreation_percent_change_from_baseline": "retail and recreation"
    , "grocery_and_pharmacy_percent_change_from_baseline": "grocery and pharmacy"
    , "parks_percent_change_from_baseline": "parks"
    , "transit_stations_percent_change_from_baseline": "transit stations"
    , "workplaces_percent_change_from_baseline": "workplaces"
    , "residential_percent_change_from_baseline": "residential"})

fig = go.Figure()

things_to_plot = ['retail and recreation',
                  'grocery and pharmacy',
                  'parks',
                  'transit stations',
                  'workplaces',
                  'residential']


i = 0
for element in things_to_plot:
    fig.add_trace(go.Scatter(x=mobility['date'], y=mobility[element], name=element))
    vis = [False] * len(things_to_plot)
    vis[i] = True
    i += 1

fig.update_layout(
    title={'text': 'Mobility in Germany during pandemic',
           'y': 0.88,
           'x': 0.5,
           'xanchor': 'center',
           'yanchor': 'top'},
    autosize=False,
    xaxis_title="Date",
    yaxis_title="Change",
    width=900,
    height=550,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    xaxis=dict(titlefont=dict(size=15)),
    titlefont=dict(size=15),
    title_x=0.5
)

fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y",
    ticks="outside")
fig.add_hline(y=0, line_width=2)
fig.update_yaxes(ticks="outside")
fig.write_html('../plots/interactive/13_plotly_mobility.html', include_plotlyjs='cdn')
fig.show()