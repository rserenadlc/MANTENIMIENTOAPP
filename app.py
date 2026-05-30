import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Portal de Mantenimiento | Scuderia", 
    page_icon="🏎️", 
    layout="centered"
)

# --- BASE DE DATOS EN MEMORIA (CON TUS 10 PRIMEROS EQUIPOS REALES) ---
if "equipos_reales" not in st.session_state:
    st.session_state.equipos_reales = [
        {"eco": "A-TC-K-02", "marca": "KENWORTH", "modelo": "T600/T600 B/T660", "ano": 2009, "status": "activo"},
        {"eco": "A-TC-K-35", "marca": "KENWORTH", "modelo": "t680", "ano": 2024, "status": "activo"},
        {"eco": "A-TC-M-32", "marca": "MACK", "modelo": "anthem 48", "ano": 2024, "status": "activo"},
        {"eco": "TC-17", "marca": "KENWORTH", "modelo": "T800", "ano": 2012, "status": "activo"},
        {"eco": "A-TC-K-14", "marca": "KENWORTH", "modelo": "T800 B", "ano": 2012, "status": "activo"},
        {"eco": "A-TC-K-12", "marca": "KENWORTH", "modelo": "T800 B", "ano": 2011, "status": "activo"},
        {"eco": "A-TC-K-11", "marca": "KENWORTH", "modelo": "T800 B", "ano": 2011, "status": "activo"},
        {"eco": "A-TC-K-13", "marca": "KENWORTH", "modelo": "T800 B", "ano": 2011, "status": "activo"},
        {"eco": "A-TC-K-15", "marca": "KENWORTH", "modelo": "t 800 b", "ano": 2023, "status": "PENDIENTE"},
        {"eco": "a-tc-k-40", "marca": "KENWORTH", "modelo": "t680", "ano": 2025, "status": "activo"},
    ]

if "mantenimientos" not in st.session_state:
    st.session_state.mantenimientos = [
        {"id": 1, "cliente": "INDHECA / CARECO", "equipo": "KENWORTH T680 (Eco: A-TC-K-35)", "estado": "Pendiente", "tecnico": "Ninguno"},
        {"id": 2, "cliente": "INDHECA / CARECO", "equipo": "MACK anthem 48 (Eco: A-TC-M-32)", "estado": "Completado", "tecnico": "Carlos Gómez"},
    ]

# --- ENCABEZADO ---
st.title("🏎️ Portal de Servicios")

rol = st.selectbox("Selecciona tu perfil para la demo:", ["Cliente", "Técnico", "Administrador"])

st.divider()

# ================= ROL: CLIENTE =================
if rol == "Cliente":
    st.header("Bienvenido, Cliente (INDHECA / CARECO)")
    
    tab1, tab2 = st.tabs(["Mis Equipos y Solicitar", "Historial de Mantenimientos"])
    
    with tab1:
        st.subheader("Mis Equipos Activos (Primeros 10 del Control)")
        
        # Mostramos los 10 equipos reales en una tabla estética dentro del contenedor
        with st.container(border=True):
            st.markdown("### 📋 Flota de Maquinaria Disponible")
            # Convertimos la lista de equipos en una tabla visual limpia
            st.dataframe(st.session_state.equipos_reales, use_container_width=True, hide_index=True)
        
        st.subheader("Solicitar Nuevo Mantenimiento")
        
        # El selector ahora se llena dinámicamente con los números económicos reales del Excel
        lista_opciones_equipos = [f"{e['marca']} {e['modelo']} (Eco: {e['eco']})" for e in st.session_state.equipos_reales]
        equipo_sel = st.selectbox("Selecciona el equipo que requiere servicio:", lista_opciones_equipos)
        
        detalles = st.text_area("Describe la falla, kilometraje o tipo de servicio requerido:")
        
        if st.button("Enviar Solicitud", type="primary"):
            st.session_state.mantenimientos.append({
                "id": len(st.session_state.mantenimientos) + 1,
                "cliente": "INDHECA / CARECO",
                "equipo": equipo_sel,
                "estado": "Pendiente",
                "tecnico": "Ninguno"
            })
            st.success(f"¡Solicitud para el equipo {equipo_sel} enviada con éxito!")

    with tab2:
        st.subheader("Estado de mis Servicios")
        for m in st.session_state.mantenimientos:
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
            paso1 = st.checkbox("1. Inspección visual general y Check-list de fluidos inicial.")
            paso2 = st.checkbox("2. Limpieza o cambio de filtros según bitácora de la maquinaria.")
            paso3 = st.checkbox("3. Pruebas de presión del sistema y arranque de control.")
            
            if paso1 and paso2 and paso3:
                if st.button
