import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
import streamlit as st

## LOAD DATA DIRECTLY FROM SS WEBSITE
@st.cache_data
def load_name_data():
    names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
    response = requests.get(names_file)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        dfs = []
        files = [file for file in z.namelist() if file.endswith('.txt')]
        for file in files:
            with z.open(file) as f:
                df = pd.read_csv(f, header=None)
                df.columns = ['name','sex','count']
                df['year'] = int(file[3:7])
                dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
    return data

df = load_name_data()

print(df)

df['total_births'] = df.groupby(['year', 'sex'])['count'].transform('sum')
df['prop'] = df['count'] / df['total_births']

st.title('My Name App')

tab1, tab2, tab3 = st.tabs(['Overall', 'By Name', 'By Year'])

with tab1:
    st.write('Here is stuff about all the data')

    # Group by year and sex, then count unique names
    unique_names_by_gender = df.groupby(['year', 'sex'])['name'].nunique().reset_index()

    # Plot
    fig = plt.figure(figsize=(10, 5))

    for gender in ['F', 'M']:
        gender_data = unique_names_by_gender[unique_names_by_gender['sex'] == gender]
        plt.plot(gender_data['year'], gender_data['name'], label='Female' if gender == 'F' else 'Male')

    plt.title('Number of Unique Baby Names per Year by Gender')
    plt.xlabel('Year')
    plt.ylabel('Unique Names')
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)

    top_names = df.groupby(['name', 'sex'])['count'].sum().reset_index()
    top_names = top_names.sort_values('count', ascending=False).groupby('sex').head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_names, x='count', y='name', hue='sex', ax=ax)
    ax.set_title('Top 10 Names of All Time by Sex')
    ax.set_xlabel('Total Count')
    ax.set_ylabel('Name')
    st.pyplot(fig)

with tab2:
    st.write('Name')

    # pick a name
    noi = st.text_input('Enter a name')
    plot_female = st.checkbox('Plot female line')
    plot_male = st.checkbox('Plot male line')
    name_df = df[df['name']==noi]

    fig = plt.figure(figsize=(15, 8))

    if plot_female:
        sns.lineplot(data=name_df[name_df['sex'] == 'F'], x='year', y='prop', label='Female')

    if plot_male:
        sns.lineplot(data=name_df[name_df['sex'] == 'M'], x='year', y='prop', label='Male')

    plt.title(f'Popularity of {noi} over time')
    plt.xlim(1880, 2025)
    plt.xlabel('Year')
    plt.ylabel('Proportion')
    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()

    st.pyplot(fig)

with tab3:
    st.write('Year')

    year_of_interest = st.text_input('Enter a year')
    top_names = df[df['year'] == int(year_of_interest)]
    top_female = top_names[top_names['sex'] == 'F'].nlargest(10, 'count')

    fig = plt.figure(figsize=(15, 8))
    sns.barplot(data=top_female, x='count', y='name')
    plt.title(f"Top 10 Female Names in {year_of_interest}")
    plt.xlabel('Count')
    plt.ylabel('Name')
    plt.tight_layout()
    st.pyplot(fig)

    top_male = top_names[top_names['sex'] == 'M'].nlargest(10, 'count')

    fig = plt.figure(figsize=(15, 8))
    sns.barplot(data=top_male, x='count', y='name')
    plt.title(f"Top 10 Male Names in {year_of_interest}")
    plt.xlabel('Count')
    plt.ylabel('Name')
    plt.tight_layout()
    st.pyplot(fig)