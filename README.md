# -Google-Search-Trend-Anomaly-Detector-Business-Impact-Dashboard-



## 🚀 Project Overview  
Search behavior reflects customer intent — but sudden **spikes or drops in Google search trends** often go unnoticed, leading to missed opportunities or unexpected revenue loss.  

This project uses **BigQuery** to process search trend data and **Power BI** to visualize anomalies alongside business KPIs, creating a dashboard that helps teams quickly detect unusual search behavior and understand its **impact on traffic, sales, and ad spend efficiency.**  

---

## 🎯 Problem Statement  
- Businesses track search data but struggle to **spot anomalies in real time.**  
- Anomalies are rarely **linked to business KPIs** like revenue, traffic, or ad spend.  
- Decision-makers need a clear, **interactive dashboard** to connect search anomalies → business impact → recommended actions.  

---

## 💡 Objectives  
1. Use **BigQuery** for storing, cleaning, and querying large-scale search trend data.  
2. Detect anomalies in keyword-level time-series search data.  
3. Link anomalies to **synthetic business KPIs** (traffic, conversions, sales).  
4. Build a **Power BI dashboard** with anomaly flags, KPI impact cards, and actionable insights.  

---

## 🔧 Tools & Technologies  
- **Data Storage & Querying:** Google BigQuery (SQL, partitioned tables for time-series).  
- **ETL & Processing:** BigQuery SQL (rolling averages, Z-score anomaly detection).  
- **Visualization:** Power BI (interactive dashboard, KPI cards, anomaly highlighting).  
- **Documentation:** GitHub (Markdown storytelling, project files).  

---

## 📊 Approach  

### 1️⃣ Data Collection  
- Pulled keyword search trend data from Google Trends API → loaded into BigQuery.  
- Created synthetic KPI datasets (traffic, sales, ad spend) → uploaded to BigQuery.  

### 2️⃣ Data Processing in BigQuery  
- Cleaned and standardized datasets (daily/weekly aggregation).  
- Applied SQL logic for anomaly detection:  
  - **Rolling averages + standard deviation thresholds**  
  - **Z-scores to highlight unusual spikes/drops**  

### 3️⃣ Business Impact Analysis  
- Linked anomalies in search data to changes in traffic, sales, and ad spend.  
- Quantified impact (e.g., “20% drop in searches → 12% drop in traffic → ~₹50,000 revenue loss”).  

### 4️⃣ Dashboard in Power BI  
- Line charts: Search trends with anomaly points flagged.  
- KPI cards: Impact on sales, traffic, conversions.  
- Drill-down filters: Keyword, region, date range.  
- Insights panel: Business explanation + recommendation.  

---

## 🔍 Example Insight  
- **Anomaly:** Spike in “AI jobs” searches in January.  
- **Impact:** Website traffic to career pages increased by 40%, boosting ad efficiency by 15%.  
- **Recommendation:** Increase recruitment ad budget during high search spikes.  

---

## ✅ Outcomes  
- Automated anomaly detection pipeline using **BigQuery SQL**.  
- Built **interactive Power BI dashboard** that connects anomalies to KPIs.  
- Delivered **business-first insights**, helping teams react to anomalies proactively.  

---

