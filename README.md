Customer Engagement & Product Utilization Analytics for Retention Strategy

An interactive analytics dashboard built with Python, Pandas, Plotly, and Streamlit to explore customer engagement, product utilization, and retention patterns in banking.

🔗 Project Links
Live Dashboard: customerengagementretentionanalytics-4zcqxhz53hucatvziukjqx.streamlit.app
GitHub Repository: https://github.com/tbhanukarthik325-oss/Customer_Engagement_Retention_Analytics.git

📌 Project Overview

Customer retention is an important challenge for banking institutions. Understanding customer engagement, product usage, and financial relationships can help organizations identify patterns associated with customer exits.

This project analyzes banking customer data and presents the findings through an interactive dashboard. It focuses on descriptive analytics, helping users explore customer characteristics and retention patterns rather than predicting future customer behavior.

🎯 Objectives
Analyze customer exit and retention rates.
Examine engagement levels and product utilization.
Explore retention patterns across age groups, gender, and geography.
Investigate relationships between customer balances and engagement.
Analyze credit card ownership and customer retention.
Create descriptive customer segments based on behavioral characteristics.
Present findings through an interactive Streamlit dashboard.
📊 Dataset Overview

The project uses the European_Bank.csv dataset.
| Attribute                | Description                  |
| ------------------------ | ---------------------------- |
| Original dataset rows    | 10,000                       |
| Original dataset columns | 14                           |
| Enriched dataset rows    | 10,000                       |
| Enriched dataset columns | 19                           |
| Target variable          | `Exited`                     |
| Missing values           | None found during validation |
| Duplicate rows           | None found during validation |

The enriched dataset, customer_retention_analysis.csv, includes additional analytical fields used to explore customer relationships and behavioral segments.

🛠️ Technologies Used
Python — data analysis and application logic
Pandas — data manipulation and analysis
NumPy — numerical operations
Plotly — interactive charts
Streamlit — interactive web dashboard
Matplotlib & Seaborn — exploratory data visualization
Jupyter Notebook — exploratory data analysis

🔍 Key Analysis Areas
1. Customer Engagement

Explores active and inactive customers and compares exit rates across engagement groups.

2. Product Utilization

Examines product counts and their relationship with customer retention patterns.

3. Financial Commitment

Investigates account balances and disengagement among high-balance customers.

4. Credit Card Analysis

Explores credit card ownership and retention patterns.

5. Relationship Strength

Uses a descriptive score based on activity status, product ownership, and credit card ownership.

6. Behavioral Segmentation

Groups customers into descriptive segments to support further investigation of retention patterns.
7. Demographic Analysis

Explores customer patterns by age group, gender, and geography.

8. Interactive Customer Explorer

Allows users to filter customers using engagement status, product count, minimum balance, and minimum estimated salary.

📈 Key Performance Indicators

The analysis includes the following descriptive metrics:
| KPI                         |  Value | Description                                        |
| --------------------------- | -----: | -------------------------------------------------- |
| Overall Exit Rate           | 20.37% | Percentage of customers who exited                 |
| Product Depth Index         |   1.53 | Average number of products held                    |
| Relationship Strength Index |   1.71 | Average of the defined relationship-strength score |

Note: These metrics describe patterns in the available dataset. They do not establish causation or demonstrate predictive accuracy.

🚀 Run the Project Locally
Step 1: Clone the repository
git clone https://github.com/tbhanukarthik325-oss/Customer_Engagement_Retention_Analytics.git

Step 2: Navigate to the project folder
cd Customer_Engagement_Retention_Analytics

Step 3: Create and activate a virtual environment (optional)

Windows:
python -m venv venv
venv\Scripts\activate

Step 4: Install dependencies
pip install -r requirements.txt

Step 5: Launch the dashboard
streamlit run app.py

Then The dashboard should open in your browser

📁 Project Structure

Customer_Engagement_Retention_Analytics/
│
├── data/
│   ├── European_Bank.csv
│   └── customer_retention_analysis.csv
│
├── images/
│
├── notebooks/
│   └── customer_retention_eda.ipynb
│
├── app.py
├── README.md
└── requirements.txt

💡 Key Takeaways

This project demonstrates how exploratory data analysis and interactive visualization can help investigate customer engagement and retention patterns. The dashboard allows users to explore relationships between activity, product utilization, customer demographics, and exit behavior.

The findings are descriptive and should be interpreted in the context of the available dataset. They do not, by themselves, prove why customers leave.

🔮 Future Enhancements
Add time-based retention analysis if historical records are available.
Introduce customer cohort analysis.
Add explainable predictive modeling as a separate, validated extension.
Improve dashboard export and reporting features.
Evaluate retention strategies using appropriate business data.

👨‍💻 Author:
Tirumalakonda Bhanu Karthik
Department: CSE (Data Science)
