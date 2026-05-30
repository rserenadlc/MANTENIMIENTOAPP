import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA Y TEMA ESTILO FERRARI ---
st.set_page_config(
    page_title="Portal de Mantenimiento | Scuderia", 
    page_icon="🏎️", 
    layout="centered"
)

# Inyección de CSS personalizado para lograr el look exacto de Ferrari
st.markdown("""
    <style>
    /* Fondo de la aplicación en blanco */
    .stApp {
        background-color: #FFFFFF;
        color: #111111;
    }
    
    /* Títulos principales en negro Ferrari */
    h1, h2, h3, p, span {
        color: #111111 !important;
    }
    
    /* Paneles o contenedores simulados con fondo negro y texto blanco */
    .ferrari-card {
        background-color: #111111;
        padding: 20px;
        border-radius: 8px;
        color: #FFFFFF !important;
        margin-bottom: 15px;
    }
    .ferrari-card p, .ferrari-card h3, .ferrari-card li {
        color: #FFFFFF !important;
    }
    
    /* Botón Primario: Rojo Ferrari con letras blancas */
    div.stButton > button:first-child {
        background-color: #E81C23 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        transition: background-color 0.3s ease;
    }
    
    /* Efecto al pasar el mouse sobre el botón */
    div.stButton > button:first-child:hover {
        background-color: #B81419 !important;
        color: #FFFFFF !important;
    }
    
    /* Ajustes para los Tabs (pestañas) */
    button[data-baseweb="tab"] {
        color: #111111 !important;
    }
    button[aria-selected="true"] {
        color: #E81C23 !important;
        border-bottom-color: #E81C23 !important;
    }
    </style>
""", unsafe_html=True)


# --- SIMULACIÓN DE BASE DE DATOS EN MEMORIA ---
if "mantenimientos" not in st.session_state:
    st.session_state.mantenimientos = [
        {"id": 1, "cliente": "Empresa Alfa", "equipo": "Compresor CAT v4", "estado": "Pendiente", "tecnico": "Ninguno"},
        {"id": 2, "cliente": "Empresa Alfa", "equipo": "Generador Cummins 150kVA", "estado": "Completado", "tecnico": "Carlos Gómez"},
    ]

# --- ENCABEZADO CON IMAGEN/ICONO ---
# Nota: Puedes cambiar este emoji grande por una URL de imagen real usando st.image("URL") si lo deseas.
st.markdown("<h1 style='text-align: center; color: #E81C23 !important;'>🏎️ Portal de Servicios</h1>", unsafe_html=True)

rol = st.selectbox("Selecciona tu perfil para la demo:", ["Cliente", "Técnico", "Administrador"])

st.markdown("<hr style='border-top: 2px solid #E81C23;'>", unsafe_html=True)

# ================= ROL: CLIENTE =================
if rol == "Cliente":
    st.header("Bienvenido, Cliente (Empresa Alfa)")
    
    tab1, tab2 = st.tabs(["Mis Equipos y Solicitar", "Historial de Mantenimientos"])
    
    with tab1:
        st.subheader("Mis Equipos Activos")
        
        # Usamos el contenedor negro "estilo Ferrari" para los equipos
        st.markdown("""
        <div class="ferrari-card">
            <h3>Equipos en Operación</h3>
            <ul>
                <li><strong>Compresor CAT v4</strong> (ID: 045)</li>
                <li><strong>Generador Cummins 150kVA</strong> (ID: 102)</li>
            </ul>
        </div>
        """, unsafe_html=True)
        
        st.subheader("Solicitar Nuevo Mantenimiento")
        equipo_sel = st.selectbox("Selecciona el equipo:", ["Compresor CAT v4", "Generador Cummins 150kVA"])
        detalles = st.text_area("Describe la falla o tipo de servicio:")
        
        if st.button("Enviar Solicitud"):
            st.session_state.mantenimientos.append({
                "id": len(st.session_state.mantenimientos) + 1,
                "cliente": "Empresa Alfa",
                "equipo": equipo_sel,
                "estado": "Pendiente",
                "tecnico": "Ninguno"
            })
            st.success("¡Solicitud enviada con éxito!")

    with tab2:
        st.subheader("Estado de mis Servicios")
        for m in st.session_state.mantenimientos:
            if m["cliente"] == "Empresa Alfa":
                status_color = "🔴" if m["estado"] == "Pendiente" else "🟢"
                st.write(f"{status_color} **{m['equipo']}** - Estado: *{m['estado']}* (Técnico: {m['tecnico']})")

# ================= ROL: TÉCNICO =================
elif rol == "Técnico":
    st.header("Panel del Técnico: Carlos Gómez")
    
    pendientes = [m for m in st.session_state.mantenimientos if m["estado"] == "Pendiente"]
    
    if not pendientes:
        st.success("¡No tienes mantenimientos pendientes por hoy!")
    else:
        st.subheader("Órdenes Disponibles")
        m_seleccionado = st.selectbox(
            "Selecciona una orden para trabajar:", 
            options=pendientes, 
            format_func=lambda x: f"ID {x['id']} - {x['cliente']} ({x['equipo']})"
        )
        
        if m_seleccionado:
            # Alerta visual usando el panel negro
            st.markdown(f"""
            <div class="ferrari-card" style="border-left: 5px solid #E81C23;">
                <h3>⚠️ Orden Activa</h3>
                <p>Trabajando en: <strong>{m_seleccionado['equipo']}</strong> para el cliente <strong>{m_seleccionado['cliente']}</strong></p>
            </div>
            """, unsafe_html=True)
            
            st.subheader("📋 Lista de pasos obligatorios:")
            paso1 = st.checkbox("1. Inspección visual y Check-list inicial.")
            paso2 = st.checkbox("2. Limpieza de filtros y verificación de fluidos.")
            paso3 = st.checkbox("3. Pruebas de presión y arranque de control.")
            
            if paso1 and paso2 and paso3:
                if st.button("Marcar como Completado ✅"):
                    for m in st.session_state.mantenimientos:
                        if m["id"] == m_seleccionado["id"]:
                            m["estado"] = "Completado"
                            m["tecnico"] = "Carlos Gómez"
                    st.success("¡Mantenimiento registrado con éxito!")
                    st.rerun()
            else:
                st.info("Por favor, marca todos los pasos para poder finalizar la orden.")

# ================= ROL: ADMINISTRADOR =================
elif rol == "Administrador":
    st.header("Panel de Administración")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="ferrari-card">
            <h3>👥 Clientes</h3>
            <p>• Empresa Alfa<br>• Industrias Beta<br>• Constructora Delta</p>
        </div>
        """, unsafe_html=True)
        
    with col2:
        st.markdown("""
        <div class="ferrari-card">
            <h3>🔧 Técnicos Activos</h3>
            <p>• Carlos Gómez (En ruta)<br>• Juan Pérez (Disponible)</p>
        </div>
        """, unsafe_html=True)
        
    st.subheader("📊 Monitoreo Global de Servicios")
    st.dataframe(st.session_state.mantenimientos, use_container_width=True)