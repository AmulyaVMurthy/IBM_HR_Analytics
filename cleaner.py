import pandas as pd
from sklearn.preprocessing import LabelEncoder

class HRDataCleaner:
    def __init__(self, dataframe):
        self.df = dataframe

    def remove_useless_columns(self):
        cols_to_drop = ['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber']
        # Use errors='ignore' in case they were already dropped
        self.df = self.df.drop(columns=cols_to_drop, errors='ignore')
        return self.df

    def encode_categories(self):
        # 1. Manually fix binary columns (Yes/No, Gender)
        binary_cols = ['Attrition', 'OverTime', 'Gender']
        le = LabelEncoder()
        for col in binary_cols:
            if col in self.df.columns:
                self.df[col] = le.fit_transform(self.df[col])

        # 2. Automatically find remaining text columns and One-Hot Encode them
        # This fixes 'BusinessTravel', 'Department', 'JobRole', etc.
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        self.df = pd.get_dummies(self.df, columns=categorical_cols)
        
        return self.df