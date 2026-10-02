"""Medi-Guard AI modern healthcare design system for Streamlit & Plotly."""

from __future__ import annotations
import streamlit as st


def inject_styles() -> None:
    """Injects modern, professional healthcare UI CSS styles into Streamlit."""
    st.markdown(
        """
        <style>
        /* Import clean modern typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }

        /* App background styling - Professional Clean Healthcare palette */
        .stApp {
            background-color: #F8FAFC !important;
            color: #1E293B !important;
        }

        /* Header gradient styling */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif !important;
            color: #0F172A !important;
            font-weight: 700 !important;
        }
        
        .main-title-gradient {
            background: linear-gradient(135deg, #0284C7 0%, #0369A1 50%, #0D9488 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            margin-bottom: 0.2rem !important;
            padding-bottom: 4px !important;
        }

        .subtitle-text {
            color: #475569 !important;
            font-size: 1.05rem !important;
            margin-bottom: 1.2rem !important;
            font-weight: 500 !important;
        }

        /* Educational Disclaimer Banner */
        .disclaimer-banner {
            background-color: #EFF6FF !important;
            border-left: 4px solid #0284C7 !important;
            color: #1E40AF !important;
            padding: 12px 16px !important;
            border-radius: 6px !important;
            font-size: 0.88rem !important;
            margin-bottom: 18px !important;
            line-height: 1.45 !important;
        }

        /* Custom Cards */
        .med-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 20px 24px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
            margin-bottom: 16px !important;
        }
        
        .blue-title {
            color: #0284C7 !important;
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            margin: 0 0 8px 0 !important;
        }
        
        .small-muted {
            color: #64748B !important;
            font-size: 0.92rem !important;
            line-height: 1.5 !important;
        }

        /* Metric Cards - Modern Healthcare styling */
        div[data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            padding: 16px 20px !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03) !important;
        }
        div[data-testid="stMetric"] label {
            color: #64748B !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #0F172A !important;
            font-size: 1.85rem !important;
            font-weight: 700 !important;
        }

        /* Form Container */
        div[data-testid="stForm"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 24px !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03) !important;
        }

        /* Input Controls */
        input[type="text"], input[type="number"], div[data-baseweb="select"] {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 6px !important;
        }

        /* Buttons styling */
        div.stButton > button, button[data-testid="stFormSubmitButton"] {
            background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 22px !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 6px rgba(2, 132, 201, 0.2) !important;
        }
        div.stButton > button:hover, button[data-testid="stFormSubmitButton"]:hover {
            box-shadow: 0 4px 12px rgba(2, 132, 201, 0.35) !important;
            color: #FFFFFF !important;
        }

        /* Triage alert styling */
        .triage-alert-Normal {
            background-color: #F0FDF4 !important;
            border: 1px solid #BBF7D0 !important;
            color: #15803D !important;
            padding: 16px 20px !important;
            border-radius: 8px !important;
            margin-bottom: 16px !important;
        }
        .triage-alert-Moderate {
            background-color: #FEFCE8 !important;
            border: 1px solid #FEF08A !important;
            color: #A16207 !important;
            padding: 16px 20px !important;
            border-radius: 8px !important;
            margin-bottom: 16px !important;
        }
        .triage-alert-Urgent {
            background-color: #FFF7ED !important;
            border: 1px solid #FFEDD5 !important;
            color: #C2410C !important;
            padding: 16px 20px !important;
            border-radius: 8px !important;
            margin-bottom: 16px !important;
        }
        .triage-alert-Critical {
            background-color: #FEF2F2 !important;
            border: 1px solid #FCA5A5 !important;
            color: #B91C1C !important;
            padding: 16px 20px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            margin-bottom: 16px !important;
        }

        /* Streamlit Tab styling */
        button[data-baseweb="tab"] {
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            color: #475569 !important;
        }
        button[aria-selected="true"] {
            color: #0284C7 !important;
            border-bottom-color: #0284C7 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def apply_plot_theme(fig) -> None:
    """Modifies a Plotly figure for clean presentation on light healthcare background."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#475569", family="Inter, sans-serif"),
        xaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1", zerolinecolor="#CBD5E1"),
        yaxis=dict(gridcolor="#E2E8F0", linecolor="#CBD5E1", zerolinecolor="#CBD5E1")
    )
