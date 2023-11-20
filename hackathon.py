# -*- coding: utf-8 -*-
"""Hackathon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NrtE-FWaxi6oPpAH0qeIbbB8j4XwCPwZ
"""

#Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Data loading
from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
data_Facebook = pd.read_csv('/content/drive/My Drive/Facebook.csv')
data_Twitter = pd.read_csv('/content/drive/My Drive/Twitter.csv')

data_Facebook.columns

data_Twitter.columns

columns_to_summarize = ['Posts_LikeCount', 'Posts_CommentCount', 'Posts_ShareCount', 'Posts_ViewCount']

# Generating summary
summary = data_Facebook[columns_to_summarize].describe()
summary

# Calculate percentiles for each metric
like_threshold = data_Facebook['Posts_LikeCount'].quantile(0.50)
comment_threshold = data_Facebook['Posts_CommentCount'].quantile(0.50)
share_threshold = data_Facebook['Posts_ShareCount'].quantile(0.50)# Calculate percentiles for each metric

def categorize_post(row):
    likes = row['Posts_LikeCount']
    comments = row['Posts_CommentCount']
    shares = row['Posts_ShareCount']

    if likes >= like_threshold and comments < comment_threshold and shares < share_threshold:
        return 'Interesting'
    elif likes >= like_threshold and comments >= comment_threshold and shares < share_threshold:
        return 'Discussion Worthy'
    elif shares >= share_threshold and comments >= comment_threshold and likes >= like_threshold:
        return 'Viral'
    else:
        return 'No impact'

data_Facebook['Post_Impact'] = data_Facebook.apply(categorize_post, axis=1)

data_Facebook.head()

data_Facebook['Date'] = pd.to_datetime(data_Facebook['Posts_TimeStamp'], unit='s')
data_Facebook.drop('Posts_TimeStamp', axis=1, inplace=True)
data_Facebook.head()

columns_to_summarize_T = ['Posts Favorite Count', 'Posts Reply Count', 'Posts Retweet Count', 'Posts View Count']

# Generating summary
summary = data_Twitter[columns_to_summarize_T].describe()
summary

# Calculate percentiles for each metric for twitter
Favorite_threshold = data_Twitter['Posts Favorite Count'].quantile(0.5)
Reply_threshold = data_Twitter['Posts Reply Count'].quantile(0.5)
Retweet_threshold = data_Twitter['Posts Retweet Count'].quantile(0.5)

def categorize_post(row, favorite_threshold, reply_threshold, retweet_threshold):
    fav_count, reply_count, retweet_count = row['Posts Favorite Count'], row['Posts Reply Count'], row['Posts Retweet Count']

    if fav_count > favorite_threshold and reply_count <= reply_threshold and retweet_count <= retweet_threshold:
        return 'Interesting'
    elif reply_count > reply_threshold and retweet_count <= retweet_threshold:
        return 'Discussion Worthy'
    elif retweet_count > retweet_threshold and fav_count > favorite_threshold and reply_count > reply_threshold:
        return 'Viral'
    else:
        return 'Other'

# Example usage
data_Twitter['Post_Impact'] = data_Twitter.apply(lambda row: categorize_post(row, Favorite_threshold, Reply_threshold, Retweet_threshold), axis=1)

data_Twitter.head()

data_Facebook.columns

# Ensure the date column is in datetime format
data_Facebook_1 = data_Facebook.copy()
data_Facebook_1['Date'] = pd.to_datetime(data_Facebook_1['Date'])

# Set the date column as the index
data_Facebook_1.set_index('Date', inplace=True)

# Group the data by Week and Post Impact, then count the occurrences
grouped_data = data_Facebook_1.resample('M').apply(lambda x: x['Post_Impact'].value_counts()).unstack(fill_value=0)

# Reset the index so that Date becomes a column again, if you need it for plotting
grouped_data.reset_index(inplace=True)

# Plotting
grouped_data.set_index('Date').plot(kind='bar', stacked=True, figsize=(15, 7))

plt.title('Post Impact Over Time - Grouped by Week')
plt.xlabel('Week')
plt.ylabel('Number of Posts')
plt.legend(title='Post Impact')
plt.xticks(rotation=45)  # Rotate the x-axis labels for better readability
plt.tight_layout()  # Adjust the layout
plt.show()

data_Facebook.columns

# Updated list of regions to exclude
exclude_regions = [
    'Anglosphere', 'African Union', 'EU', 'Xinjiang', 'Chongqing', 'Beijing', 'Jilin',
    'Jiangsu','Shanghai','Jiangxi', 'Hainan', 'Sichuan', 'Hong Kong', 'Fujian', 'Guangdong', 'Tibet', 'Shandong'
]

