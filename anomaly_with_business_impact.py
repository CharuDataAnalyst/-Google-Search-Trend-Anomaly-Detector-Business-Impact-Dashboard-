
import pandas as pd
import numpy as np

# 1. Load Datasets

search_df = pd.read_csv("C:/Users/hp/Desktop/google/searchtrend.csv", parse_dates=["Date"])
business_df = pd.read_csv("C:/Users/hp/Desktop/google/business metric.csv", parse_dates=["Date"])
# Melt search trends wide -> long
df_long = search_df.melt(
    id_vars=["Date"],        # Keep Date
    var_name="Keyword",      # Column names become Keyword
    value_name="Search_Volume"  # Values become numeric metric
)
print(df_long)

# -----------------------------
# 2. Merge with business metrics
# -----------------------------
# Melt business dataset into long format for keywords
biz_long = business_df.melt(
    id_vars=["Date", "Website_Traffic", "Sales_Revenue", "Ad_Clicks", "Engagement"],
    var_name="Keyword",
    value_name="Business_Metric"
)

print(biz_long)
# Merge search + business
df = pd.merge(df_long, biz_long, on=["Date", "Keyword"], how="left")
print(df)
# -----------------------------
# 3. Anomaly Detection
# -----------------------------
# Rolling mean & std (7-day window)
df["Rolling_Mean"] = df.groupby("Keyword")["Search_Volume"].transform(
    lambda x: x.rolling(window=7, min_periods=1).mean()
)
df["Rolling_STD"] = df.groupby("Keyword")["Search_Volume"].transform(
    lambda x: x.rolling(window=7, min_periods=1).std()
)

# Z-score
df["Z_Score"] = (df["Search_Volume"] - df["Rolling_Mean"]) / df["Rolling_STD"]

# -----------------------------
# 4. Severity Scoring
# -----------------------------
def classify_severity(z):
    if pd.isna(z):
        return "Normal"
    elif z > 3:
        return "High"
    elif z > 2:
        return "Medium"
    elif z > 1.5:
        return "Low"
    else:
        return "Normal"

df["Severity"] = df["Z_Score"].apply(classify_severity)

# -----------------------------
# 5. Extract anomalies
# -----------------------------
anomalies = df[df["Severity"] != "Normal"].copy()

# Keep only columns needed for dashboard
anomalies = anomalies[[
    "Date", "Keyword", "Search_Volume", "Z_Score", "Severity",
    "Business_Metric", "Website_Traffic", "Sales_Revenue", "Ad_Clicks", "Engagement"
]]

# -----------------------------
# 6. Export CSV
# -----------------------------
anomalies.to_csv("anomalies_with_business_impact.csv", index=False)

print("Pipeline complete. Output saved to anomalies_with_business_impact.csv")
print(anomalies.head(10))