import streamlit as st

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Portal de Mantenimiento | Scuderia", 
    page_icon="🏎️", 
    layout="centered"
)

# --- BASE DE DATOS EN MEMORIA (10 EQUIPOS REALES DEL EXCEL) ---
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

# --- TABLA DE SEGUIMIENTO SIMULADA (MÉTRICAS DE KILOMETRAJE Y MOTOR) ---
if "seguimiento_kilometraje" not in st.session_state:
    st.session_state.seguimiento_kilometraje = [
        {"Económico": "A-TC-K-02", "KM Actual": "320,500 km", "Último Servicio": "310,000 km", "Sig. Servicio": "325,000 km", "Estatus": "OK", "Condición": "En Rango"},
        {"Económico": "A-TC-K-35", "KM Actual": "45,200 km", "Último Servicio": "30,000 km", "Sig. Servicio": "45,000 km", "Estatus": "⚠️ REVISIÓN", "Condición": "⚠️ KILOMETRAJE CUMPLIDO"},
        {"Económico": "A-TC-M-32", "KM Actual": "12,800 km", "Último Servicio": "0 km", "Sig. Servicio": "15,000 km", "Estatus": "OK", "Condición": "En Rango"},
        {"Económico": "TC-17", "KM Actual": "512,100 km", "Último Servicio": "500,000 km", "Sig. Servicio": "510,000 km", "Estatus": "🚨 ALERTA", "Condición": "🚨 EXCEDIDO"},
        {"Económico": "A-TC-K-14", "KM Actual": "189,400 km", "Último Servicio": "180,000 km", "Sig. Servicio": "195,000 km", "Estatus": "OK", "Condición": "En Rango"},
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
    
    # Separación exacta en las 3 pestañas solicitadas
    tab1, tab2, tab3 = st.tabs(["📋 Mis Equipos Activos", "📊 Seguimiento de Servicios", "⏳ Historial de Mantenimientos"])
    
    with tab1:
        st.subheader("Flota de Maquinaria Disponible")
        with st.container(border=True):
            st.dataframe(st.session_state.equipos_reales, use_container_width=True, hide_index=True)
        
    with tab2:
        st.subheader("Monitoreo Dinámico de Desgaste y Kilometraje")
        st.caption("Esta tabla identifica automáticamente qué equipos requieren mantenimiento preventivo basándose en sus alertas de kilometraje.")
        
        # Tabla de control de kilometraje simulada
        with st.container(border=True):
            st.dataframe(st.session_state.seguimiento_kilometraje, use_container_width=True, hide_index=True)
            
        st.markdown("---")
        
        # Recuadro inferior exclusivo para solicitar el mantenimiento
        with st.container(border=True):
            st.subheader("🛠️ Solicitar Mantenimiento Preventivo / Correctivo")
            st.info("Utilice este apartado prioritariamente para las unidades marcadas con estatus de ⚠️ REVISIÓN o 🚨 ALERTA por kilometraje de servicio cumplido.")
            
            lista_opciones_equipos = [f"{e['marca']} {e['modelo']} (Eco: {e['eco']})" for e in st.session_state.equipos_reales]
            equipo_sel = st.selectbox("Seleccione la unidad que ingresará a taller:", lista_opciones_equipos)
            
            col_km, col_tipo = st.columns(2)
            with col_km:
                km_reportado = st.text_input("Kilometraje actual de la unidad:", placeholder="Ej. 45,200 km")
            with col_tipo:
                tipo_maint = st.selectbox("Tipo de Servicio:", ["Preventivo (Cambio de filtros/fluidos)", "Correctivo (Falla reportada)", "Inspección General"])
                
            detalles = st.text_area("Observaciones o síntomas reportados por el operador:")
            
            if st.button("Enviar Orden de Servicio", type="primary"):
                st.session_state.mantenimientos.append({
                    "id": len(st.session_state.mantenimientos) + 1,
                    "cliente": "INDHECA / CARECO",
                    "equipo": equipo_sel,
                    "estado": "Pendiente",
                    "tecnico": "Ninguno"
                })
                st.success(f"¡Solicitud de servicio creada con éxito para la unidad {equipo_sel}! El departamento técnico ha sido notificado.")

    with tab3:
        st.subheader("Historial General y Estatus de Órdenes")
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
                if st.button("Marcar como Completado ✅", type="primary"):
                    for m in st.session_state.mantenimientos:
                        if m["id"] == m_seleccionado["id"]:
                            m["estado"] = "Completado"
                            m["tecnico"] = "Carlos Gómez"
                    st.success("¡Mantenimiento registrado con éxito en el historial!")
                    st.rerun()
            else:
                st.info("Por favor, marca todos los pasos obligatorios para poder finalizar la orden de servicio.")

# ================= ROL: ADMINISTRADOR =================
elif rol == "Administrador":
    st.header("Panel de Administración")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 👥 Clientes Activos")
            st.write("• CARECO\n\n• INDHECA")
        
    with col2:
        with st.container(border=True):