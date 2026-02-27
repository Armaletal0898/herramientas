import streamlit as st

def apply_styles():
    # --- CONFIGURACIÓN DE COLORES ---
    COLOR_TEXT_SAFE = "#cbd5e1"
    SIDEBAR_BG = "#1e293b"
    
    st.markdown(f"""
        <style>
            /* 1. FONDO GLOBAL DE LA APLICACIÓN */
            .stApp {{ 
                background-color: #0e1117 !important; 
                color: #ffffff !important; 
            }}

            /* 2. SIDEBAR (BARRA LATERAL) */
            [data-testid="stSidebar"] {{ 
                background-color: {SIDEBAR_BG} !important; 
                border-right: 1px solid #334155 !important; 
            }}
            
            /* Asegurar que el contenedor interno del sidebar sea oscuro */
            [data-testid="stSidebar"] > div:first-child {{
                background-color: {SIDEBAR_BG} !important;
            }}

            /* Estilo para los títulos y textos en el Sidebar */
            [data-testid="stSidebar"] .stMarkdown p, 
            [data-testid="stSidebar"] h1, 
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3 {{
                color: {COLOR_TEXT_SAFE} !important;
            }}

            /* 3. INPUTS (CAMPOS DE TEXTO) */
            [data-testid="stSidebar"] .stTextInput>div>div>input {{
                background-color: #0f172a !important; 
                color: white !important; 
                border: 1px solid #475569 !important;
                border-radius: 5px;
            }}

            /* 4. BOTONES */
            .stButton>button {{
                border-radius: 8px !important;
                transition: all 0.3s ease;
            }}

            /* 5. TARJETAS DE MÉTRICAS (Auditoría) */
            .metric-card {{
                background-color: #1e2130; 
                padding: 15px; 
                border-radius: 10px;
                border: 1px solid #333; 
                text-align: center; 
                margin-bottom: 10px;
            }}
            .metric-label {{ font-size: 14px; color: #aaa; }}
            .metric-value {{ font-size: 24px; font-weight: bold; color: {COLOR_TEXT_SAFE}; }}

            /* 6. CUADRO DE INFORMACIÓN (Infraestructura/SSL) */
            .info-box {{
                background-color: #1e2130; 
                padding: 20px; 
                border-radius: 10px;
                border: 1px solid #334155; 
                height: 100%;
                color: white;
            }}
            .info-box h4 {{ color: #ffffff !important; margin-top: 0; }}

            /* 7. ESTILO DE LAS PESTAÑAS (TABS) */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
                background-color: transparent;
            }}
            .stTabs [data-baseweb="tab"] {{
                background-color: #1e2130;
                border-radius: 5px 5px 0px 0px;
                color: {COLOR_TEXT_SAFE};
                padding: 8px 16px;
                border: 1px solid #334155;
            }}
            .stTabs [aria-selected="true"] {{
                background-color: #334155 !important;
                border-bottom: 2px solid #e59a94 !important;
            }}

            /* 8. RADIO BUTTONS DEL MENÚ */
            [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
                color: {COLOR_TEXT_SAFE};
            }}
        </style>
    """, unsafe_allow_html=True)
