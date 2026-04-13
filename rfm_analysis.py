# Importing Python necessary libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
pio.templates.default = "plotly_white"

data = pd.read_csv("D:/Data Science/Data Science projects/data analysis/RFM Analysis/rfm_data.csv")
pd.set_option('display.max_columns',None)
# Let's have a look at first five rows of the dataset:
print(data.head())

# Check for missing values
print(data.isnull().sum())

# Next, we look at the descriptive statistics of the data:
print(data.describe())



# Convert 'PurchaseDate' to datetime
data['PurchaseDate'] = pd.to_datetime(data['PurchaseDate'], errors='coerce')

# Calculate Recency
current_date = pd.to_datetime(datetime.now())
data['Recency'] = (current_date - data['PurchaseDate']).dt.days

# Calculate Frequency
frequency_data = data.groupby('CustomerID')['OrderID'].count().reset_index()
frequency_data.rename(columns={'OrderID': 'Frequency'}, inplace=True)
data = data.merge(frequency_data, on='CustomerID', how='left')

# Calculate Monetary Value
monetary_data = data.groupby('CustomerID')['TransactionAmount'].sum().reset_index()
monetary_data.rename(columns={'TransactionAmount': 'MonetaryValue'}, inplace=True)
data = data.merge(monetary_data, on='CustomerID', how='left')

print(data.head())

# Define scoring criteria for each RFM value
recency_scores = [5,4,3,2,1] # Higher score for lower recency(more recent)
frequency_scores = [1,2,3,4,5] # Higher score for higher frequency value
monetary_scores = [1,2,3,4,5] # Higher score for higher monetary value

# Calculate RFM Scores
data['RecencyScore'] = pd.cut(data['Recency'], bins=5, labels = recency_scores)
data['FrequencyScore'] = pd.cut(data['Frequency'],bins=5, labels = frequency_scores)
data['MonetaryScore'] = pd.cut(data['MonetaryValue'],bins=5, labels = monetary_scores)

# Convert RFM scores to numeric type
data["RecencyScore"] = data["RecencyScore"].astype(int)
data["FrequencyScore"] = data["FrequencyScore"].astype(int)
data["MonetaryScore"] = data["MonetaryScore"].astype(int)

# RFM Value Segmentation
# Now let’s calculate the final RFM score and the value segment according to the scores:

# Calculate the RFM score by combining the individual scores
data["RFM_Score"] = data["RecencyScore"] + data["FrequencyScore"] + data["MonetaryScore"]

# Create RFM segments based on the RFM score
segment_labels = ['Low-Value', 'Mid-Value', 'High-Value']
data['Value Segment'] = pd.qcut(data['RFM_Score'], q=3, labels = segment_labels)

print(data.head())

# Now Let's have a look at the segment distribution
segment_counts = data['Value Segment'].value_counts().reset_index()
segment_counts.columns = ['Value Segment', 'Count']

pastel_colors = px.colors.qualitative.Pastel

# Create the bar chart
fig_segment_dist = px.bar(segment_counts, x='Value Segment', y='Count', color = 'Value Segment',
                          color_discrete_sequence = pastel_colors,
                          title = 'RFM Value segment Distribution')
# Update the Layout
fig_segment_dist.update_layout(xaxis_title = 'RFM Value Segment',
                               yaxis_title = 'Count',
                               showlegend=False)
# Show the Figure
fig_segment_dist.show()

# RFM Customer Segments
# Create a new column for RFM customer segments
data['RFM Customer Segments'] = ''

# Assign RFM customer segments based on RFM Score
data.loc[data['RFM_Score'] >= 9, 'RFM Customer Segments'] = 'Champions'
data.loc[(data['RFM_Score'] >= 6) & (data['RFM_Score'] < 9),'RFM Customer Segments'] = 'Potential Loyalists'
data.loc[(data['RFM_Score'] >= 5) & (data['RFM_Score'] < 6),'RFM Customer Segments'] = 'At Risk Customers'
data.loc[(data['RFM_Score'] >= 4) & (data['RFM_Score'] < 5),'RFM Customer Segments'] = 'Cant Lose'
data.loc[(data['RFM_Score'] >= 3) & (data['RFM_Score'] < 4),'RFM Customer Segments'] = 'Lost'

