import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import matplotlib.dates as mdates
import datetime


df = pd.read_csv('../data/archive/covid_de.csv')
df = df.groupby(['date'])[['cases','deaths']].sum().reset_index()
df['date'] = pd.to_datetime(df['date'])

cases_avg = [0]
for i in range(1,len(df['cases'])):      
    cases_avg.append(np.mean(df['cases'][max(0,i-7):i]))

df['cases_avg'] = cases_avg


plt.style.use('default')
fig, ax = plt.subplots(figsize=(7,4))

locator = mdates.MonthLocator()
formatter = mdates.DateFormatter('%b')

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)


ax.plot(df.date, df.deaths, label='deaths', c='tab:red')
ax.plot(df.date, df.cases_avg, label='cases (7-day moving average)', c='tab:blue')
ax.plot(df.date, df.cases, label='cases', c='tab:blue', alpha=0.4)
plt.yticks(range(0,35001,5000), [str(int(t/1000))+'k' for t in range(0,35001,5000)])


ax.annotate('2020', xy=(datetime.date(2020,1,1), -6000), annotation_clip=False, ha='center')
ax.annotate('2021', xy=(datetime.date(2021,1,1), -6000), annotation_clip=False, ha='center')
plt.legend(loc=(0.02,0.75))
plt.grid()

plt.title('Number of daily Covid-19 cases and deaths')
plt.ylabel('Number of cases/deaths')

plt.savefig('../plots/static/cases_deaths.png', dpi=150, bbox_inches='tight')
plt.close()