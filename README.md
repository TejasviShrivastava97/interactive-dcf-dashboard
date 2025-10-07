# 💹 Interactive DCF & Valuation Dashboard

An interactive **Discounted Cash Flow (DCF) and Valuation Dashboard** built with **Streamlit**, **Plotly**, and **Pandas**.  
This project simulates the workflow of an **Equity Research / Financial Analyst**, helping visualize valuation metrics and financial assumptions dynamically.

---

## 🚀 **Project Overview**

This dashboard provides a professional, easy-to-use interface for performing **DCF valuation**, **scenario analysis**, and **sensitivity analysis**.  
It’s designed for finance students, analysts, and professionals who want to **analyze company valuations** interactively and visualize the effects of changing key assumptions.

---

## 🧠 **Key Features**

✅ **DCF Valuation Model**  
- Projects Free Cash Flows (FCFF) over multiple years  
- Calculates Present Value, Terminal Value, and Enterprise Value  

✅ **Scenario Analysis**  
- Simulates **Best**, **Base**, and **Worst** cases  
- Adjusts growth rate, WACC, and terminal growth for each scenario  

✅ **Interactive Charts (Plotly)**  
- FCFF projections  
- Sensitivity heatmap (WACC vs Terminal Growth)  
- Revenue and EBITDA visualizations  

✅ **CSV Upload Option**  
- Users can upload their own financial data to analyze real companies  

✅ **Export Options**  
- Download valuation results to **Excel** or **PDF** reports (using `xlsxwriter` and `reportlab`)  

---

## 🧾 **Sample Data Format (CSV Upload)**

Your uploaded CSV should look like this:

```csv
Year,Revenue,EBITDA,CapEx,Depreciation,Change_in_Working_Capital
2025,1000,200,50,30,10
2026,1100,220,55,33,12
2027,1210,242,60,36,14
2028,1331,266,65,40,16
2029,1464,293,70,44,18
```

---

## 🧩 **Tech Stack**

| Category | Tools Used |
|-----------|-------------|
| Frontend | Streamlit, Plotly |
| Backend  | Python, Pandas, Numpy |
| Visualization | Plotly Graph Objects, Express |
| Reporting | XlsxWriter, ReportLab |
| Hosting | Streamlit Community Cloud |

---

## 🧠 **What You’ll Learn**

By exploring this project, you’ll understand:
- How DCF valuation models work  
- How to calculate and visualize terminal value and sensitivity analysis  
- How to build finance dashboards in Streamlit  
- How to combine financial modeling and data visualization in Python  

---

## ⚙️ **Run Locally**

To run this app on your system:

```bash
# Clone the repo
git clone https://github.com/TejasviShrivastava97/interactive-dcf-dashboard.git

# Navigate to project folder
cd interactive-dcf-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open your browser at [http://localhost:8501](http://localhost:8501)

---

## 🌐 **Live App**

👉 **View the live dashboard here:**  
🔗 [Streamlit Live App](https://interactive-dcf-dashboard-upwbzt2kdeu9mv5oxcfv4k.streamlit.app/)


---

## 🧑‍💼 **About the Creator**

👋 **Created by [Tejasvi Shrivastava](https://www.linkedin.com/in/tejasvishrivastava97/)**  
MBA in Business Analytics | Financial Modeling & Valuation Enthusiast | Aspiring Financial Analyst  

This project demonstrates end-to-end financial modeling, valuation, and dashboard design skills.

---

## ⭐ **Support**

If you find this project useful:
- Give the repo a ⭐ on GitHub  
- Share your feedback on [LinkedIn](https://www.linkedin.com/in/tejasvishrivastava97/)  

---
