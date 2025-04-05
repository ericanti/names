import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

names_file = 'C:/Users/erica/STAT386/names.zip'

with zipfile.ZipFile(names_file, 'r') as z:
    dfs = []
    files = [file for file in z.namelist() if file.endswith('.txt')]
    for file in files:
        with z.open(file) as f:
            df = pd.read_csv(f)
            df.columns = ['name', 'sex', 'count']
            df['year'] = file[3:7]
            dfs.append(df)

names = pd.concat(dfs, ignore_index=True)

names.to_csv('names.csv', index=False)

noi = "Eric"

soi = "M"

name_df = names[(names['name'] == noi) & (names['sex'] == soi)]

name_df

plt.figure(figsize=(14, 7))
sns.lineplot(x = name_df['year'], y = name_df['count'])
plt.title(noi)
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=90, fontsize = 5)
plt.tight_layout()
plt.show()