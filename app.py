import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="Equity Research & Valuation Dashboard", layout="wide", page_icon="📊")
st.title("📊 Equity Research & Valuation Dashboard")

# ----------------- SIDEBAR INPUTS -----------------
st.sidebar.header("Valuation Inputs")
forecast_years = st.sidebar.slider("Forecast Years", 3, 10, 5)
wacc = st.sidebar.slider("Discount Rate (WACC %)", 1.0, 20.0, 10.0) / 100
terminal_growth = st.sidebar.slider("Terminal Growth Rate (%)", 0.0, 6.0, 2.0) / 100
fcff_initial = st.sidebar.number_input("Initial FCFF (millions)", 100, 10000, 1000)
growth_rate = st.sidebar.slider("FCFF Growth Rate (%)", 0.0, 20.0, 5.0) / 100
market_cap = st.sidebar.number_input("Current Market Cap (millions)", 100, 50000, 15000)

# ----------------- PROJECTED FCFF -----------------
years = np.arange(1, forecast_years + 1)
fcff = [fcff_initial * ((1 + growth_rate) ** i) for i in range(forecast_years)]

def dcf_calc(fcffs, wacc, tg):
    pv_fcffs = sum([fcff / ((1 + wacc) ** (i+1)) for i, fcff in enumerate(fcffs)])
    terminal_value = fcffs[-1] * (1 + tg) / (wacc - tg)
    pv_terminal = terminal_value / ((1 + wacc) ** len(fcffs))
    return pv_fcffs + pv_terminal, pv_fcffs, pv_terminal

dcf_value, pv_fcffs, pv_terminal = dcf_calc(fcff, wacc, terminal_growth)

# ----------------- COMPS DATA -----------------
comps_df = pd.DataFrame({
    "Company": ["Comp A", "Comp B", "Comp C", "Comp D", "Comp E"],
    "Revenue": [2000, 2500, 1800, 2200, 2600],
    "EBITDA": [400, 500, 350, 420, 480],
    "P/E": [15, 18, 20, 17, 19],
    "EV/EBITDA": [10, 12, 11, 9, 13],
    "Revenue_Growth": [8, 10, 12, 9, 11],
    "Market_Cap": [15000, 18000, 14000, 16000, 20000]
})

# Peer multiples
median_pe = comps_df["P/E"].median()
median_ev_ebitda = comps_df["EV/EBITDA"].median()

# Apply multiples
eps_estimate = fcff_initial / 100  # EPS proxy
ebitda_estimate = fcff_initial * 0.8  # EBITDA proxy
pe_valuation = eps_estimate * median_pe
ev_ebitda_valuation = ebitda_estimate * median_ev_ebitda
comps_value = (pe_valuation + ev_ebitda_valuation) / 2
blended_value = (dcf_value + comps_value) / 2

# ----------------- EXPORT FUNCTIONS -----------------
def to_excel(dcf_value, comps_value, blended_value, market_cap, comps_df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Summary Sheet
        summary = pd.DataFrame({
            "Metric": ["DCF Value", "Comps Value", "Blended Value", "Market Cap"],
            "Value (M)": [dcf_value, comps_value, blended_value, market_cap]
        })
        summary.to_excel(writer, index=False, sheet_name="Summary")

        # Comps Sheet
        comps_df.to_excel(writer, index=False, sheet_name="Comps")

    return output.getvalue()

def to_pdf(dcf_value, comps_value, blended_value, market_cap, recommendation):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Equity Valuation Report")

    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"DCF Value: ${dcf_value:,.0f}M")
    c.drawString(100, 680, f"Comps Value: ${comps_value:,.0f}M")
    c.drawString(100, 660, f"Blended Value: ${blended_value:,.0f}M")
    c.drawString(100, 640, f"Market Cap: ${market_cap:,.0f}M")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 600, f"Recommendation: {recommendation}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "DCF Valuation", "Comparable Analysis", "Ratios Dashboard", "Valuation Bridge", "Summary"
])

