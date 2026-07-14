"""MediGuard AI custom styling library for Streamlit & Plotly."""

from __future__ import annotations
import streamlit as st

def inject_styles() -> None:
    """Injects custom CSS to style Streamlit app elements for a premium dark mode UI."""
    st.markdown(
        """
        <style>
        /* Force deep dark space medical dashboard theme */
        .stApp {
            background: radial-gradient(circle at top left, #0D1326 0%, #070B16 100%) !important;
            color: #E2E8F0 !important;
        }

        /* Title gradient styling */
        h1, h2, h3 {
            color: #FFFFFF !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .main-title-gradient {
            background: linear-gradient(135deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-size: 2.8rem !important;
            margin-bottom: 0px !important;
            padding-bottom: 5px !important;
        }
        
        /* Metric blocks - customized glassmorphism */
        div[data-testid="stMetric"] {
            background: rgba(19, 28, 59, 0.45) !important;
            border: 1px solid rgba(56, 189, 248, 0.12) !important;
            border-radius: 12px !important;
            padding: 18px 22px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            border-color: rgba(56, 189, 248, 0.25) !important;
            box-shadow: 0 8px 32px 0 rgba(2, 132, 201, 0.1) !important;
            transform: translateY(-2px);
        }
        div[data-testid="stMetric"] label {
            color: #94A3B8 !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.8px !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 2.1rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
            font-size: 0.9rem !important;
            font-weight: 600 !important;
        }

        /* Glassmorphic Cards */
        .med-card {
            background: rgba(19, 28, 59, 0.45) !important;
            border: 1px solid rgba(56, 189, 248, 0.12) !important;
            border-radius: 12px !important;
            padding: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(12px);
            margin-bottom: 15px !important;
            transition: all 0.3s ease;
        }
        .med-card:hover {
            border-color: rgba(56, 189, 248, 0.25) !important;
        }
        
        .blue-title {
            color: #38BDF8 !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
            margin: 0 0 10px 0 !important;
            letter-spacing: 0.5px !important;
            background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .small-muted {
            color: #94A3B8 !important;
            font-size: 0.92rem !important;
            line-height: 1.5 !important;
        }

        /* Form container styling */
        div[data-testid="stForm"] {
            background: rgba(15, 23, 42, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 16px !important;
            padding: 25px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        }

        /* Custom Inputs & Selectboxes */
        input[type="text"], input[type="number"], div[data-baseweb="select"] {
            background-color: #0F172A !important;
            color: #F1F5F9 !important;
            border: 1px solid #1E293B !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #0F172A !important;
            color: #F1F5F9 !important;
            border: none !important;
        }
        
        /* Sliders */
        .stSlider {
            color: #38BDF8 !important;
        }

        /* Buttons styling */
        div.stButton > button, button[data-testid="stFormSubmitButton"] {
            background: linear-gradient(135deg, #0284C7 0%, #4F46E5 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(2, 132, 201, 0.2) !important;
            transition: all 0.3s ease !important;
        }
        div.stButton > button:hover, button[data-testid="stFormSubmitButton"]:hover {
            box-shadow: 0 6px 20px rgba(2, 132, 201, 0.4) !important;
            transform: translateY(-1px) !important;
            color: #FFFFFF !important;
            border: none !important;
        }

        /* Custom Triage alert status box styling */
        .triage-alert-Normal {
            background-color: rgba(16, 185, 129, 0.08) !important;
            border: 1px solid rgba(16, 185, 129, 0.25) !important;
            color: #34D399 !important;
            padding: 16px 20px !important;
            border-radius: 10px !important;
            margin-bottom: 20px !important;
        }
        .triage-alert-Moderate {
            background-color: rgba(245, 158, 11, 0.08) !important;
            border: 1px solid rgba(245, 158, 11, 0.25) !important;
            color: #FBBF24 !important;
            padding: 16px 20px !important;
            border-radius: 10px !important;
            margin-bottom: 20px !important;
        }
        .triage-alert-Urgent {
            background-color: rgba(239, 68, 68, 0.08) !important;
            border: 1px solid rgba(239, 68, 68, 0.25) !important;
            color: #F87171 !important;
            padding: 16px 20px !important;
            border-radius: 10px !important;
            margin-bottom: 20px !important;
        }
        .triage-alert-Critical {
            background-color: rgba(185, 28, 28, 0.12) !important;
            border: 1px solid rgba(185, 28, 28, 0.35) !important;
            color: #F87171 !important;
            padding: 16px 20px !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            margin-bottom: 20px !important;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.85; }
            50% { opacity: 1; }
            100% { opacity: 0.85; }
        }

        /* Dataframe theme adjustments */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            overflow: hidden !important;
        }
        
        /* Expander panel styling */
        div[data-testid="stExpander"] {
            background: rgba(19, 28, 59, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def apply_plot_theme(fig) -> None:
    """Modifies a Plotly figure to fit beautifully into the dark mode design system."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Inter, sans-serif"),
        xaxis=dict(gridcolor="#1E293B", linecolor="#1E293B", zerolinecolor="#1E293B"),
        yaxis=dict(gridcolor="#1E293B", linecolor="#1E293B", zerolinecolor="#1E293B")
    )
