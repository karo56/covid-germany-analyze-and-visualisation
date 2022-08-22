import pandas as pd

import matplotlib.pyplot as plt

covid_file = '../data/archive/covid_de.csv'

df = pd.read_csv(covid_file)
df_demographics = pd.read_csv('../data/archive/demographics_de.csv')


cases_gender_age = df.groupby(['age_group'])[['cases','deaths']].sum().reset_index()

age_demographic = df_demographics.groupby(['age_group'])[['population']].sum().reset_index()
age_demographic = age_demographic.drop(['age_group'], axis=1)

demographic_and_cases = pd.concat([cases_gender_age, age_demographic], axis=1)
demographic_and_cases['percent_infected'] = demographic_and_cases['cases'] / demographic_and_cases['population'] * 100
demographic_and_cases['percent_death'] = demographic_and_cases['deaths'] / demographic_and_cases['population'] * 100


def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x * 1e-6)


fig, ax = plt.subplots(figsize=(7, 4.5))
ax.set_title("Percentage of COVID-19 cases and deaths by age")
ax.bar(demographic_and_cases['age_group'], demographic_and_cases['percent_infected'], color='b', label='cases')
ax.bar(demographic_and_cases['age_group'], demographic_and_cases['percent_death'], bottom=demographic_and_cases['percent_infected'], color='r', label='deaths')
ax.set_xlabel('Age group')
ax.set_ylabel('Percent of cases/deaths')
ax.legend(prop={'size': 10}, loc='upper left')
plt.savefig('../plots/static/bar_covid_perc.png', dpi=150, bbox_inches='tight')
plt.show()
