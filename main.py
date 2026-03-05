import sqlite3
import pandas as pd
from cleaner import HRDataCleaner
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

def run_pipeline():
    # --- STEP 1: DATABASE CONNECTION ---
    conn = sqlite3.connect('hr_analytics.db')
    
    
    # --- STEP 2: SQL INSIGHTS ---
    print(">>> RUNNING SQL ANALYSIS...")
    query = "SELECT Department, COUNT(*) as Total FROM attrition_data WHERE Attrition = 'Yes' GROUP BY Department"
    sql_results = pd.read_sql_query(query, conn)
    print(sql_results)

    # --- STEP 3: DATA PREPARATION ---
    raw_df = pd.read_sql_query("SELECT * FROM attrition_data", conn)
    cleaner = HRDataCleaner(raw_df)
    
    # Apply our cleaning class methods
    cleaner = HRDataCleaner(raw_df)
    tableau_df = cleaner.remove_useless_columns()
     # Export the processed data for Tableau
    tableau_df.to_csv('data/hr_tableau_friendly.csv', index=False)
    print("✅ Tableau-friendly CSV exported with proper field names!")
    #  NOW performing the encoding for the Machine Learning model
    # This creates the 1s and 0s needed for the RandomForest
    processed_df = cleaner.encode_categories()

    
    
    # --- STEP 4: MACHINE LEARNING (The "Predictor") ---
    # Split data into Features (X) and Target (y)
    X = processed_df.drop('Attrition', axis=1)
    y = processed_df['Attrition']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and Train Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # --- STEP 5: EVALUATION ---
    predictions = model.predict(X_test)
    print("\n>>> MODEL PERFORMANCE REPORT:")
    print(classification_report(y_test, predictions))
    
    # --- STEP 6: FEATURE IMPORTANCE (The 'Why') ---
    importances = pd.Series(model.feature_importances_, index=X.columns)
    print("\n>>> TOP 5 REASONS FOR ATTRITION:")
    print(importances.sort_values(ascending=False).head(5))



    conn.close()

if __name__ == "__main__":
    run_pipeline()
    