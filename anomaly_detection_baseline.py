import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("C:/Users/hp/Desktop/google/merged_data.csv")

# Preview
print(df.head())

df_long = df.melt(id_vars=["Date"], 
                  var_name="Keyword", 
                  value_name="Search_Volume")

print(df_long.head())

df_long["Date"] = pd.to_datetime(df_long["Date"], dayfirst=True)


# Group by keyword and calculate rolling mean/std to catch anomalies
df_long["Rolling_Mean"] = df_long.groupby("Keyword")["Search_Volume"].transform(lambda x: x.rolling(7, min_periods=1).mean())
df_long["Rolling_STD"]  = df_long.groupby("Keyword")["Search_Volume"].transform(lambda x: x.rolling(7, min_periods=1).std())

# Define anomaly condition (value far from rolling mean)
df_long["Anomaly"] = np.where(
    (df_long["Search_Volume"] > df_long["Rolling_Mean"] + 2*df_long["Rolling_STD"]) |
    (df_long["Search_Volume"] < df_long["Rolling_Mean"] - 2*df_long["Rolling_STD"]),
    1, 0
)

# See some anomalies
print(df_long[df_long["Anomaly"] == 1].head(20))

#What this does:
#For each keyword, takes a 7-day rolling average and standard deviation.
#Flags days where search volume jumps/drops >2 standard deviations from normal.
#Creates a new column "Anomaly" with 1 = anomaly, 0 = normal.


# Choose one keyword to visualize (example: DataAnalytics)
keyword = "DataAnalytics"
df_plot = df_long[df_long["Keyword"] == keyword]

plt.figure(figsize=(14,6))
plt.plot(df_plot["Date"], df_plot["Search_Volume"], label="Search Volume", color="blue")
plt.scatter(
    df_plot[df_plot["Anomaly"]==1]["Date"],
    df_plot[df_plot["Anomaly"]==1]["Search_Volume"],
    color="red", label="Anomaly", marker="o", s=80
)

