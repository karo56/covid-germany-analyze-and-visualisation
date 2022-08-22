import pandas as pd
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt


covid_file = '../data//archive/covid_de.csv'


df = pd.read_csv(covid_file)
cases_gender_age = df.groupby(['age_group'])[['cases','deaths']].sum().reset_index()



def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)


fig, ax = plt.subplots(figsize=(7, 4.5))
ax.set_title("COVID-19 cases and deaths by age")
ax.bar(cases_gender_age['age_group'], cases_gender_age['cases'], color='b', label='cases')
ax.bar(cases_gender_age['age_group'], cases_gender_age['deaths'], bottom=cases_gender_age['cases'], color='r', label='deaths')

ax.set_xlabel('Age group')
ax.set_ylabel('Number of cases')

formatter = FuncFormatter(millions)

ax.yaxis.set_major_formatter(formatter)
ax.legend(prop={'size': 10}, loc='upper left')
plt.savefig('../plots/static/bar_covid_cases.png', dpi=150, bbox_inches='tight')
plt.show()