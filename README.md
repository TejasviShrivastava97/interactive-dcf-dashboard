# Interactive DCF & Valuation Dashboard 💹

This project is an **interactive financial modeling and valuation dashboard** built with **Streamlit**.  
It allows users to:
- Upload financial data (CSV format)
- Adjust assumptions (growth rates, WACC, terminal growth, etc.)
- See valuation metrics (NPV, Terminal Value, Enterprise Value)
- Explore visuals (revenue, EBITDA, FCFF, sensitivity heatmaps)
- Export results to Excel/PDF for reporting

## Tech Stack
- Python (pandas, numpy)
- Streamlit (for the dashboard)
- Plotly (for interactive charts)
- XlsxWriter & ReportLab (for exports)

## How to Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