# Filter the DataFrame to exclude these regions
filtered_data = data_Facebook[~data_Facebook['Region'].isin(exclude_regions)]

filtered_data.columns

# Filter for viral posts in data_Facebook
viral_posts = filtered_data[filtered_data['Post_Impact'] == 'Viral']

# Group by Region and Date, then count occurrences
grouped_data = viral_posts.groupby(['Region', viral_posts['Date'].dt.date]).size().reset_index(name='Count')

# Pivot the data for heatmap
pivot_table = grouped_data.pivot("Region", "Date", "Count").fillna(0)

# Create a heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(pivot_table, annot=True, fmt="g", cmap='viridis')

plt.title('Viral Posts by Region and Date')
plt.xlabel('Date')
plt.ylabel('Region')
plt.xticks(rotation=45)
plt.show()

# Assuming 'Region' is the column name for regions in your DataFrame
unique_regions = filtered_data['Region'].unique()

print(unique_regions)

# Filter for viral posts in data_Facebook
viral_posts = filtered_data[filtered_data['Post_Impact'] == 'Viral']

# Identify top 8 countries with most viral posts
top_countries = viral_posts['Region'].value_counts().nlargest(8).index

# Filter to include only top countries
viral_top_countries = viral_posts[viral_posts['Region'].isin(top_countries)]
viral_posts.columns

# Filter for viral posts in data_Facebook
viral_posts = filtered_data[filtered_data['Post_Impact'] == 'Viral']

# Identify top 8 countries with most viral posts
top_countries = viral_posts['Region'].value_counts().nlargest(8).index

# Filter to include only top countries
viral_top_countries = viral_posts[viral_posts['Region'].isin(top_countries)]

# Group by Region and Date, then count occurrences
grouped_data = viral_top_countries.groupby(['Region', viral_top_countries['Date'].dt.date]).size().reset_index(name='Count')

# Pivot the data for heatmap
pivot_table = grouped_data.pivot("Region", "Date", "Count").fillna(0)

# Create a heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(pivot_table, annot=True, fmt="g", cmap='viridis')

plt.title('Viral Posts by Top 8 Regions and Date')
plt.xlabel('Date')
plt.ylabel('Region')
plt.xticks(rotation=45)
plt.show()

#Filter twitter data
exclude_regions = [
    'Anglosphere','African Union', 'Fujian', 'UN', 'EU', 'Xinjiang', 'Chongqing', 'Beijing', 'Jilin',
    'Jiangsu','Shanghai','Jiangxi', 'Hainan', 'Sichuan', 'Guangdong', 'Tibet', 'shaanxi', 'Shandong'
]

# Filter the DataFrame to exclude these regions
filtered_data_T = data_Twitter[~data_Twitter['Region'].isin(exclude_regions)]
filtered_data_T.head()

# Filter twitter data
exclude_regions2 = ['Shaanxi', 'Guangxi', 'Henan']

# Filter the DataFrame to exclude these regions
filtered_data_2 = filtered_data_T[~filtered_data_T['Region'].isin(exclude_regions2)]
filtered_data_2.head()

import pandas as pd

# Assuming your DataFrame is named 'df' and the column name is 'Posts Created At'
filtered_data_2['Posts Created At'] = pd.to_datetime(filtered_data_T['Posts Created At'])

# Assuming 'Region' is the column name for regions in your DataFrame
unique_regions = filtered_data_2['Region'].unique()

print(unique_regions)

import seaborn as sns

# Filter for viral posts in data_Twitter
viral_posts = filtered_data_2[filtered_data_2['Post_Impact'] == 'Viral']

# Identify top 8 countries with most viral posts
top_countries = viral_posts['Region'].value_counts().nlargest(8).index

# Filter to include only top countries
viral_top_countries = viral_posts[viral_posts['Region'].isin(top_countries)]

# Group by Region and Date, then count occurrences
grouped_data = viral_top_countries.groupby(['Region', viral_top_countries['Posts Created At'].dt.date]).size().reset_index(name='Count')

# Pivot the data for heatmap
pivot_table = grouped_data.pivot("Region", "Posts Created At", "Count").fillna(0)

# Create a heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(pivot_table, annot=True, fmt="g", cmap='viridis')

plt.title('Viral Posts by Top 8 Regions and Date, twitter')
plt.xlabel('Posts Created At')
plt.ylabel('Region')
plt.xticks(rotation=45)
plt.show()

import pandas as pd
from IPython.display import display

