import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Portal de Mantenimiento | Scuderia", 
    page_icon="🏎️", 
    layout="centered"
)

# --- SIMULACIÓN DE BASE DE DATOS EN MEMORIA ---
if "mantenimientos" not in st.session_state:
    st.session_state.mantenimientos = [
        {"id": 1, "cliente": "Empresa Alfa", "equipo": "Compresor CAT v4", "estado": "Pendiente", "tecnico": "Ninguno"},
        {"id": 2, "cliente": "Empresa Alfa", "equipo": "Generador Cummins 150kVA", "estado": "Completado", "tecnico": "Carlos Gómez"},
    ]

# --- ENCABEZADO ---
st.title("🏎️ Portal de Servicios")

rol = st.selectbox("Selecciona tu perfil para la demo:", ["Cliente", "Técnico", "Administrador"])

st.divider()

# ================= ROL: CLIENTE =================
if rol == "Cliente":
    st.header("Bienvenido, Cliente (Empresa Alfa)")
    
    tab1, tab2 = st.tabs(["Mis Equipos y Solicitar", "Historial de Mantenimientos"])
    
    with tab1:
        st.subheader("Mis Equipos Activos")
        
        # Usamos contenedores nativos expandibles o cajas de información
        with st.container(border=True):
            st.markdown("### 📋 Equipos en Operación")
            st.write("• **Compresor CAT v4** (ID: 045)")
            st.write("• **Generador Cummins 150kVA** (ID: 102)")
        
        st.subheader("Solicitar Nuevo Mantenimiento")
        equipo_sel = st.selectbox("Selecciona el equipo:", ["Compresor CAT v4", "Generador Cummins 150kVA"])
        detalles = st.text_area("Describe la falla o tipo de servicio:")
        
        # type="primary" usará el color de acento configurado (Rojo)
        if st.button("Enviar Solicitud", type="primary"):
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
            with st.container(border=True):
                st.markdown("### ⚠️ Orden Activa")
                st.write(f"Trabajando en: **{m_seleccionado['equipo']}**")
                st.write(f"Cliente: **{m_seleccionado['cliente']}**")
            
            st.subheader("📋 Lista de pasos obligatorios:")
            paso1 = st.checkbox("1. Inspección visual y Check-list inicial.")
            paso2 = st.checkbox("2. Limpieza de filtros y verificación de fluidos.")
            paso3 = st.checkbox("3. Pruebas de presión y arranque de control.")
            
            if paso1 and paso2 and paso3:
                if st.button("Marcar como Completado ✅", type="primary"):
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
        with st.container(border=True):
            st.markdown("### 👥 Clientes")
            st.write("• Empresa Alfa\n\n• Industrias Beta\n\n• Constructora Delta")
        
    with col2:
        with st.container(border=True):
            st.markdown("### 🔧 Técnicos Activos")
            st.write("• Carlos Gómez (En ruta)\n\n• Juan Pérez (Disponible)")
        
    st.subheader("📊 Monitoreo Global de Servicios")
    st.dataframe(st.session_state.mantenimientos, use_container_width=True)
