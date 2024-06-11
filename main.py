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

# Load the datasets
traffic_data = pd.read_csv('traffic_captured_summary.csv')
host_status = pd.read_csv('host_status.csv')

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

# Apply the function to the 'Source' column
merged_data['Source_numeric'] = merged_data['Source'].apply(ip_to_numeric)

# Additional feature engineering
merged_data['Packet_Rate'] = merged_data['Packet_Count'] / merged_data['Duration']

# Prepare features and labels
X = merged_data.drop(columns=['Source', 'Status'])
y = merged_data['Status']

# Handle infinite values from division by zero
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X.fillna(0, inplace=True)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply SMote to balance the dataset
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