# Convert the 'Posts Created At' column to datetime
filtered_data_2['Posts Created At'] = pd.to_datetime(filtered_data_2['Posts Created At'])

# Filter the DataFrame to include only rows where 'Impact' is maximum within each region
most_viral_posts = filtered_data_2[filtered_data_2.groupby('Region')['Posts Retweet Count'].transform(max) == filtered_data_2['Posts Retweet Count']]

# Extract the timestamp of the most viral post per region
most_viral_times = most_viral_posts[['Region', 'Posts Created At']]

# Display the times of the most viral posts per region in a table format
print("Time of the most viral posts per region:")
display(most_viral_times)

import pandas as pd
from IPython.display import display

# Convert the 'Posts Created At' column to datetime
filtered_data_2['Posts Created At'] = pd.to_datetime(filtered_data_2['Posts Created At'])

# Filter the DataFrame to include only rows where 'Impact' is maximum within each region
most_viral_posts = filtered_data_2[filtered_data_2.groupby('Region')['Posts Retweet Count'].transform(max) == filtered_data_2['Posts Retweet Count']]

# Extract the timestamp of the most viral post per region
most_viral_times = most_viral_posts[['Region', 'Posts Created At','Posts']]

# Display the times of the most viral posts per region in a table format
print("Time of the most viral posts per region:")
display(most_viral_times)

#### Time of most retweeted posts

# Convert the 'Posts Created At' column to datetime
filtered_data_2['Posts Created At'] = pd.to_datetime(filtered_data_2['Posts Created At'])

# Filter the DataFrame to include only rows where 'Impact' is maximum within each region
most_viral_posts = filtered_data_2[filtered_data_2.groupby('Region')['Posts Retweet Count'].transform(max) == filtered_data_2['Posts Retweet Count']]

# Extract and print the timestamp of the most viral post per region
most_viral_times = most_viral_posts[['Region', 'Posts Created At']]
print("Time of the most viral posts per region:")
print(most_viral_times)

# Assuming 'Region' and 'Post_Impact' are columns in your DataFrame
# Replace 'filtered_data' with the name of your DataFrame
data = filtered_data[['Region', 'Post_Impact']]

# Count viral posts by country
viral_counts = data[data['Post_Impact'] == 'Viral']['Region'].value_counts().reset_index()
viral_counts.columns = ['Country', 'Number of Viral Posts']

# Print the viral post counts by country
print(viral_counts)

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Corrected data with updated country name
data = pd.DataFrame({
    'Country': [
        'United States of America', 'Egypt', 'Singapore', 'Australia', 'Hong Kong',
        'Pakistan', 'Sierra Leone', 'Trinidad and Tobago', 'Nepal', 'Somalia',
        'Iceland', 'Kenya', 'South Africa', 'Botswana', 'Guyana', 'North Macedonia',
        'Papua New Guinea', 'Uganda', 'Lebanon', 'Norway', 'Greece'
    ],
    'Viral Posts': [
        23, 20, 19, 8, 8, 8, 7, 7, 4, 4, 4, 4, 4, 3, 2, 2, 2, 1, 1, 1, 1
    ]
})

# Load a world map GeoDataFrame
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the world map with your data
merged = world.set_index('name').join(data.set_index('Country'), how='left')

# Fill NaN values with 0
merged['Viral Posts'].fillna(0, inplace=True)

# Define a function to assign colors
def assign_color(viral_posts):
    if viral_posts > 15:
        return 'red'
    elif 8 < viral_posts <= 15:
        return 'orange'
    elif 5 < viral_posts <= 8:
        return 'pink'
    elif 1 < viral_posts <= 5:
        return 'yellow'
    else:
        return 'lightgrey'

# Apply the function to create a color column
merged['Color'] = merged['Viral Posts'].apply(assign_color)

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
merged.plot(ax=ax, color=merged['Color'], legend=True, edgecolor='black')

# Add text for viral post counts
for idx, row in merged.iterrows():
    if row['Viral Posts'] > 0:
        ax.text(row['geometry'].centroid.x, row['geometry'].centroid.y,
                str(int(row['Viral Posts'])), fontsize=10, ha='center', va='center',
                fontweight='bold', color='black')

plt.show()

import pandas as pd

# Merge the dataframes
# Assuming 'entity name' is the common column and should not be duplicated
merged_data = pd.merge(data_Facebook, data_Twitter, on='Entity Name', how='outer')

# Display the first few rows of the merged dataframe
merged_data.columns

import pandas as pd

# Assuming you have already loaded and merged your data into 'merged_data'
# Replace 'merged_data' with the name of your merged dataframe variable

# Get unique values in the 'Region_FB' column
unique_regions = merged_data['Region_x'].unique()

