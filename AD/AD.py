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

# Page config
st.set_page_config(
    page_title="AD clinical Trial Dashboard",
    page_icon= ":bar_chart",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Title of the dashboard
st.title("Alzheimer's Diasease Clinical Trial Dashboard")
st.markdown('## Insight into Industry-Sponsored Alzheimers Disease Trials')

# Sidebar for filtering
st.sidebar.title("Filters")
st.sidebar.markdown("Use the filters below to refine the data displayed in the dashboard.")

# =Slidebar for filtering Start Year
st.sidebar.title("Filter by Year Range")
year_range = st.slider(
    "Select Year Range",
    min_value= int(cleaned_df['Start Year'].min()),
    max_value= int(cleaned_df['Start Year'].max()),
    value=(2010, 2030)
)
# Filter the for study start year
df_start = cleaned_df[(cleaned_df['Start Year'] >= year_range[0]) & (cleaned_df['Start Year'] <= year_range[1])]
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


# Streamlit slider for selecting the year range
st.subheader("Select Year Range for Completed Trials")
start_year, end_year = st.slider(
    "Select the range of years", 
    min_value=2010, max_value=2030, 
    value=(2010, 2030)  
)

# Filter the data based on the selected year range
df_complete = cleaned_df[(cleaned_df['Completion Year'] >= start_year) & 
                            (cleaned_df['Completion Year'] <= end_year)]

# Count the number of trials in the Selected Year Range
num_trials_complete = df_complete.shape[0]
# Streamlit section to show the number of trials in the Selected Year Range
st.subheader("Number of Trials complete in the Selected Year Range")
st.metric(label="Trials complete (Selected Year Range)", value=num_trials_complete)


# Plot 1: Pie Chart for Phases will complete in the Selected Year Range
st.subheader("Phases Distribution of Trials complete in the Selected Year Range")
phase_counts = df_complete['Phases'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(phase_counts, labels=phase_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)


# Plot 2: Bar Chart for Sponsor vs. Phases (complete in the Selected Year Range)
st.subheader("Sponsor vs. Phases of Trials Complete in the Selected Year Range")
sponsor_phase_counts = df_complete.groupby(['Sponsor', 'Phases']).size().reset_index(name='Counts')
fig2 = px.bar(sponsor_phase_counts, x='Sponsor', y='Counts', color='Phases', barmode='group',
            title="Number of Studies per Sponsor by Phases")
st.plotly_chart(fig2)

# Plot3: Bar Chart for Conditions 
st.subheader("Trials by Condition (complete in the Selected Year Range)")
condition_counts = df_complete.groupby('Conditions').size().reset_index(name='Counts')
fig3 = px.bar(condition_counts, x='Conditions', y='Counts',
            title="Number of Studies per Condition")
st.plotly_chart(fig3)


# New Plot 4: Number of Studies Expected to Complete in the Selected Year Range
st.subheader("Number of Studies Expected to Complete in the Selected Year Range")

# Group by year and sponsor
date_grouped_df = df_complete.groupby(['Completion Year', 'Sponsor']).size().reset_index(name='Count')

# Create a bar chart using Plotly
fig4 = px.bar(date_grouped_df, 
              x='Completion Year', 
              y='Count', 
              color='Sponsor', 
              barmode='group',
              title="Studies Expected to Complete in the Selected Year Range by Sponsor"
              )
fig4.update_layout(
    width=800,  # Set width as needed
    height=500,  # Set height as needed
    margin=dict(l=40, r=40, t=40, b=40),
     legend=dict(
        title='',
        font=dict(
            size=5  # Change this value to make the legend smaller or larger
        ),
        bgcolor='rgba(255, 255, 255, 0.5)'  # Optional: make the background semi-transparent
    )
)
st.plotly_chart(fig4)

# Footer
st.write("### Data Source: https://clinicaltrials.gov")