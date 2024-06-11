
import pandas as pd
import hashlib

# Load the datasets
traffic_data = pd.read_csv('data/traffic_captured_summary.csv')
host_status = pd.read_csv('data/host_status.csv')

# Clean IP addresses in the host_status data to match the format in traffic_data
host_status['IPv6 Address'] = host_status['IPv6 Address'].apply(lambda x: x.split('/')[0])

# Merge datasets on IP address
merged_data = traffic_data.merge(host_status, left_on='Source', right_on='IPv6 Address', how='left')

# Drop unnecessary columns
merged_data = merged_data.drop(columns=['Destination', 'IPv6 Address', 'Host'])

# Encode the target variable
merged_data['Status'] = merged_data['Status'].map({'benign': 0, 'malicious': 1})

# Drop rows with NaN values in the merged data
merged_data = merged_data.dropna(subset=['Status'])

# Save the preprocessed data
merged_data.to_csv('data/preprocessed_data.csv', index=False)