# Print the unique region values
print(unique_regions)

# List of Chinese cities/regions to be excluded
chinese_cities = ['Shanghai', 'Anglosphere','Jiangxi', 'African Union', 'Beijing', 'Hong Kong', 'Fujian',
                  'Xinjiang', 'Chongqing', 'EU', 'Jilin', 'Jiangsu', 'Hainan',
                  'Sichuan', 'Guangdong', 'Tibet', 'Shandong']

# Exclude rows where 'Region_FB' is one of the Chinese cities
filtered_data = merged_data[~merged_data['Region_x'].isin(chinese_cities)]

# Display the first few rows of the filtered dataframe
filtered_data.head()

# Let's first ensure that 'Facebook Followers Count' and 'X (Twitter) Followers Count' are numeric
filtered_data['Facebook Followers Count'] = pd.to_numeric(filtered_data['Facebook Followers Count'], errors='coerce')
filtered_data['X (Twitter) Followers Count'] = pd.to_numeric(filtered_data['X (Twitter) Followers Count'], errors='coerce')

# Fill NaN values with 0 for calculation
filtered_data['Facebook Followers Count'].fillna(0, inplace=True)
filtered_data['X (Twitter) Followers Count'].fillna(0, inplace=True)

# Calculate total followers again after ensuring the columns are numeric
filtered_data['Total Followers'] = filtered_data['Facebook Followers Count'] + filtered_data['X (Twitter) Followers Count']

# Aggregate data by country for the filtered data
followers_per_country_filtered = filtered_data.groupby('Region_x')['Total Followers'].sum().nlargest(5)

# Plotting the bar graph for the filtered data
followers_per_country_filtered.plot(kind='bar', figsize=(10, 6), color='skyblue', title='Top 5 Countries by Total Followers (Excluding Certain Regions)')
plt.xlabel('Country')
plt.ylabel('Total Followers')
plt.show()

# Correcting the issue by ensuring all follower counts are integers and then plotting the bar chart
# These counts are based on the user's earlier provided information
follower_counts = {
   "USA": 133000000,         # Elon Musk
   "Egypt": 12200000,        # MBC مصر
   "South Africa": 4000000,  # eNCA
   "Pakistan": 19100000,     # Imran Khan
   "Singapore": 2100000      # Aaron Aziz (as of 2017)
}


# Converting follower counts in the dataset to integers
# It appears the follower counts are stored as strings with commas, so we'll remove commas and convert to integers
data_Twitter['X (Twitter) Followers Count'] = data_Twitter['X (Twitter) Followers Count'].str.replace(',', '').astype(int)

# Re-aggregating the total followers count for each country
country_followers = data_Twitter.groupby('Region')['X (Twitter) Followers Count'].sum().to_dict()

# Preparing the data for the bar chart again
# Creating lists for plotting
countries = list(follower_counts.keys())
most_followed_counts = [follower_counts[country] for country in countries]
total_country_followers = [country_followers.get(country, 0) for country in countries]

# Plotting the bar chart
plt.figure(figsize=(12, 6))
bar_width = 0.35
index = range(len(countries))

bar1 = plt.bar(index, most_followed_counts, bar_width, label='Most Followed Person')
bar2 = plt.bar([i + bar_width for i in index], total_country_followers, bar_width, label='Total Followers in Country')

plt.xlabel('Country')
plt.ylabel('Followers Count')
plt.title('Comparison of Most Followed Person vs Total Followers in Country on Twitter (2023)')
plt.xticks([i + bar_width / 2 for i in index], countries)
plt.legend()

plt.tight_layout()
plt.show()

filtered_data.columns

filtered_data.head()

# Get unique values in the 'Region_FB' column
unique_regions = filtered_data['Region'].unique()

# Print the unique region values
print(unique_regions)

# Ensure 'Posts_ShareCount' is numeric
filtered_data['Posts_ShareCount'] = pd.to_numeric(filtered_data['Posts_ShareCount'], errors='coerce')

# Fill NaN values in 'Posts_ShareCount' with 0
filtered_data['Posts_ShareCount'].fillna(0, inplace=True)

# Group by 'Region' and get the index of the row with the max 'Posts_ShareCount' in each group
idx = filtered_data.groupby('Region')['Posts_ShareCount'].idxmax()

# Use the index to get the most viral post per region
most_viral_posts = filtered_data.loc[idx]

# Extract and print the timestamp of the most viral post per region
most_viral_times = most_viral_posts[['Region', 'Date', 'Posts']]
print("Time of the most viral posts per region:")
print(most_viral_times)

