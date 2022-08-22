import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import warnings
warnings.filterwarnings("ignore")


df = pd.read_csv('../data/archive/covid_de.csv')
data = df.groupby(['date'])['cases'].sum().reset_index()
data = data[data['date']>='2021-01-01']
data.index = pd.DatetimeIndex(data['date']).to_period('D')

model = ARIMA(data.cases, order=(10,1,1))
model_fit = model.fit()
fcast = model_fit.get_forecast(61).summary_frame()
predictions = model_fit.predict(start=0, end=len(data)+60)


data['date'] = list(data['date'].to_timestamp())

fig = go.Figure()
fig.add_trace(go.Scatter(x=data.date, y=data.cases, name='data', line=dict(width=4)))
fig.add_trace(go.Scatter(x=predictions.index.to_timestamp(), y=list(predictions), 
                         name='prediction'))

fig.add_trace(go.Scatter(x=pd.date_range(start='2021-05-20', end='2021-07-19'), 
                         y=fcast['mean_ci_lower'], line_color='grey', 
                         showlegend=False, name='95% confidence interval'))
fig.add_trace(go.Scatter(x=pd.date_range(start='2021-05-20', end='2021-07-19'), 
                         y=fcast['mean_ci_upper'], fill='tonexty', line_color='grey', 
                         name='95% confidence interval'))

fig.update_layout(
    title={'text': 'Prediction of new daily cases (ARIMA)',
           'y':0.87,
           'x':0.5,
           'xanchor': 'center',
           'yanchor': 'top'},
    hoverlabel=dict(bgcolor="white"),
    autosize=False,
    xaxis_title="Date",
    yaxis_title="Cases",
    width=900,
    height=550,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    xaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    titlefont=dict(size=15),
    title_x=0.5,
    legend=dict(font=dict(size=13))
)
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y")

fig.add_vline(x='2021-05-20', line_width=2, line_dash="dash", line_color="black")
fig.add_annotation(x='2021-04-25', y=-15000, text="<b>Prediction starts</b>",
                   showarrow=False, font_size=15)

fig.write_html('../plots/interactive/plotly_predicitons.html', include_plotlyjs='cdn')
fig.show()