# 1. data_preprocessing.py
Purpose: This script loads the raw datasets, cleans and merges them, and encodes the target variable.

## Steps:

  1. Load the datasets: Reads the raw data files traffic_captured_summary.csv and host_status.csv.
  2. Clean IP addresses: Adjusts the format of the IP addresses in the host_status dataset to match those in the traffic_data.
  3. Merge datasets: Merges the traffic data with the host status data based on the IP addresses.
  4. Drop unnecessary columns: Removes columns that are not needed for analysis.
  5. Encode target variable: Converts the Status column into numerical values (0 for benign, 1 for malicious).
  6. Handle missing values: Drops rows with missing values in the Status column.
  7. Save preprocessed data: Outputs the cleaned and merged data to preprocessed_data.csv.

# 2. feature_engineering.py
Purpose: This script generates additional features from the preprocessed data.

## Steps:

  1. Load preprocessed data: Reads the preprocessed_data.csv file.
  2. Convert IP addresses: Transforms IP addresses into numerical hashes.
  3. Feature engineering: Creates new features, such as the packet rate (Packet_Count divided by Duration).
  4. Handle infinite values and NaNs: Replaces infinite values resulting from division by zero and fills NaNs with zeros.
  5. Save data with new features: Outputs the data with new features to featured_data.csv.


# 3. model_training.py
Purpose: This script trains a machine learning model using the engineered features and evaluates its performance.

## Steps:

  1. Load data with features: Reads the featured_data.csv file.
  2. Prepare features and labels: Separates the features (X) and target variable (y).
  3. Scale features: Standardizes the feature values.
  4. Balance dataset: Applies SMOTE to address class imbalance by generating synthetic samples for the minority class.
  5. Split data: Divides the data into training and testing sets.
  6. Train model: Uses a Random Forest classifier to train on the training set.
  7. Predict and evaluate: Makes predictions on the test set and evaluates the model's performance using accuracy and a classification report.

# 4. main.py
Purpose: This script combines all the steps from data preprocessing to model training and evaluation into a single script.

## Steps:

  1. Load and preprocess data: Combines steps from data_preprocessing.py.
  2. Feature engineering: Combines steps from feature_engineering.py.
  3. Prepare features and labels: Separates features and target variable.
  4. Scale features: Standardizes the feature values.
  5. Balance dataset: Applies SMOTE to address class imbalance.
  6. Split data: Divides the data into training and testing sets.
  7. Train model: Uses a Random Forest classifier for training.
  8. Predict and evaluate: Makes predictions on the test set and evaluates the model.


These scripts will help you systematically preprocess your data, engineer useful features, train a machine learning model, and evaluate its performance.