keywords = ['Gaza', 'Hamas', 'Israel', 'Palestine']
filtered_rows = filtered_data[filtered_data['Posts'].str.contains('|'.join(keywords), case=False, na=False)]

# Display the filtered DataFrame
print(filtered_rows)

# Assuming most_viral_posts is your DataFrame containing the most viral posts per region
# Count the number of viral posts in each region
region_counts = filtered_rows['Region'].value_counts()

# Plotting
plt.figure(figsize=(10, 6))
region_counts.plot(kind='bar')
plt.title('Distribution of Viral Posts in Each Region')
plt.xlabel('Region')
plt.ylabel('Count of Viral Posts')
plt.xticks(rotation=80)
plt.show()

exclude_regions = [
    'Anglosphere', 'Xinjiang', 'Chongqing', 'Beijing', 'Jilin',
    'Jiangsu', 'Shanghai', 'Jiangxi', 'Hainan', 'Sichuan', 'Hong Kong', 'Fujian', 'Guangdong', 'Tibet', 'Shandong'
]

filtered_data_R = data_Facebook[~data_Facebook['Region'].isin(exclude_regions)]

keywords = ['Gaza', 'Hamas', 'Israel', 'Palestine']
filtered_rows_P = filtered_data_R[filtered_data_R['Posts'].str.contains('|'.join(keywords), case=False, na=False)]

# Display the filtered DataFrame
print(filtered_rows_P)

# Assuming most_viral_posts is your DataFrame containing the most viral posts per region
# Count the number of viral posts in each region
region_counts = filtered_rows_P['Region'].value_counts()

# Plotting
plt.figure(figsize=(10, 6))
region_counts.plot(kind='bar')
plt.title('Distribution of Posts in Each Region')
plt.xlabel('Region')
plt.ylabel('Count of Viral Posts')
plt.xticks(rotation=80)
plt.show()

filtered_rows_P.head()

# Filter for only 'viral' Post_Impact
viral_posts = filtered_rows_P[filtered_rows_P['Post_Impact'] == 'viral']

# Count the number of viral posts in each region
region_counts = viral_posts['Region'].value_counts()
print(region_counts)

import pandas as pd
import matplotlib.pyplot as plt

# Assuming filtered_rows_P is a DataFrame you have defined earlier

# Filter for only 'viral' Post_Impact
viral_posts = filtered_rows_P[filtered_rows_P['Post_Impact'] == 'viral']

# Count the number of viral posts in each region
region_counts = viral_posts['Region'].value_counts()

# Plotting
plt.figure(figsize=(10, 6))
region_counts.plot(kind='bar')  # Use region_counts here
plt.title('Distribution of Viral Posts in Each Region')
plt.xlabel('Region')
plt.ylabel('Count of Viral Posts')
plt.xticks(rotation=80)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming filtered_rows_P is a DataFrame you have defined earlier

# Check if there are 'viral' values in 'Post_Impact'
if 'Viral' in filtered_rows_P['Post_Impact'].unique():
    # Filter for only 'viral' Post_Impact
    viral_posts = filtered_rows_P[filtered_rows_P['Post_Impact'] == 'Viral']

    # Check if there are any rows in viral_posts
    if not viral_posts.empty:
        # Count the number of viral posts in each region
        region_counts = viral_posts['Region'].value_counts()

        # Check if region_counts is not empty
        if not region_counts.empty:
            # Plotting
            plt.figure(figsize=(10, 6))
            region_counts.plot(kind='bar')
            plt.title('Distribution of Viral Posts in Each Region')
            plt.xlabel('Region')
            plt.ylabel('Count of Viral Posts')
            plt.xticks(rotation=80)
            plt.show()
        else:
            print("No viral posts found in any region.")
    else:
        print("There are no viral posts.")
else:
    print("'viral' value not found in 'Post_Impact' column.")

!pip install wordcloud

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Assuming df is your DataFrame and 'posts' is the column name
# Concatenate all posts into a single string
text = " ".join(post for post in filtered_rows_P['Posts'])

# Create and generate a word cloud image
wordcloud = WordCloud(background_color="white").generate(text)

# Display the generated wordcloud image
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Assuming df is your DataFrame and 'Posts' is the column name
# Concatenate all posts into a single string
text = " ".join(post for post in filtered_rows_P['Posts'])

# Create and generate a word cloud image with higher resolution
wordcloud = WordCloud(background_color="white", width=800, height=400).generate(text)

# Display the generated wordcloud image
plt.figure(figsize=(20, 10), dpi=300)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# Save the image in high resolution
plt.savefig('wordcloud_high_res.png', dpi=300)

plt.show()