# Cancer Treatment Study with Pandas (matplotlib scipy)

## Overview

Welcome to the Pymaceuticals, Inc. Cancer Treatment Study project! In this project, we analyze data from an animal study conducted by Pymaceuticals, Inc. The study aims to evaluate the performance of a drug regimen called Capomulin in treating squamous cell carcinoma (SCC), a form of skin cancer, compared to other treatment regimens.

As a senior data analyst at Pymaceuticals, Inc., you will find a detailed analysis of the study results in this repository, including data preparation, summary statistics, data visualization, and statistical analysis. The project is organized into different tasks, each contributing to a comprehensive report on the study's findings.

## Project Structure

The project is organized into several tasks, as follows:

1. **Data Preparation**: In this section, we prepare the data by merging the mouse metadata and study results into a single DataFrame, identifying duplicate mouse IDs, and creating a cleaned DataFrame for analysis.

2. **Summary Statistics**: Here, we calculate summary statistics, including the mean, median, variance, standard deviation, and SEM of the tumor volume for each drug regimen.

3. **Bar and Pie Charts**: We generate bar charts to show the total number of mice for each drug regimen and pie charts to visualize the distribution of female versus male mice in the study.

4. **Quartiles, Outliers, and Boxplots**: In this section, we calculate the final tumor volume for selected treatment regimens, determine potential outliers, and create box plots to visualize the distribution of tumor volumes.

5. **Line and Scatter Plots**: We create line plots to display tumor volume over time for a single mouse treated with Capomulin and scatter plots to show the relationship between mouse weight and average tumor volume.

6. **Correlation and Regression**: Finally, we calculate the correlation coefficient and perform linear regression analysis to examine the relationship between mouse weight and tumor volume for the Capomulin regimen.

## Usage

To run the analysis and reproduce the results, follow these steps:

1. Clone this repository to your local machine.

2. Ensure you have the required dependencies installed, such as pandas, matplotlib, and scipy. You can install them using pip:

   ```bash
   pip install pandas matplotlib scipy
