import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv('../data/containment_health_index.csv', index_col=0)
data = pd.DataFrame(index=pd.date_range(start="2020-01-10",end="2021-05-14"))
data['Germany_index'] = df[df['country_name']=='Germany'].iloc[0,11:-6]
data['Poland_index'] = df[df['country_name']=='Poland'].iloc[0,11:-6]

df = pd.read_csv('../data/CONVENIENT_global_confirmed_cases.csv', index_col=0, header=[0,1])
df.index = pd.to_datetime(df.index)
cases = pd.DataFrame()
countries = ['Germany', 'Poland']
population = {'Germany':84.01*10**6, 'Poland':37.81*10**6}
countries_col = [(country,'nan') for country in countries]
cases = df[countries_col].droplevel(1, axis=1)
for country in countries:
    cases[country] = cases[country]/population[country]*100000
data = data.join(cases).fillna(0)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=data.index, y=data['Poland_index'], mode='lines', name='Poland index', 
                         line_color='red'), secondary_y=True)
fig.add_trace(go.Scatter(x=data.index, y=data['Germany_index'], mode='lines', name='Germany index', 
                         line_color='blue'), secondary_y=True)
fig.add_trace(go.Bar(x=data.index, y=data['Poland'], width=2e8, name='Poland cases', 
                     marker_color='red'), secondary_y=False)
fig.add_trace(go.Bar(x=data.index, y=data['Germany'], width=2e8, name='Germany cases', 
                     marker_color='blue'), secondary_y=False)
fig.update_traces(marker_line_width=0, opacity=0.5, secondary_y=False)


fig.update_layout(
    title='Impact of restrictions on number of new Covid-19 cases',
    autosize=False,
    xaxis_title='Date',
    yaxis_title='Number of cases per 100k inhabitants',
    legend_title_text='',
    legend = dict(font = dict(size = 15)),
    legend_title = dict(font = dict(size = 15)),
    width=900,
    height=500,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    titlefont=dict(size=18),
    title_x=0.5,
    xaxis=dict(titlefont=dict(size=15),
               rangeselector=dict(buttons=list([
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
fig.update_yaxes(range=[0,95],secondary_y=False)
fig.update_yaxes(dict(tickfont=dict(size=15), titlefont=dict(size=15)),range=[0,95],
                 title_text="Containment and health index", secondary_y=True)

fig.write_html('../plots/interactive/plotly_restrictions.html', include_plotlyjs='cdn')
fig.show()
