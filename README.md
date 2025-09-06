Automated Loan Eligibility & Suggestion System

📌 Project Overview

This project implements a machine learning–based system for forecasting customers’ loan eligibility and recommending suitable credit limits. The solution uses a two-stage pipeline:

Classification – Predicts whether an applicant is eligible for a loan.

Hybrid Regression (Clustering + XGBoost) – For ineligible applicants, suggests an alternative loan amount based on financial and demographic patterns.

The system is designed to support financial institutions in minimizing lending risks while providing applicants with constructive alternatives instead of outright rejection.


⚙️ Features

Supervised ML models for loan eligibility classification.

Hybrid algorithm: K-Means clustering + Regression (XGBoost, CatBoost, LightGBM, Random Forest) for loan amount prediction.

End-to-end ML pipeline: preprocessing, feature engineering, balancing, model tuning.

Streamlit-based web application for user interaction.

MySQL database integration for applicant and prediction data.


📊 Machine Learning Workflow

Data preprocessing (missing values, outliers, encoding, scaling).

Loan eligibility prediction using RandomForestClassifier (tuned with GridSearchCV).

For rejected applications → K-Means clustering → Regression model predicts suitable loan amount.

Results stored in database & shown in UI.

👨‍💻 Author

Developed by Ramosh Drushal Samarwickrama
📧 ramshsamarawickrama@gmail.com
