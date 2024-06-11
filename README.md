
# IPv6_Traffic

This repository contains the code and datasets for a project where a virtual IPv6 network was simulated to capture and create a dataset with information about the packets. Subsequently, a machine learning algorithm was developed to detect benign users from malicious ones.

## Table of Contents

- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Datasets](#datasets)
- [Installation](#installation)
- [Usage](#usage)
- [Model](#model)
- [Results](#results)
- [Contributing](#contributing)

## Introduction

The goal of this project is to simulate a virtual IPv6 network, capture traffic data, and use this data to train a machine learning model to distinguish between benign and malicious users. The project leverages Mininet for network simulation and various Python libraries for data processing and machine learning.

## Project Structure

```
IPv6_Traffic/
├── data/
│   ├── traffic_captured_summary.csv
│   └── host_status.csv
├── scripts/
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   └── model_training.py
├── generateTraffic.py
├── main.py
└── README.md
```

- `data/`: Contains the dataset files.
- `scripts/`: Contains the Python scripts for data preprocessing, feature engineering, and model training.
- `generateTraffic.py`: Script to generate traffic in the simulated network.
- `main.py`: Main script to run the machine learning pipeline.
- `README.md`: This file.

## Datasets

The project uses two primary datasets:

1. `traffic_captured_summary.csv`: Contains information about the captured network packets.
2. `host_status.csv`: Contains the status (benign or malicious) of the hosts in the network.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/IPv6_Traffic.git
   cd IPv6_Traffic
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Generate Traffic**:
   Run the script to generate network traffic in the simulated environment.
   ```bash
   python generateTraffic.py
   ```
   
2. **Main Script**:
   You can run the entire pipeline using the main script.
   ```bash
   python main.py
   ```
**Alternatively**

   2. **Data Preprocessing**:
      Run the data preprocessing script to clean and prepare the data.
      ```bash
      python scripts/data_preprocessing.py
      ```
   
   3. **Feature Engineering**:
      Run the feature engineering script to create additional features.
      ```bash
      python scripts/feature_engineering.py
      ```
   
   4. **Model Training**:
      Run the model training script to train the machine learning model.
      ```bash
      python scripts/model_training.py
      ```



## Model

The machine learning model used in this project is a Random Forest classifier. The model is trained to classify network traffic as benign or malicious based on the captured packet data.

## Results

The model achieved an accuracy of 74% on the test set, with balanced precision and recall for both benign and malicious classes.

## Contributing

Contributions are welcome! If you have any ideas or improvements, feel free to open an issue or submit a pull request.
