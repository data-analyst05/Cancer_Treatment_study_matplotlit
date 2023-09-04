#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# 
# - Add your analysis here.
#  

# In[3]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

# Study data files
mouse_metadata_path = "./data/Mouse_metadata.csv"
study_results_path = "./data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame
merged_data = pd.merge(study_results, mouse_metadata, on="Mouse ID", how="left")

# Display the data table for preview
merged_data


# In[4]:


# Checking the number of mice.
unique_mice_count = len(merged_data["Mouse ID"].unique())
unique_mice_count


# In[5]:


# Our data should be uniquely identified by Mouse ID and Timepoint
# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
duplicate_mouse = merged_data[merged_data.duplicated(subset=["Mouse ID", "Timepoint"])]["Mouse ID"].unique()
duplicate_mouse


# In[6]:


# Optional: Get all the data for the duplicate mouse ID. 
duplicate_mouse_data = merged_data[merged_data["Mouse ID"] =="g989"]
duplicate_mouse_data


# In[7]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
cleaned_data = merged_data[merged_data["Mouse ID"].isin(duplicate_mouse_data) == False]
cleaned_data
# cleaned_data = merged_data.drop_duplicates(subset=["Mouse ID", "Timepoint"])
# cleaned_data


# In[8]:


# Checking the number of mice in the clean DataFrame.
unique_mice_count_cleaned = len(cleaned_data["Mouse ID"].unique())
unique_mice_count_cleaned


# ## Summary Statistics

# In[16]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen

# Use groupby and summary statistical methods to calculate the following properties of each drug regimen: 
# mean, median, variance, standard deviation, and SEM of the tumor volume. 
# Assemble the resulting series into a single summary DataFrame.

# Group the cleaned data by Drug Regimen
grouped_data = cleaned_data.groupby("Drug Regimen")

# Calculate summary statistics for tumor volume
summary_statistics = grouped_data["Tumor Volume (mm3)"].agg(["mean", "median", "var", "std", "sem"])

# Rename columns for clarity
summary_statistics = summary_statistics.rename(columns={
    "mean": "Mean Tumor Volume",
    "median": "Median Tumor Volume",
    "var": "Tumor Volume Variance",
    "std": "Tumor Volume Std.Dev",
    "sem": "Tumor Volume Std.Err."
})

# Display the summary statistics
summary_statistics


# In[20]:


# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# and SEM of the tumor volume for each regimen (only one method is required in the solution)


# Using the aggregation method, produce the same summary statistics in a single line
summary_statistics_sl = cleaned_data.groupby("Drug Regimen").agg({"Tumor Volume (mm3)" : ["mean", "median", "var", "std", "sem"]})
summary_statistics_sl


# ## Bar and Pie Charts

# In[28]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.
# Create a DataFrame to count the number of mice per drug regimen
mice_count_by_regimen = cleaned_data["Drug Regimen"].value_counts()

# Create a bar plot using Pandas
mice_count_by_regimen.plot(kind="bar", title="Number of Mice per Drug Regimen (Pandas)")
plt.xticks(rotation=90)
plt.ylabel("# of Observed Mouse Timepoints")
plt.show()


# In[30]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using pyplot.
plt.bar(mice_count_by_regimen.index, mice_count_by_regimen.values)
plt.title("Number of Mice per Drug Regimen (Matplotlib)")
plt.xlabel("Drug Regimen")
plt.ylabel("# of Observed Mouse Timepoints")
plt.xticks(rotation=45)
plt.show()


# In[32]:


# Generate a pie plot showing the distribution of female versus male mice using Pandas

# Create a DataFrame to count the distribution of female versus male mice
gender_distribution = cleaned_data.Sex.value_counts()

# Create a pie plot using Pandas
gender_distribution.plot(kind="pie", autopct='%1.1f%%', title="Distribution of Female vs. Male Mice (Pandas)")
plt.ylabel("")
plt.show()


# In[34]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot

# Create a pie plot using Matplotlib's pyplot
plt.pie(gender_distribution.values, labels=gender_distribution.index, autopct='%1.1f%%')
plt.title("Distribution of Female vs. Male Mice (Matplotlib)")
plt.show()


# ## Quartiles, Outliers and Boxplots

# In[47]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  

# Capomulin, Ramicane, Infubinol, and Ceftamin



# Start by getting the last (greatest) timepoint for each mouse
final_timepoint_df = cleaned_data.groupby("Mouse ID")["Timepoint"].max().reset_index()
final_timepoint_df

# Merge this group df with the original DataFrame to get the tumor volume at the last timepoint
merge_final_timepoint_df=final_timepoint_df.merge(cleaned_data, on=["Mouse ID", "Timepoint"], how="left")


# In[62]:


