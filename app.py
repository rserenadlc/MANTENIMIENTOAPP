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

# --- TABLA DE SEGUIMIENTO SIMULADA ---
if "seguimiento_kilometraje" not in st.session_state:
    st.session_state.seguimiento_kilometraje = [
        {"Económico": "A-TC-K-02", "KM Actual": "320,500 km", "Último Servicio": "310,000 km", "Sig. Servicio": "325,000 km", "Estatus": "OK", "Condición": "En Rango"},
        {"Económico": "A-TC-K-35", "KM Actual": "45,200 km", "Último Servicio": "30,000 km", "Sig. Servicio": "45,000 km", "Estatus": "⚠️ REVISIÓN", "Condición": "⚠️ KILOMETRAJE CUMPLIDO"},
        {"Económico": "A-TC-M-32", "KM Actual": "12,800 km", "Último Servicio": "0 km", "Sig. Servicio": "15,000 km", "Estatus": "OK", "Condición": "En Rango"},
        {"Económico": "TC-17", "KM Actual": "512,100 km", "Último Servicio": "500,000 km", "Sig. Servicio": "510,000 km", "Estatus": "🚨 ALERTA", "Condición": "🚨 EXCEDIDO"},
        {"Económico": "A-TC-K-14", "KM Actual": "189,400 km", "Último Servicio": "180,000 km", "Sig. Servicio": "195,000 km", "Estatus": "OK", "Condición": "En Rango"},
    ]

# --- HISTORIAL COMPLETO CON FECHAS Y DESCRIPCIONES ---
if "mantenimientos" not in st.session_state:
    st.session_state.mantenimientos = [
        {
            "id": 1, 
            "cliente": "INDHECA / CARECO", 
            "equipo": "KENWORTH T680 (Eco: A-TC-K-35)", 
            "estado": "Pendiente", 
            "tecnico": "Ninguno",
            "descripcion": "Servicio preventivo por cumplimiento de kilometraje (45,000 km). Cambio de aceite de motor, filtro de aceite y filtro de combustible.",
            "fecha_prog": "01/06/2026",
            "fecha_fin": "-"
        },
        {
            "id": 2, 
            "cliente": "INDHECA / CARECO", 
            "equipo": "MACK anthem 48 (Eco: A-TC-M-32)", 
            "estado": "Completado", 
            "tecnico": "Carlos Gómez",
            "descripcion": "Inspección inicial de asentamiento y revisión de niveles de fluidos hidráulicos. Todo en orden.",
            "fecha_prog": "20/05/2026",
            "fecha_fin": "22/05/2026"
        },
    ]

# --- ENCABEZADO ---
st.title("🏎️ Portal de Servicios")

rol = st.selectbox("Selecciona tu perfil para la demo:", ["Cliente", "Técnico", "Administrador"])

st.divider()

# ================= ROL: CLIENTE =================
if rol == "Cliente":
    st.header("Bienvenido, Cliente (INDHECA / CARECO)")
    
    tab1, tab2, tab3 = st.tabs(["📋 Mis Equipos Activos", "📊 Seguimiento de Servicios", "⏳ Historial de Mantenimientos"])
    
    with tab1:
        st.subheader("Flota de Maquinaria Disponible")
        with st.container(border=True):
            st.dataframe(st.session_state.equipos_reales, use_container_width=True, hide_index=True)
        
    with tab2:
        st.subheader("Monitoreo Dinámico de Desgaste y Kilometraje")
        with st.container(border=True):
            st.dataframe(st.session_state.seguimiento_kilometraje, use_container_width=True, hide_index=True)
            
        st.markdown("---")
        
        with st.container(border=True):
            st.subheader("🛠️ Solicitar Mantenimiento Preventivo / Correctivo")
            
            lista_opciones_equipos = [f"{e['marca']} {e['modelo']} (Eco: {e['eco']})" for e in st.session_state.equipos_reales]
            equipo_sel = st.selectbox("Seleccione la unidad que ingresará a taller:", lista_opciones_equipos)
            
            col_km, col_tipo = st.columns(2)
            with col_km:
                km_reportado = st.text_input("Kilometraje actual de la unidad:", placeholder="Ej. 45,200 km")
            with col_tipo:
                tipo_maint = st.selectbox("Tipo de Servicio:", ["Preventivo (Cambio de filtros/fluidos)", "Correctivo (Falla reportada)", "Inspección General"])
                
            detalles = st.text_area("Observaciones o síntomas reportados por el operador:")
            
            if st.button("Enviar Orden de Servicio", type="primary"):
                # Insertamos la fecha de hoy simulada para la programación
                st.session_state.mantenimientos.append({
                    "id": len(st.session_state.mantenimientos) + 1,
                    "cliente": "INDHECA / CARECO",
                    "equipo": equipo_sel,
                    "estado": "Pendiente",
                    "tecnico": "Ninguno",
                    "descripcion": f"[{tipo_maint}] Km reportado: {km_reportado}. Observaciones: {detalles}",
                    "fecha_prog": "30/05/2026", # Fecha actual simulada
                    "fecha_fin": "-"
                })
                st.success(f"¡Solicitud de servicio creada con éxito!")

    with tab3:
        st.subheader("Historial y Estatus Detallado de Órdenes")
        
        # Desplegamos cada mantenimiento de forma estética en su propia tarjeta
        for m in st.session_state.mantenimientos:
            with st.container(border=True):
                col_info, col_status = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"### 🚛 {m['equipo']}")
                    st.markdown(f"**Descripción:** {m['descripcion']}")
                    st.markdown(f"👤 **Técnico Asignado:** {m['tecnico']}")
                    
                    # Lógica de fechas según el estado
                    if m["estado"] == "Completado":
                        st.markdown(f"📅 **Fecha de Finalización:** {m['fecha_fin']}")
                    else:
                        st.markdown(f"📅 **Fecha Programada:** {m['fecha_prog']}")
                
                with col_status:
                    st.write("") # Espaciador visual
                    if m["estado"] == "Pendiente":
                        st.error("🔴 PENDIENTE")
                    else:
                        st.success("🟢 COMPLETADO")

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
                st.write(f"Descripción inicial: *{m_seleccionado['descripcion']}*")
            
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
                            m["fecha_fin"] = "30/05/2026" # Sella la fecha de hoy al finalizar
                    st.success("¡Mantenimiento registrado con éxito!")
                    st.rerun()
            else:
                st.info("Por favor, marca todos los pasos obligatorios para poder finalizar la orden.")

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
            st.markdown("### 🔧 Técnicos Asignados")
            st.write("• Carlos Gómez (En ruta)\n\n• Juan Pérez (Disponible)")
        
    st.subheader("📊 Monitoreo Global de Servicios")
    st.dataframe(st.session_state.mantenimientos, use_container_width=True, hide_index=True)
