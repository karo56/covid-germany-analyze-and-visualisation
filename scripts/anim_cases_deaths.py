import matplotlib.pyplot as plt
import matplotlib.animation as animation
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


fig, ax = plt.subplots(figsize=(9,5))

locator = mdates.MonthLocator()
formatter = mdates.DateFormatter('%b')

def anim_frame(day, data):
    plt.clf()
    ax = plt.subplot()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    
    plt.ylim(-1000, 36000)
    plt.xlim(datetime.date(2020,1,1), datetime.date(2021,6,1))
    plt.yticks(range(0,36000,5000), [str(int(t/1000))+'k' for t in range(0,36000,5000)])
    plt.title('Daily cases and deaths')
    plt.ylabel('Number of cases/deaths')
    plt.xlabel('Date')
    d = data[data['date'] <= day]
    plt.plot(d.date, d.deaths, label='deaths', c='tab:red', linewidth=2)
    plt.plot(d.date, d.cases_avg, label='cases (7-day moving average)', c='tab:blue', linewidth=2)
    plt.plot(d.date, d.cases, label='cases', c='tab:blue', alpha=0.4, linewidth=2)
    plt.legend(loc=(0.02,0.75))
    plt.annotate('2020', xy=(datetime.date(2020,1,1), -4600), annotation_clip=False, ha='center')
    plt.annotate('2021', xy=(datetime.date(2021,1,1), -4600), annotation_clip=False, ha='center')

anim = animation.FuncAnimation(fig, func=anim_frame, frames=df['date'], fargs=(df,))

anim.save('../plots/animated/cases_deaths.gif',writer='imagemagick', fps=24, dpi=150)
plt.close()
