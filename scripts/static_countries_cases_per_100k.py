import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import matplotlib.dates as mdates
import datetime


df = pd.read_csv('../data/CONVENIENT_global_confirmed_cases.csv', index_col=0, header=[0,1])
df.index = pd.to_datetime(df.index)
data = pd.DataFrame()
countries = ['Germany', 'Poland', 'United Kingdom', 'Italy']
population = {'Germany':84.01*10**6, 'Poland':37.81*10**6, 'United Kingdom':68.2*10**6, 'Italy':60.39*10**6}
countries_col = [(country,'nan') for country in countries]
data = df[countries_col].droplevel(1, axis=1)
for country in countries:
    data[country] = data[country]/population[country]*100000
data = data.cumsum()


plt.style.use('default')
fig, ax = plt.subplots(figsize=(7,4))

locator = mdates.MonthLocator()
formatter = mdates.DateFormatter('%b')

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

colors = ['tab:red','tab:green','tab:blue','tab:orange']

for i in range(4):
    country = countries[i]
    ax.plot(data[country], label=country, alpha=0.8, linewidth=2, c=colors[i])
plt.yticks(range(0,7001,1000), [str(int(t/1000))+'k' for t in range(0,7001,1000)])

ax.annotate('2020', xy=(datetime.date(2020,2,1), -1400), annotation_clip=False, ha='center')
ax.annotate('2021', xy=(datetime.date(2021,1,1), -1400), annotation_clip=False, ha='center')
plt.legend(loc=(0.02,0.7))
    
plt.title('Total number of Covid-19 cases per 100k inhabitants')
plt.ylabel('Number of cases')
plt.grid()
plt.savefig('../plots/static/countries_cases_per_100k.png', dpi=150, bbox_inches='tight')
plt.close()