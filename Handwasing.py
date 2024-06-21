# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# # Load the datasets
# monthly_deaths = pd.read_csv('monthly_deaths.csv')
# yearly_deaths_by_clinic = pd.read_csv('yearly_deaths_by_clinic.csv')
#
# # Calculate monthly mortality rates
# monthly_deaths['mortality_rate'] = monthly_deaths['deaths'] / monthly_deaths['births']
#
# # Calculate yearly mortality rates for each clinic
# yearly_deaths_by_clinic['mortality_rate'] = yearly_deaths_by_clinic['deaths'] / yearly_deaths_by_clinic['births']
#
# # Define the implementation year of handwashing
# handwashing_start_year = 1847
#
# # Split the data into before and after handwashing periods
# before_handwashing = yearly_deaths_by_clinic[yearly_deaths_by_clinic['year'] < handwashing_start_year]
# after_handwashing = yearly_deaths_by_clinic[yearly_deaths_by_clinic['year'] >= handwashing_start_year]
#
# # Calculate the average mortality rates before and after handwashing
# average_mortality_before = before_handwashing['mortality_rate'].mean()
# average_mortality_after = after_handwashing['mortality_rate'].mean()
#
# print(f"Average mortality rate before handwashing: {average_mortality_before:.4f}")
# print(f"Average mortality rate after handwashing: {average_mortality_after:.4f}")
#
# # Set Seaborn style and context for aesthetics
# sns.set(style='whitegrid', context='talk')
#
# # Plot the yearly mortality rates for each clinic
# plt.figure(figsize=(14, 7))
# sns.lineplot(data=yearly_deaths_by_clinic, x='year', y='mortality_rate', hue='clinic', marker='o')
# plt.axvline(x=handwashing_start_year, color='red', linestyle='--', label='Handwashing Introduction (1847)')
# plt.title('Yearly Mortality Rates by Clinic')
# plt.xlabel('Year')
# plt.ylabel('Mortality Rate')
# plt.legend(title='Clinic')
# plt.tight_layout()
# plt.show()
#
# # Plot the monthly mortality rates
# monthly_deaths['date'] = pd.to_datetime(monthly_deaths['date'])
# plt.figure(figsize=(14, 7))
# sns.lineplot(data=monthly_deaths, x='date', y='mortality_rate', marker='o', color='blue')
# plt.axvline(x=pd.to_datetime('1847-06-01'), color='red', linestyle='--', label='Handwashing Introduction (1847)')
# plt.title('Monthly Mortality Rates')
# plt.xlabel('Date')
# plt.ylabel('Mortality Rate')
# plt.legend()
# plt.tight_layout()
# plt.show()
#
# # Compare the average mortality rates before and after handwashing
# plt.figure(figsize=(10, 7))
# sns.barplot(x=['Before Handwashing', 'After Handwashing'], y=[average_mortality_before, average_mortality_after], palette='viridis')
# plt.title('Average Mortality Rates Before and After Handwashing')
# plt.ylabel('Average Mortality Rate')
# plt.xlabel('')
# plt.tight_layout()
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Label, LabelSet
from bokeh.transform import factor_cmap
from bokeh.palettes import Viridis256


# Load the datasets
monthly_deaths = pd.read_csv('monthly_deaths.csv')
yearly_deaths_by_clinic = pd.read_csv('yearly_deaths_by_clinic.csv')

# Calculate monthly mortality rates
monthly_deaths['mortality_rate'] = monthly_deaths['deaths'] / monthly_deaths['births']

# Calculate yearly mortality rates for each clinic
yearly_deaths_by_clinic['mortality_rate'] = yearly_deaths_by_clinic['deaths'] / yearly_deaths_by_clinic['births']

# Define the implementation year of handwashing
handwashing_start_year = 1847

# Split the data into before and after handwashing periods
before_handwashing = yearly_deaths_by_clinic[yearly_deaths_by_clinic['year'] < handwashing_start_year]
after_handwashing = yearly_deaths_by_clinic[yearly_deaths_by_clinic['year'] >= handwashing_start_year]

