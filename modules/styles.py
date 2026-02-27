import streamlit as st

def apply_styles():
    """
    Aplica estilos CSS dinámicos que se adaptan automáticamente al tema 
    elegido por el usuario (Light o Dark).
    """
    
    # Definición de variables de color para reutilizar
    PRIMARY_PURPLE = "#6d28d9"
    BORDER_COLOR_DARK = "rgba(51, 65, 85, 0.5)"
    BORDER_COLOR_LIGHT = "rgba(203, 213, 225, 0.8)"

    st.markdown(f"""
        <style>
            /* --- 1. CONFIGURACIÓN DINÁMICA POR TEMA --- */

            /* Estilos cuando el usuario elige MODO OSCURO */
            [data-theme="dark"] .stApp {{
                background-color: #0e1117;
                color: #ffffff;
            }}
            [data-theme="dark"] [data-testid="stSidebar"] {{
                background-color: #1e293b !important;
                border-right: 1px solid {BORDER_COLOR_DARK} !important;
            }}
            [data-theme="dark"] [data-testid="stSidebar"] .stMarkdown p {{
                color: #cbd5e1 !important;
            }}

            /* Estilos cuando el usuario elige MODO CLARO (Elegante y cómodo) */
            [data-theme="light"] .stApp {{
                background-color: #f8fafc !important; /* Gris azulado muy suave */
                color: #0f172a !important; /* Texto azul oscuro profundo */
            }}
            [data-theme="light"] [data-testid="stSidebar"] {{
                background-color: #ffffff !important;
                border-right: 1px solid {BORDER_COLOR_LIGHT} !important;
            }}
            [data-theme="light"] [data-testid="stSidebar"] .stMarkdown p,
            [data-theme="light"] [data-testid="stSidebar"] label {{
                color: #334155 !important;
                font-weight: 600 !important;
            }}

            /* --- 2. COMPONENTES COMUNES (ADAPTATIVOS) --- */

            /* Botones con estilo moderno */
            .stButton>button {{
                border-radius: 8px !important;
                transition: all 0.3s ease;
                font-weight: 600 !important;
            }}

            /* Tarjetas de Métricas (Usamos transparencias para que se adapten) */
            .metric-card {{
                background-color: rgba(30, 41, 59, 0.1); 
                padding: 15px; 
                border-radius: 10px;
                border: 1px solid {PRIMARY_PURPLE}44;
                text-align: center; 
                margin-bottom: 10px;
            }}
            
            [data-theme="dark"] .metric-value {{ color: #ffffff; }}
            [data-theme="light"] .metric-value {{ color: #1e293b; }}

            /* Cuadro de Información (Infraestructura/SSL) */
            .info-box {{
                background-color: rgba(30, 41, 59, 0.05); 
                padding: 20px; 
                border-radius: 10px;
                border: 1px solid rgba(109, 40, 217, 0.2); 
                height: 100%;
                color: inherit;
            }}

            /* Estilo de las pestañas (Tabs) */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 8px;
            }}
            .stTabs [data-baseweb="tab"] {{
                background-color: rgba(30, 41, 59, 0.05);
                border-radius: 5px 5px 0px 0px;
                padding: 8px 16px;
                border: 1px solid rgba(109, 40, 217, 0.1);
            }}
            
            /* Pestaña seleccionada */
            .stTabs [aria-selected="true"] {{
                background-color: {PRIMARY_PURPLE}22 !important;
                border-bottom: 2px solid {PRIMARY_PURPLE} !important;
            }}

            /* --- 3. INPUTS Y FORMULARIOS --- */
            [data-theme="light"] .stTextInput input {{
                background-color: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
            }}
        </style>
    """, unsafe_allow_html=True)