# --- DCF Tab ---
with tab1:
    st.subheader("Discounted Cash Flow (DCF) Valuation")
    col1, col2, col3 = st.columns(3)
    col1.metric("Enterprise Value (DCF)", f"${dcf_value:,.0f}M")
    col2.metric("PV of Cash Flows", f"${pv_fcffs:,.0f}M")
    col3.metric("PV of Terminal Value", f"${pv_terminal:,.0f}M")

    fig_dcf = go.Figure()
    fig_dcf.add_trace(go.Bar(x=years, y=fcff, name="FCFF Projection", marker_color="blue"))
    fig_dcf.update_layout(title="FCFF Projections Over Forecast Period", template="plotly_white")
    st.plotly_chart(fig_dcf, use_container_width=True)

# --- Comps Tab ---
with tab2:
    st.subheader("Comparable Company Analysis (Comps)")
    st.dataframe(comps_df)

    col1, col2 = st.columns(2)
    with col1:
        fig_pe = px.bar(comps_df, x="Company", y="P/E", title="P/E Ratios", text="P/E", color="P/E")
        st.plotly_chart(fig_pe, use_container_width=True)
    with col2:
        fig_ev = px.bar(comps_df, x="Company", y="EV/EBITDA", title="EV/EBITDA Multiples", text="EV/EBITDA", color="EV/EBITDA")
        st.plotly_chart(fig_ev, use_container_width=True)

# --- Ratios Dashboard ---
with tab3:
    st.subheader("Financial Ratios Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        fig_growth = px.line(comps_df, x="Company", y="Revenue_Growth", markers=True, title="Revenue Growth by Peer (%)")
        st.plotly_chart(fig_growth, use_container_width=True)

    with col2:
        fig_scatter = px.scatter(comps_df, x="P/E", y="EV/EBITDA", size="Market_Cap",
                                 color="Revenue_Growth", hover_name="Company",
                                 title="Valuation Multiples vs Growth (Bubble Size = Market Cap)")
        st.plotly_chart(fig_scatter, use_container_width=True)

# --- Valuation Bridge ---
with tab4:
    st.subheader("Valuation Bridge (DCF vs Comps vs Blended)")
    bridge_df = pd.DataFrame({
        "Valuation Method": ["DCF", "Comps", "Blended"],
        "Value": [dcf_value, comps_value, blended_value]
    })
    fig_bridge = px.bar(bridge_df, x="Valuation Method", y="Value", text="Value", color="Valuation Method",
                        title="Valuation Comparison")
    st.plotly_chart(fig_bridge, use_container_width=True)

# --- Summary ---
with tab5:
    st.subheader("Valuation Summary & Recommendation")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("DCF Value", f"${dcf_value:,.0f}M")
    col2.metric("Comps Value", f"${comps_value:,.0f}M")
    col3.metric("Blended Value", f"${blended_value:,.0f}M")
    col4.metric("Market Cap", f"${market_cap:,.0f}M")

    if blended_value > market_cap * 1.2:
        recommendation = "BUY 🚀 (Undervalued)"
        st.success(f"Recommendation: **{recommendation}**")
    elif blended_value < market_cap * 0.8:
        recommendation = "SELL ⚠️ (Overvalued)"
        st.error(f"Recommendation: **{recommendation}**")
    else:
        recommendation = "HOLD 🤝 (Fairly Valued)"
        st.info(f"Recommendation: **{recommendation}**")

    # Export buttons
    st.markdown("### 📤 Export Report")
    excel_data = to_excel(dcf_value, comps_value, blended_value, market_cap, comps_df)
    st.download_button(label="📊 Download Excel Report", data=excel_data, file_name="valuation_report.xlsx", mime="application/vnd.ms-excel")

    pdf_data = to_pdf(dcf_value, comps_value, blended_value, market_cap, recommendation)
    st.download_button(label="📄 Download PDF Report", data=pdf_data, file_name="valuation_report.pdf", mime="application/pdf")
