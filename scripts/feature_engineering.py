
import pandas as pd
import hashlib

# Load the preprocessed data
merged_data = pd.read_csv('data/preprocessed_data.csv')

# Function to convert IP address to a numerical hash
def ip_to_numeric(ip):
    return int(hashlib.md5(ip.encode()).hexdigest(), 16)

# Apply the function to the 'Source' column
merged_data['Source_numeric'] = merged_data['Source'].apply(ip_to_numeric)

# Additional feature engineering
merged_data['Packet_Rate'] = merged_data['Packet_Count'] / merged_data['Duration']

# Handle infinite values from division by zero
merged_data.replace([float('inf'), -float('inf')], 0, inplace=True)
merged_data.fillna(0, inplace=True)

# Save the data with new features
merged_data.to_csv('data/featured_data.csv', index=False)
