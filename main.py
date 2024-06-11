import pandas as pd
import hashlib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

# Function to convert IP address to a numerical hash
def ip_to_numeric(ip):
    return int(hashlib.md5(ip.encode()).hexdigest(), 16)

# Function to determine subnet based on the host IPv6 address generation pattern
def determine_subnet(ip):
    last_value = int(ip.split('::')[-1].split('/')[0])  # Extract the numerical part after '::'
    if 1 <= last_value <= 100:
        return 'Subnet 1'
    elif 101 <= last_value <= 200:
        return 'Subnet 2'
    elif 201 <= last_value <= 300:
        return 'Subnet 3'
    elif 301 <= last_value <= 400:
        return 'Subnet 4'
    elif 401 <= last_value <= 500:
        return 'Subnet 5'
    else:
        return 'Other'

# Load the datasets
traffic_data = pd.read_csv('data/traffic_captured_summary.csv')
host_status = pd.read_csv('data/host_status.csv')

# Remove /64 suffix from IP addresses in host_status
host_status['IPv6 Address'] = host_status['IPv6 Address'].apply(lambda x: x.split('/')[0])

# Filter traffic data to only include packets where the destination is the server IP
server_ipv6 = '2001:db8::1'
traffic_data = traffic_data[traffic_data['Destination'] == server_ipv6]

# Merge datasets on IP address with inner join to drop unmatched IPs
merged_data = traffic_data.merge(host_status, left_on='Source', right_on='IPv6 Address', how='inner')

# Drop unnecessary columns
merged_data = merged_data.drop(columns=['Destination', 'IPv6 Address', 'Host'])

# Encode the target variable
merged_data['Status'] = merged_data['Status'].map({'benign': 0, 'malicious': 1})

# Drop rows with NaN values in the merged data
merged_data = merged_data.dropna(subset=['Status'])

# Additional feature engineering
merged_data['Packet_Rate'] = merged_data['Packet_Count'] / merged_data['Duration']
merged_data['Total_Packets'] = merged_data['Packet_Count']

# Apply the function to the 'Source' column
merged_data['Source_numeric'] = merged_data['Source'].apply(ip_to_numeric)

# Handle infinite values from division by zero
merged_data.replace([np.inf, -np.inf], 0, inplace=True)
merged_data.fillna(0, inplace=True)

# Prepare features and labels
X = merged_data.drop(columns=['Source', 'Status'])
y = merged_data['Status']

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply SMOTE to balance the dataset
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# Split the resampled data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Train a Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
classification_report_result = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print("Classification Report:")
print(classification_report_result)

# Predict on the entire dataset to identify malicious hosts
y_full_pred = model.predict(X_scaled)
merged_data['Predicted_Status'] = y_full_pred

# Determine subnets based on the last octet of the IP address
merged_data['Subnet'] = merged_data['Source'].apply(determine_subnet)

# Group by subnets and count malicious hosts
subnet_counts = merged_data[merged_data['Predicted_Status'] == 1].groupby('Subnet').size().reset_index(name='Malicious_Hosts')

# Flag subnets with more than 20 malicious hosts as suspicious
subnet_counts['Suspicious'] = subnet_counts['Malicious_Hosts'] > 20

print(subnet_counts)