# Print the updated data with RFM segments
print(data[['CustomerID', 'RFM Customer Segments']])

# RFM Aanlysis
# Lets analyse the distribution of customers across different RFM customer segments within each value segments:
segment_product_counts = data.groupby(['Value Segment', 'RFM Customer Segments']).size().reset_index(name='Count')
segment_product_counts = segment_product_counts.sort_values('Count', ascending=False)
fig_treemap_segment_product = px.treemap(segment_product_counts,
                                         path=['Value Segment','RFM Customer Segments'],
                                         values = 'Count',
                                         color = 'Value Segment', color_discrete_sequence=px.colors.qualitative.Pastel,
                                         title='RFM Customer Segments by Value')
fig_treemap_segment_product.show()

# Let’s analyze the distribution of RFM values within the Champions segment:

# Filter the data to include only the customers in the Champions segment
champions_segment = data[data['RFM Customer Segments'] == 'Champions']

fig = go.Figure()
fig.add_trace(go.Box(y=champions_segment['RecencyScore'], name='Recency'))
fig.add_trace(go.Box(y=champions_segment['FrequencyScore'], name='Frequency'))
fig.add_trace(go.Box(y=champions_segment['MonetaryScore'], name='Monetary'))

fig.update_layout(title="Distribution of RFM Values within Champions Segments",
                  yaxis_title = 'RFM Value',
                  showlegend= True)
fig.show()

# Let's analyse the correlation of the recency, frequency, and monetary scores within the champions segment:
correlation_matrix = champions_segment[['RecencyScore', 'FrequencyScore', 'MonetaryScore']].corr()

# Visualize the correlation matrix using a heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
                    z=correlation_matrix.values,
                    x=correlation_matrix.columns,
                    y=correlation_matrix.columns,
                    colorscale= 'RdBu',
                    colorbar= dict(title='Correlation')))
fig_heatmap.update_layout(title="Correlation Matrix of RFM Values within Champions Segment")
fig_heatmap.show()


# Now let's have a look at the number of customers in all the segments
import plotly.colors as pc

pastel_colors = pc.qualitative.Pastel

segment_counts = data['RFM Customer Segments'].value_counts()

# Create a bar chart to compare segment counts
fig = go.Figure(data=[go.Bar(x=segment_counts.index,y=segment_counts.values,
                             marker=dict(color=pastel_colors))])

# Update the layout
fig.update_layout(title="Comparison of RFM Segments",
                  xaxis_title = 'RFM Segments',
                  yaxis_title = 'Number of Customers',
                  showlegend=False)
fig.update_traces(marker_line_color='rgb(8, 48, 107)',
                  marker_line_width=1.5)
fig.show()

# Let's have a look at the recency, frequency, and monetary scores of all the segments:
# Calculate the average Recency, Frequency, and Monetary scores for each segment
segment_scores = data.groupby('RFM Customer Segments')[['RecencyScore', 'FrequencyScore', 'MonetaryScore']].mean().reset_index()

# Create a grouped bar chart to compare segment scores
fig = go.Figure()

# Add bars for Recency score
fig.add_trace(go.Bar(
    x = segment_scores['RFM Customer Segments'],
    y = segment_scores['RecencyScore'],
    name = 'Recency Score',
    marker_color = 'rgb(158,202,225)'
))

# Add bars for Frequency Score
fig.add_trace(go.Bar(
    x = segment_scores['RFM Customer Segments'],
    y = segment_scores['FrequencyScore'],
    name = 'Frequency Score',
    marker_color = 'rgb(94,158,217)'
))

# Add bars for Monetary Score
fig.add_trace(go.Bar(
    x = segment_scores['RFM Customer Segments'],
    y = segment_scores['MonetaryScore'],
    name = 'Monetary Score',
    marker_color = 'rgb(32,102,148)'
))

# Update the Layout
fig.update_layout(
    title = 'Comparison of RFM Segments based on Recency, Frequency and Monetary Score',
    xaxis_title = 'RFM Segments',
    yaxis_title = 'Score',
    barmode = 'group',
    showlegend = True
)
fig.show()
