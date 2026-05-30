import streamlit as st

# Configuración de la página para móvil
st.set_page_config(page_title="Portal de Mantenimiento", page_icon="🛠️", layout="centered")

# --- SIMULACIÓN DE BASE DE DATOS EN MEMORIA ---
if "mantenimientos" not in st.session_state:
    st.session_state.mantenimientos = [
        {"id": 1, "cliente": "Empresa Alfa", "equipo": "Compresor CAT v4", "estado": "Pendiente", "tecnico": "Ninguno"},
        {"id": 2, "cliente": "Empresa Alfa", "equipo": "Generador Cummins 150kVA", "estado": "Completado", "tecnico": "Carlos Gómez"},
    ]

# --- INTERFAZ DE SELECCIÓN DE ROL ---
st.title("🛠️ Portal de Servicios")
rol = st.selectbox("Selecciona tu perfil para la demo:", ["Cliente", "Técnico", "Administrador"])

st.markdown("---")

# ================= ROL: CLIENTE =================
if rol == "Cliente":
    st.header("Bienvenido, Cliente (Empresa Alfa)")
    
    tab1, tab2 = st.tabs(["Mis Equipos y Solicitar", "Historial de Mantenimientos"])
    
    with tab1:
        st.subheader("Mis Equipos Activos")
        st.info("• Compresor CAT v4 (ID: 045)\n\n• Generador Cummins 150kVA (ID: 102)")
        
        st.subheader("Solicitar Nuevo Mantenimiento")
        equipo_sel = st.selectbox("Selecciona el equipo:", ["Compresor CAT v4", "Generador Cummins 150kVA"])
        detalles = st.text_area("Describe la falla o tipo de servicio:")
        
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
            st.warning(f"Trabajando en: {m_seleccionado['equipo']} para {m_seleccionado['cliente']}")
            
            st.subheader("📋 Lista de pasos obligatorios:")
            paso1 = st.checkbox("1. Inspección visual y Check-list inicial.")
            paso2 = st.checkbox("2. Limpieza de filtros y verificación de fluidos.")
            paso3 = st.checkbox("3. Pruebas de presión y arranque de control.")
            
            # Botón para finalizar (solo se activa si cumple los pasos)
            if paso1 and paso2 and paso3:
                if st.button("Marcar como Completado ✅", type="primary"):
                    for m in st.session_state.mantenimientos:
                        if m["id"] == m_seleccionado["id"]:
                            m["estado"] = "Completado"
                            m["tecnico"] = "Carlos Gómez"
                    st.success("¡Mantenimiento registrado e historial actualizado!")
                    st.rerun()
            else:
                st.info("Por favor, marca todos los pasos para poder finalizar la orden.")

# ================= ROL: ADMINISTRADOR =================
elif rol == "Administrador":
    st.header("Panel de Administración")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Clientes")
        st.write("- Empresa Alfa\n- Industrias Beta\n- Constructora Delta")
        
    with col2:
        st.subheader("🔧 Técnicos Activos")
        st.write("- Carlos Gómez (En ruta)\n- Juan Pérez (Disponible)")
        
    st.subheader("📊 Monitoreo Global de Servicios")
    st.table(st.session_state.mantenimientos)