plt.title(f"Search Trends with Anomalies - {keyword}", fontsize=16, fontweight="bold")
plt.xlabel("Date", fontsize=12)
plt.ylabel("Search Volume", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

#This will create individual anomaly charts for every keyword in the dataset.
keywords = df_long["Keyword"].unique()

for keyword in keywords:
    df_plot = df_long[df_long["Keyword"] == keyword]

    plt.figure(figsize=(14,6))
    plt.plot(df_plot["Date"], df_plot["Search_Volume"], label="Search Volume", color="blue")
    plt.scatter(
        df_plot[df_plot["Anomaly"]==1]["Date"],
        df_plot[df_plot["Anomaly"]==1]["Search_Volume"],
        color="red", label="Anomaly", marker="o", s=80
    )

    plt.title(f"Search Trends with Anomalies - {keyword}", fontsize=16, fontweight="bold")
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Search Volume", fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# This give the average search trends per month + % growth/decline for each keyword.

# Add Month-Year column
df_long["Month_Year"] = df_long["Date"].dt.to_period("M")

# Calculate monthly average search volume
monthly_trends = df_long.groupby(["Month_Year", "Keyword"])["Search_Volume"].mean().reset_index()

# Calculate month-over-month growth
monthly_trends["Growth_Rate"] = monthly_trends.groupby("Keyword")["Search_Volume"].pct_change() * 100

print(monthly_trends.head(15))


#Find Top 5 Growing & Declining Skills over time.

# Get last available month and previous month
latest_month = monthly_trends["Month_Year"].max()
prev_month = latest_month - 1

# Compare last vs previous month
latest_data = monthly_trends[monthly_trends["Month_Year"] == latest_month]
prev_data = monthly_trends[monthly_trends["Month_Year"] == prev_month]

# Merge to compare growth
compare = pd.merge(latest_data, prev_data, on="Keyword", suffixes=("_latest", "_prev"))

# Calculate growth
compare["Change"] = ((compare["Search_Volume_latest"] - compare["Search_Volume_prev"]) / compare["Search_Volume_prev"]) * 100

# Top 5 increasing skills
top5_up = compare.sort_values("Change", ascending=False).head(5)

# Top 5 declining skills
top5_down = compare.sort_values("Change").head(5)

print("🔥 Top 5 Growing Skills:\n", top5_up[["Keyword", "Change"]])
print("\n📉 Top 5 Declining Skills:\n", top5_down[["Keyword", "Change"]])

# Check overall trend (2019–2024) for each skill.

monthly_trends["Month_Year"] = monthly_trends["Month_Year"].astype(str)

plt.figure(figsize=(12,6))

for skill in df_long["Keyword"].unique():
    skill_trend = monthly_trends[monthly_trends["Keyword"] == skill]
    plt.plot(skill_trend["Month_Year"], skill_trend["Search_Volume"], label=skill)

plt.title("Skill Demand Trends (2019–2024)")
plt.xlabel("Year")
plt.ylabel("Search Volume")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Create a ranking of top 10 skills across all years by average demand.

top_skills = (
    monthly_trends.groupby("Keyword")["Search_Volume"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print(top_skills)

#Year-wise Demand Ranking (Trend Shift Detection)
#This table show demand of each skill across different years.
#It helps us detect anomalies, growth trends, and decline.
monthly_trends["Month_Year"] = pd.to_datetime(monthly_trends["Month_Year"])
monthly_trends["Year"] = monthly_trends["Month_Year"].dt.year

yearly_trends = (
    monthly_trends.groupby(["Year", "Keyword"])["Search_Volume"]
    .mean()
    .reset_index()
)

# Sort skills by year and demand
pivot_yearly = yearly_trends.pivot(index="Keyword", columns="Year", values="Search_Volume")
print(pivot_yearly.head(10))

#create a heatmap to show skills demand trend across years.

import seaborn as sns

plt.figure(figsize=(12,6))
sns.heatmap(pivot_yearly, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Yearly Demand Trends for Skills")
plt.ylabel("Skills")
plt.xlabel("Year")
plt.tight_layout()
plt.show()

# Calculate year-over-year growth for each skill
growth_rate = yearly_trends.copy()
growth_rate["Growth_Rate"] = growth_rate.groupby("Keyword")["Search_Volume"].pct_change() * 100

print(growth_rate.head(15))

#find the top 5 fastest-growing skills in the latest year.
# Get the latest year
latest_year = growth_rate["Year"].max()

# Filter growth rate for the latest year
latest_growth = growth_rate[growth_rate["Year"] == latest_year]

# Top 5 fastest-growing skills
top_growth = latest_growth.sort_values("Growth_Rate", ascending=False).head(5)
print(top_growth)

#Visualize the top 5 fastest-growing skills in the latest year.
plt.figure(figsize=(8,5))
plt.bar(top_growth["Keyword"], top_growth["Growth_Rate"], color="skyblue")
plt.title(f"Top 5 Fastest-Growing Skills in {latest_year}")
plt.xlabel("Skills")
plt.ylabel("Growth Rate (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

#Find the 5 most declining skills (falling demand) in the latest year.
# Calculate growth rates for each keyword over time
declining_skills = yearly_trends.groupby("Keyword")["Search_Volume"].pct_change().reset_index()
declining_skills = declining_skills.rename(columns={"Search_Volume": "Growth_Rate"})

# Add Year + Keyword back (to align properly)
declining_skills = declining_skills.merge(yearly_trends[["Year", "Keyword"]], left_index=True, right_index=True)

# Get the most recent year
latest_year = yearly_trends["Year"].max()

# Filter for latest year
latest_decline = declining_skills[declining_skills["Year"] == latest_year].dropna()

# Bottom 5 declining skills
bottom_decline = latest_decline.nsmallest(5, "Growth_Rate")

print("Bottom 5 Declining Skills:")
print(bottom_decline)

