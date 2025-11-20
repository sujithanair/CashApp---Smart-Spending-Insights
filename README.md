# 💸 SpendSmart – Personal Finance Dashboard

SpendSmart is an interactive Streamlit-based dashboard that analyzes your personal spending patterns, identifies trends, compares budgets vs. actual spend, and generates AI-powered financial insights.

This project is designed as a showpiece for data analysis, visualization, and end-to-end app development.

---

## 🚀 Features

### **1. Upload & Analyze Transactions**

* Upload a CSV of your spending data
* Automatic data cleaning, categorization, and aggregation
* Monthly trend breakdown and category-level insights

### **2. Interactive Dashboards**

* Spending by category (bar charts)
* Monthly spend trends (line charts)
* Budget vs actual spend comparison

### **3. Smart Budget Suggestions**

* Automatically calculates recommended monthly budgets per category
* Flags over-budget categories with explanations

### **4. 🤖 AI-Powered Financial Insights**

Uses the OpenAI API to provide:

* Personalized financial summary
* Budget review explanation
* Savings recommendations
* A 3-step action plan

---

## 📁 Project Structure

```
smart-spending-insights/
├── streamlit_app.py        # Main Streamlit app
├── analysis.py             # Data processing + analysis logic
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
```

---

## 🧩 How It Works

### **1. Upload CSV**

Your file is processed into a clean DataFrame with:

* Date normalization
* Category grouping
* Merchant-level spend
* Monthly spend aggregation

### **2. Analysis Engine (`analysis.py`)**

This computes:

* Total spend
* Biggest spend category
* Fastest-growing category
* Category ranking

### **3. Visualization Layer**

Built using **Altair**, with interactive charts embedded in Streamlit.

### **4. AI Insights**

Uses the OpenAI SDK (`openai>=1.0.0`) to generate:

* Personalized commentary
* Budget interpretation
* Actionable financial advice

---

## 🛠️ Installation & Setup

### **1. Clone the repo**

```bash
git clone https://github.com/yourusername/smart-spending-insights.git
cd smart-spending-insights
```

### **2. Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Run the Streamlit app**

```bash
streamlit run streamlit_app.py
```

---

## 🔑 OpenAI API Key

This app uses the **new OpenAI Python client**.

You must set your API key in Streamlit’s sidebar or via environment variable:

```bash
export OPENAI_API_KEY="your_key_here"
```

Get your key from:
➡️ [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

---

## 🧪 Sample Transactions File

Format:

```
date,merchant,category,amount
2024-01-01,HEB,Groceries,52.30
2024-01-03,Uber,Transport,18.25
...
```

---

## 🎯 Future Enhancements

* Predictive spend forecasting (ARIMA / Prophet)
* Category-level anomaly detection
* Savings goal tracker
* Cash flow projections

---




If you’d like, I can also generate a **requirements.txt**, **screenshots section**, or a polished **GitHub descripti
