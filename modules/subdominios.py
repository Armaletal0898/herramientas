import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def render_subdominios(results):
    st.title("🔗 Inteligencia de Subdominios")
    
    if results and results.get("subs"):
        subdominios = results["subs"]
        target = results["target"]

        st.subheader("🌐 Visualización de Superficie de Ataque")
        
        # Configuración de posiciones
        n_subs = len(subdominios)
        x_nodes = [0] 
        y_nodes = [0]
        text_nodes = [f"<b>CENTRO: {target}</b>"]
        color_nodes = ['#7c3aed'] # Morado para el centro
        size_nodes = [40]

        # Generar posiciones circulares
        angles = np.linspace(0, 2*np.pi, n_subs, endpoint=False)
        distancia = 1.5 

        for i, sub in enumerate(subdominios):
            x_nodes.append(distancia * np.cos(angles[i]))
            y_nodes.append(distancia * np.sin(angles[i]))
            text_nodes.append(f"Sub: {sub}")
            color_nodes.append('#4b5563') 
            size_nodes.append(20)

        # Crear líneas de conexión
        edge_x = []
        edge_y = []
        for i in range(1, len(x_nodes)):
            edge_x.extend([0, x_nodes[i], None])
            edge_y.extend([0, y_nodes[i], None])

        fig = go.Figure()

        # Líneas (Aristas)
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#334155'),
            hoverinfo='none',
            mode='lines'
        ))

        # Nodos (Puntos) - AQUÍ SE CORRIGIÓ EL ERROR
        fig.add_trace(go.Scatter(
            x=x_nodes, y=y_nodes,
            mode='markers+text',
            text=text_nodes,
            textposition="top center",
            hoverinfo='text',
            marker=dict(
                size=size_nodes,
                color=color_nodes,
                line=dict(width=2, color='#7c3aed'), # Borde morado para resaltar
                # Se eliminó la propiedad 'shadow' que causaba el error
                gradient=dict(type="radial", color="#ffffff") # Efecto de brillo alternativo
            )
        ))

        fig.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=50, l=50, r=50),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- TABLA Y MÉTRICAS ---
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📋 Listado de Activos")
            df = pd.DataFrame(subdominios, columns=["Dirección del Subdominio"])
            st.dataframe(df, use_container_width=True, height=300)

        with col2:
            st.markdown("### 📈 Resumen")
            st.markdown(f"""
            <div style="background-color: #1e2130; padding: 20px; border-radius: 10px; border: 1px solid #334155;">
                <p style="margin:0; color:#aaa;">Total Encontrados</p>
                <h2 style="margin:0; color:#7c3aed;">{n_subs}</h2>
                <hr style="opacity:0.2;">
                <p style="margin:0; color:#aaa;">Riesgo de Exposición</p>
                <h3 style="margin:0; color:#e59a94;">{'ALTO' if n_subs > 5 else 'BAJO'}</h3>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("👋 Inicia un escaneo en el panel lateral para visualizar la red de subdominios.")