# Calculate the average mortality rates before and after handwashing
average_mortality_before = before_handwashing['mortality_rate'].mean()
average_mortality_after = after_handwashing['mortality_rate'].mean()

print(f"Average mortality rate before handwashing: {average_mortality_before:.4f}")
print(f"Average mortality rate after handwashing: {average_mortality_after:.4f}")

# Convert the 'date' column to datetime
monthly_deaths['date'] = pd.to_datetime(monthly_deaths['date'])
monthly_deaths['year'] = monthly_deaths['date'].dt.year

# Set Seaborn style and context for aesthetics
sns.set(style='whitegrid', context='talk')

# Plot the yearly mortality rates for each clinic using scatterplot with lines
plt.figure(figsize=(14, 7))
clinics = yearly_deaths_by_clinic['clinic'].unique()
for clinic in clinics:
    subset = yearly_deaths_by_clinic[yearly_deaths_by_clinic['clinic'] == clinic]
    sns.scatterplot(data=subset, x='year', y='mortality_rate', label=clinic)
    plt.plot(subset['year'], subset['mortality_rate'], linestyle='-', marker='o')

plt.axvline(x=handwashing_start_year, color='red', linestyle='--', label='Handwashing Introduction (1847)')
plt.title('Yearly Mortality Rates by Clinic')
plt.xlabel('Year')
plt.ylabel('Mortality Rate')
plt.legend(title='Clinic')
plt.tight_layout()
plt.show()

# Plot the monthly mortality rates using scatterplot with lines
plt.figure(figsize=(14, 7))
sns.scatterplot(data=monthly_deaths, x='date', y='mortality_rate', color='blue')
plt.plot(monthly_deaths['date'], monthly_deaths['mortality_rate'], linestyle='-', marker='o', color='blue')

plt.axvline(x=pd.to_datetime('1847-06-01'), color='red', linestyle='--', label='Handwashing Introduction (1847)')
plt.title('Monthly Mortality Rates')
plt.xlabel('Date')
plt.ylabel('Mortality Rate')
plt.legend()
plt.tight_layout()
plt.show()


# Bubble plot for monthly mortality rates over years
plt.figure(figsize=(14, 10))
bubble_plot = sns.scatterplot(
    data=monthly_deaths,
    x='year',
    y='mortality_rate',
    size='births',
    hue='year',
    sizes=(20, 200),
    alpha=0.6,
    palette='viridis',
    legend=None
)

# Add a vertical line to mark the introduction of handwashing
plt.axvline(x=handwashing_start_year, color='red', linestyle='--', label='Handwashing Introduction (1847)')
plt.title('Bubble Plot of Monthly Mortality Rates by Year')
plt.xlabel('Year')
plt.ylabel('Mortality Rate')
plt.legend()
plt.tight_layout()
plt.show()

#Bokeh plotting for mortality rate before and after handwashing was introduced
output_file('mortality_rates.html')
p = figure(y_range=['Before Handwashing', 'After Handwashing'], height=400, width=600,
           title='Average Mortality Rates Before and After Handwashing',
           x_axis_label='Average Mortality Rate', y_axis_label='Period')
periods = ['Before Handwashing', 'After Handwashing']
average_mortality = [average_mortality_before, average_mortality_after]
source = ColumnDataSource(data=dict(periods=periods, average_mortality=average_mortality))
p.rect(x=0, y='periods', width='average_mortality', height=0.5, source=source,
       fill_color=factor_cmap('periods', palette=Viridis256, factors=periods), line_color=None)
labels = LabelSet(x='average_mortality', y='periods', text='average_mortality', level='glyph',
                  x_offset=5, y_offset=-8, source=source)
p.add_layout(labels)
p.hover.tooltips = [("Period", "@periods"), ("Average Mortality Rate", "@average_mortality{0.0000}")]
show(p)