# Put treatments into a list for for loop (and later for plot labels)

# List of promising treatment regimens
promising_regimens = ["Capomulin", "Ramicane", "Infubinol", "Ceftamin"]


    
# Create empty list to fill with tumor vol data (for plotting)
tumor_volume_data = []

# Calculate the IQR and quantitatively determine if there are any potential outliers. 
for regimen in promising_regimens:
    
    # Locate the rows which contain mice on each drug and get the tumor volumes
    regimen_data = merge_final_timepoint_df.loc[merge_final_timepoint_df["Drug Regimen"] == regimen, "Tumor Volume (mm3)"]
    
    # add subset 
    tumor_volume_data.append(regimen_data)
    
    # Determine outliers using upper and lower bounds
    quantiles = regimen_data.quantile([0.25,0.5,0.75])
    lowerq = quantiles[0.25]
    upperq = quantiles[0.75]
    iqr = upperq - lowerq
    lower_bound = lowerq - (1.5 * iqr)
    upper_bound = upperq + (1.5 * iqr)

    outliers = regimen_data.loc[(regimen_data < lower_bound) | (regimen_data > upper_bound)]
    print(f"{regimen}'s potential outliers {outliers}")


# In[65]:


# Generate a box plot that shows the distrubution of the tumor volume for each treatment group.
plt.boxplot(tumor_volume_data, labels=promising_regimens, flierprops=dict(marker="o", markersize=8, markerfacecolor="red", markeredgecolor="black"))
plt.title("Tumor Volume Distribution by Treatment Regimen")
plt.ylabel("Final Tumor Volume (mm3)")
plt.show()


# ## Line and Scatter Plots

# In[93]:


# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin
capomulin_mouse = cleaned_data[cleaned_data["Drug Regimen"] == "Capomulin"]
mouse_data=capomulin_mouse[capomulin_mouse["Mouse ID"] == "l509"]

# Generate a line plot of tumor volume vs. time point for the selected mouse
plt.plot(mouse_data["Timepoint"], mouse_data["Tumor Volume (mm3)"], marker='o')
plt.title("Capomulin treatment of mouse l509")
plt.xlabel("Timepoint(days)")
plt.ylabel("Tumor Volume (mm3)")
# plt.grid(True)
plt.show()


# In[96]:


# Generate a scatter plot of mouse weight vs. the average observed tumor volume for the entire Capomulin regimen

# Group the data by Mouse ID and calculate the average observed tumor volume and mouse weight
capomulin_data = cleaned_data[cleaned_data["Drug Regimen"] == "Capomulin"]
avg_tumor_volume_weight = capomulin_data.groupby("Mouse ID")[["Tumor Volume (mm3)", "Weight (g)"]].mean()

# Generate a scatter plot
plt.scatter(avg_tumor_volume_weight["Weight (g)"], avg_tumor_volume_weight["Tumor Volume (mm3)"])
plt.title("Mouse Weight vs. Average Observed Tumor Volume (Capomulin)")
plt.xlabel("Weight (g)")
plt.ylabel("Average Tumor Volume (mm3)")
# plt.grid(True)
plt.show()


# ## Correlation and Regression

# In[119]:


# Calculate the correlation coefficient and a linear regression model 
# for mouse weight and average observed tumor volume for the entire Capomulin regimen

# Calculate the correlation coefficient between mouse weight and average tumor volume
correlation = round(st.pearsonr(avg_tumor_volume_weight["Weight (g)"], avg_tumor_volume_weight["Tumor Volume (mm3)"])[0], 2)

# correlation = st.pearsonr(avg_tumor_volume_weight["Weight (g)"], avg_tumor_volume_weight["Tumor Volume (mm3)"])
print(f"Correlation between Weight and Tumor Volume: {correlation}")

# Calculate the linear regression model
slope, intercept, r_value, p_value, std_err = st.linregress(avg_tumor_volume_weight["Weight (g)"], avg_tumor_volume_weight["Tumor Volume (mm3)"])

# Create a regression line equation
regression_line = "y = " + str(round(slope, 2)) + "x + " + str(round(intercept, 2))

# Generate the scatter plot with the regression line
plt.scatter(avg_tumor_volume_weight["Weight (g)"], avg_tumor_volume_weight["Tumor Volume (mm3)"])
plt.plot(avg_tumor_volume_weight["Weight (g)"], slope * avg_tumor_volume_weight["Weight (g)"] + intercept, color='red')
plt.title("Mouse Weight vs. Average Observed Tumor Volume (Capomulin)")
plt.xlabel("Weight (g)")
plt.ylabel("Average Tumor Volume (mm3)")
plt.annotate(regression_line, (20, 36), fontsize=12, color='red')
# plt.grid(True)
plt.show()


# In[ ]:




