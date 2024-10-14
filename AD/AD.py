import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'AD/merged_output.xlsx'
df_merged = pd.read_excel(file_path)

cleaned_df = df_merged.dropna(subset=['Phases','Sponsor','Start Date','affiliation', 'pi'])
# Convert the 'Start Date' column to datetime format
cleaned_df['Start Date'] = pd.to_datetime(cleaned_df['Start Date'], errors='coerce')
cleaned_df['Start Year'] = cleaned_df['Start Date'].dt.year
# Convert the 'Primary Completion Date' column to datetime format
cleaned_df['Primary Completion Date'] = pd.to_datetime(cleaned_df['Start Date'], errors='coerce')
cleaned_df['Completion Year'] = cleaned_df['Primary Completion Date'].dt.year

# Phase 2-4 industry sponsered study completed in 2024 to 2027
df_selected = cleaned_df[(cleaned_df['Funder Type'].str.upper() == 'INDUSTRY') &
                        (cleaned_df['Phases'].isin(['PHASE2', 'PHASE3','PHASE4']))&
                        (cleaned_df['Study Status']!= 'WITHDRAWN')
                        ]

df_selectedC = df_selected.dropna(axis=1, how='all')

# Page config
st.set_page_config(
    page_title="AD clinical Trial Dashboard",
    page_icon= ":bar_chart",
    layout="wide",
)
# Title of the dashboard
st.title("Alzheimer's Diasease Clinical Trial Dashboard")

# Plot : Trial by year started and status in 2004 to 2024
# Filter the dat for study start in 2004 to 2024
df_start = cleaned_df[(cleaned_df['Start Year'] >=2004) & (cleaned_df['Start Year'] <= 2024)]
grouped_start = df_start.groupby(['Start Year', 'Study Status']).size().reset_index(name='Count')
st.subheader('Registered Clinical Trials by Year Started and Study Status')
fig0, ax0 = plt.subplots(figsize=(10,6))
sns.barplot(x='Start Year', y="Count", hue= 'Study Status', 
            data=grouped_start, palette="Set2", ax=ax0)
ax0.set_xlabel('Year Started')
ax0.set_ylabel('Number of Trials')
ax0.set_title('Registered Trials by Year Started and Study Status')
ax0.set_xticklabels(ax0.get_xticklabels(), rotation=45)
ax0.legend(title='Study Status')

# Display the plot in Streamlit
st.pyplot(fig0)

# Filter the data for studies complete in 2023-2034
trials_2023_2034 = df_selectedC[(df_selectedC['Completion Date'] >= '2023-01-01') & (df_selectedC['Completion Date'] <= '2034-12-31')]
# Count the number of trials in 2023-2034
num_trials_2023_2034 = trials_2023_2034.shape[0]
# Streamlit section to show the number of trials from 2023-2034
st.subheader("Number of Trials complete in 2023-2034")
st.metric(label="Trials complete (2023-2030)", value=num_trials_2023_2034)

# Plot 1: Pie Chart for Phases will complete in 2023-2034
st.subheader("Phases Distribution of Trials complete in 2023-2034")
phase_counts = trials_2023_2034['Phases'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(phase_counts, labels=phase_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)


# Plot 2: Bar Chart for Sponsor vs. Phases (complete in 2023-2034)
st.subheader("Sponsor vs. Phases of Trials Complete in 2023-2034")
sponsor_phase_counts = trials_2023_2034.groupby(['Sponsor', 'Phases']).size().reset_index(name='Counts')
fig2 = px.bar(sponsor_phase_counts, x='Sponsor', y='Counts', color='Phases', barmode='group',
              title="Number of Studies per Sponsor by Phases")
st.plotly_chart(fig2)

# Plot3: Bar Chart for Conditions 
st.subheader("Trials by Condition (complete in 2023-2034)")
condition_counts = trials_2023_2034.groupby('Conditions').size().reset_index(name='Counts')
fig3 = px.bar(condition_counts, x='Conditions', y='Counts',
              title="Number of Studies per Condition")
st.plotly_chart(fig3)

# New Plot 4: Number of Studies Expected to Complete Between 2023 and 2034
st.subheader("Number of Studies Expected to Complete Between 2023 and 2034")

# Group by year and sponsor
date_grouped_df = trials_2023_2034.groupby(['Completion Year', 'Sponsor']).size().reset_index(name='Count')

# Create a bar chart using Plotly
fig4 = px.bar(date_grouped_df, x='Completion Year', y='Count', color='Sponsor', barmode='group',
              title="Studies Expected to Complete Between 2023 and 2034 by Sponsor")

st.plotly_chart(fig4)

# Footer
st.write("### Data Source: https://clinicaltrials.gov")