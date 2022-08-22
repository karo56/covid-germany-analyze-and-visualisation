import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


covid_file = '../data/archive/covid_de.csv'

df = pd.read_csv(covid_file)

daily_cases = df.groupby(['date'])['cases'].sum().reset_index()

# df = daily_cases[(daily_cases['date'] >= 99) & (daily_cases['date'] <= 101)]
fala_I = daily_cases[(daily_cases['date'] < '2020-05-01')]
fala_I['date'] = 'I'

fala_II = daily_cases[(daily_cases['date'] >= '2020-10-01') & (daily_cases['date'] < '2021-02-01')]
fala_II['date'] = 'II'

fala_III = daily_cases[(daily_cases['date'] > '2021-03-01')]
fala_III['date'] = 'III'

to_plot = pd.concat([fala_I, fala_II, fala_III])
to_plot = to_plot.rename(columns={"date": "wave"})


plt.figure(figsize=(7, 5))
sns.set_theme(style='whitegrid')
sns_plot = sns.boxplot(x="wave", y="cases",data=to_plot).set_title("Distribution for waves")
sns.set(font_scale = 1)
plt.yticks(range(0,35001,5000), [str(int(t/1000))+'k' for t in range(0,35001,5000)])
plt.xlabel('Waves')
plt.ylabel('Number of cases')
plt.savefig('../plots/static/box_plot.png', dpi=150, bbox_inches='tight')