from sklearn import linear_model
import pandas as pd
import plotly.graph_objects as go
import numpy as np


covid_file = '../data//archive/covid_de.csv'

df = pd.read_csv(covid_file)
daily_cases = df.groupby(['date'])['cases'].sum().reset_index()
wave_III = daily_cases[(daily_cases['date'] > '2021-04-01')]

X = np.arange(len(wave_III))
X = X.reshape(-1,1)

Y = wave_III['cases'].values
Y = Y.reshape(-1,1)

regr = linear_model.LinearRegression()
regr.fit(X, Y)


X_seven = np.arange(len(wave_III)+12)
X_seven = X_seven.reshape(-1,1)


for i in range(20,32):
    df_length = len(wave_III)
    wave_III.loc[df_length] = ['2021-05-'+str(i), np.nan]


y_pred = regr.predict(X_seven)


wave_III['prediction'] = y_pred.flatten()
wave_III = wave_III.reset_index()


fig = go.Figure()
fig.add_trace(go.Scatter(x=wave_III["date"], y=wave_III["cases"], name='data', mode='markers'))
fig.add_trace(go.Scatter(x=wave_III['date'], y=wave_III['prediction'], 
                         name='prediction'))

fig.update_layout(
    title={'text': 'Prediction of new daily cases (linear regression)',
           'y':0.87,
           'x':0.5,
           'xanchor': 'center',
           'yanchor': 'top'},
    autosize=False,
    xaxis_title="Date",
    yaxis_title="Cases",
    width=900,
    height=550,
    yaxis=dict(tickfont=dict(size=15), titlefont=dict(size=15)),
    xaxis=dict(titlefont=dict(size=15)),
    titlefont=dict(size=15),
    title_x=0.5
)
fig.add_vline(x='2021-05-20', line_width=2, line_dash="dash", line_color="black")
fig.add_annotation(x='2021-05-13', y=28000, text="<b>Prediction starts</b>",
                   showarrow=False, font_size=15)

fig.write_html('../plots/interactive/15_plotly_predictions.html', include_plotlyjs='cdn')
fig.show()
