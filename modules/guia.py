import streamlit as st
import plotly.express as px
import pandas as pd
from modules.security_core import SecurityCore  # Importación del escudo de seguridad

def render_guia():
    st.title("🛡️ Guía de Seguridad Web")
    st.markdown("---")

    # 1. GRÁFICO DE PRIORIDADES
    st.subheader("📊 Matriz de Prioridades de Seguridad")
    
    # Sanitizamos los nombres de las categorías del gráfico por precaución
    categorias = ['Criptografía PQC','Zero Trust','Seguridad API','Privacidad de Datos','Resiliencia Ops']
    safe_categorias = [SecurityCore.sanitize_output(cat) for cat in categorias]

    df_radar = pd.DataFrame(dict(
        r=[95, 90, 85, 90, 80],
        theta=safe_categorias
    ))
    
    fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0,100])
    
    fig.update_traces(
        fill='toself', 
        line_color='#e59a94', 
        fillcolor='rgba(229, 154, 148, 0.3)'
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#cbd5e1", size=14),
        polar=dict(
            bgcolor='rgba(30, 33, 48, 0.5)',
            angularaxis=dict(linewidth=1, showline=True, linecolor='#475569'),
            radialaxis=dict(
                showline=True,
                gridcolor='#475569', 
                linecolor='#475569',
                tickfont=dict(color="#ffffff", size=10), 
                ticksuffix='%',
                angle=45,
                gridwidth=1
            )
        ),
        margin=dict(t=30, b=30, l=30, r=30)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # 2. GUÍA COMPLETA (Categorizada con Expanders)
    col1, col2 = st.columns(2)

    with col1:
        with st.expander("🔐 Capa de Transporte y Criptografía", expanded=True):
            st.markdown("""
            * **TLS 1.3:** Única versión aceptable. Deshabilitar TLS 1.0, 1.1 y 1.2.
            * **HSTS:** Implementar con `includeSubDomains` y `preload`.
            * **Algoritmos Cuánticos:** Transición a esquemas híbridos (ej. Kyber).
            """)
        
        with st.expander("🛡️ Protección contra Ataques Comunes"):
            st.markdown("""
            * **WAF Avanzado:** Bloqueo automático de IPs sospechosas y patrones SQLi.
            * **CSP:** Política de seguridad de contenido estricta para mitigar XSS.
            * **Rate Limiting:** Control de ráfagas para evitar denegación de servicio.
            """)

    with col2:
        with st.expander("👥 Gestión de Identidad (Zero Trust)", expanded=True):
            st.markdown("""
            * **MFA Obligatorio:** Basado en FIDO2 o aplicaciones autenticadoras.
            * **RBAC:** Control de acceso basado en roles con el privilegio mínimo.
            * **Sesiones Inmunes:** Rotación de tokens de sesión y cookies seguras.
            """)

        with st.expander("🔍 Auditoría y Cabeceras"):
            st.markdown("""
            * **Referrer-Policy:** Evitar la fuga de información sensible en URLs.
            * **Permissions-Policy:** Restricción estricta de hardware (Cámara/Mic).
            * **Logs Forenses:** Auditoría detallada de acciones administrativas.
            """)

    st.divider()

    # 3. RECOMENDACIONES DE IMPLEMENTACIÓN
    st.subheader("🚀 Recomendaciones de Implementación")
    
    rec_1, rec_2, rec_3 = st.columns(3)
    
    with rec_1:
        st.info("### 📋 Higiene Operativa")
        st.markdown("""
        **Monitoreo y Logs:**
        * **Centralización de Eventos:** Implementar un stack **ELK** o **Grafana Loki**.
        * **Alertas de Umbral:** Avisos inmediatos ante errores `401 Unauthorized`.
        
        **Mantenimiento:**
        * **SCA:** Escaneo automatizado de vulnerabilidades en dependencias.
        * **Hardening:** Forzar autenticación SSH mediante llaves seguras.
        """)

    with rec_2:
        st.success("### 🏗️ Arquitectura Segura")
        st.markdown("""
        **Infraestructura:**
        * **Micro-segmentación:** Bases de datos en subredes privadas aisladas.
        * **Contenedores Inmutables:** Docker en modo 'Read-Only'.
        
        **Defensa Proactiva:**
        * **Secret Management:** Uso de **HashiCorp Vault**.
        * **API Gateway:** Validación de tokens JWT y rate-limiting.
        """)

    with rec_3:
        st.warning("### 💾 Datos y Privacidad")
        st.markdown("""
        **Resiliencia:**
        * **Cifrado AES-256:** Cifrado en reposo para volúmenes de datos.
        * **Estrategia Backup 3-2-1:** Copias diversificadas y fuera de línea.
        
        **Privacidad Legal:**
        * **Anonimización:** Masking de datos en entornos de desarrollo.
        * **Eliminación Segura:** Flujos para cumplir con el derecho al olvido.
        """)

    st.divider()
    
    # Nota final de cierre (Sanitizamos el texto de la nota por seguridad estructural)
    footer_text = "La seguridad es 100% visibilidad. La arquitectura Zero Trust no se trata de no confiar en nadie, sino de verificarlo todo de forma continua y automática."
    safe_footer = SecurityCore.sanitize_output(footer_text)

    st.markdown(f"""
    <div style="background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #f7d08a;">
        <strong>Nota del Experto:</strong> {safe_footer}
    </div>
    """, unsafe_allow_html=True)
