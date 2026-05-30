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

# --- POOL GLOBAL DE MANTENIMIENTOS ---
if "mantenimientos" not in st.session_state:
    st.session_state.mantenimientos = [
        {
            "id": 1, 
            "cliente": "INDHECA / CARECO", 
            "equipo": "KENWORTH T680 (Eco: A-TC-K-35)", 
            "estado": "Disponible", 
            "tecnico": "Ninguno",
            "descripcion": "Servicio preventivo completo. Cambio de aceite, filtros de aire y combustible.",
            "monto": "$2,800.00 MXN",
            "fecha_prog": "02/06/2026",
            "fecha_fin": "-",
            "municipio": "Veracruz",
            "semaforo": "🟡 Próximo"
        },
        {
            "id": 2, 
            "cliente": "CONSTRUCTORA DELTA", 
            "equipo": "KENWORTH T800 (Eco: TC-17)", 
            "estado": "Disponible", 
            "tecnico": "Ninguno",
            "descripcion": "Corrección de fuga de aire en válvula de frenos y revisión de presión.",
            "monto": "$1,500.00 MXN",
            "fecha_prog": "29/05/2026",
            "fecha_fin": "-",
            "municipio": "Boca del Río",
            "semaforo": "🔴 Retrasado"
        },
        {
            "id": 3, 
            "cliente": "INDHECA / CARECO", 
            "equipo": "MACK anthem 48 (Eco: A-TC-M-32)", 
            "estado": "Completado", 
            "tecnico": "Carlos Gómez",
            "descripcion": "Inspección inicial de niveles e inspección de fluidos. Todo en orden.",
            "monto": "$1,200.00 MXN",
            "fecha_prog": "25/05/2026",
            "fecha_fin": "26/05/2026",
            "municipio": "Veracruz",
            "semaforo": "✅ Finalizado"
        },
    ]

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center;'>🏎️ Portal de Servicios</h1>", unsafe_html=True)

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
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            with st.expander("➕ Agregar Nueva Unidad", expanded=False):
                new_eco = st.text_input("Número Económico:", placeholder="Ej. A-TC-K-45")
                new_marca = st.selectbox("Marca:", ["KENWORTH", "MACK", "CATERPILLAR", "OTRO"])
                new_modelo = st.text_input("Modelo:", placeholder="Ej. T680")
                new_ano = st.number_input("Año Modelo:", min_value=2000, max_value=2027, value=2026)
                
                if st.button("Guardar Unidad 💾", type="primary", key="btn_add"):
                    if new_eco:
                        st.session_state.equipos_reales.append({
                            "eco": new_eco, "marca": new_marca, "modelo": new_modelo, "ano": int(new_ano), "status": "activo"
                        })
                        st.success(f"¡Unidad {new_eco} agregada correctamente!")
                        st.rerun()

        with col_btn2:
            with st.expander("📝 Editar Unidad Existente", expanded=False):
                lista_ecos = [e["eco"] for e in st.session_state.equipos_reales]
                eco_a_editar = st.selectbox("Selecciona el Económico a modificar:", lista_ecos)
                datos_actuales = next((item for item in st.session_state.equipos_reales if item["eco"] == eco_a_editar), None)
                edit_modelo = st.text_input("Modificar Modelo:", value=datos_actuales["modelo"] if datos_actuales else "")
                edit_status = st.selectbox("Modificar Estatus:", ["activo", "en taller", "baja"], index=0)
                
                if st.button("Actualizar Cambios 🔄", key="btn_edit"):
                    for e in st.session_state.equipos_reales:
                        if e["eco"] == eco_a_editar:
                            e["modelo"] = edit_modelo
                            e["status"] = edit_status
                    st.success(f"¡Unidad {eco_a_editar} actualizada con éxito!")
                    st.rerun()
        
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
                tipo_maint = st.selectbox("Tipo de Servicio:", ["Preventivo (Cambio de filtros/fluidos)", "Correctivo (Falla reportada)"])
                
            detalles = st.text_area("Observaciones o síntomas reportados por el operador:")
            
            if st.button("Enviar Orden de Servicio", type="primary", key="btn_solicitar"):
                # SOLUCIÓN: Agregamos llave 'semaforo' por defecto para evitar el KeyError
                st.session_state.mantenimientos.append({
                    "id": len(st.session_state.mantenimientos) + 1,
                    "cliente": "INDHECA / CARECO",
                    "equipo": equipo_sel,
                    "estado": "Disponible",
                    "tecnico": "Ninguno",
                    "descripcion": f"[{tipo_maint}] Km: {km_reportado}. Obs: {detalles}",
                    "monto": "$2,500.00 MXN",
                    "fecha_prog": "05/06/2026",
                    "fecha_fin": "-",
                    "municipio": "Veracruz",
                    "semaforo": "🟢 En tiempo"
                })
                st.success(f"¡Solicitud de servicio enviada al pool de técnicos!")

    with tab3:
        st.subheader("Historial y Estatus Detallado de Órdenes")
        for m in st.session_state.mantenimientos:
            with st.container(border=True):
                col_info, col_status = st.columns([3, 1])
                with col_info:
                    st.markdown(f"### 🚛 {m['equipo']}")
                    st.markdown(f"**Descripción:** {m['descripcion']}")
                    st.markdown(f"👤 **Técnico Asignado:** {m['tecnico']}")
                    st.markdown(f"📅 **Programación/Cierre:** {m['fecha_fin'] if m['estado'] == 'Completado' else m['fecha_prog']}")
                with col_status:
                    st.write("")
                    if m["estado"] == "Completado":
                        st.success("🟢 COMPLETADO")
                    elif m["estado"] == "Aceptado":
                        st.warning("🟡 EN PROCESO")
                    else:
                        st.info("🔵 EN POOL")

# ================= ROL: TÉCNICO =================
elif rol == "Técnico":
    st.header("Panel de Operaciones: Carlos Gómez (Técnico)")
    
    tab_disponibles, tab_mis_ordenes = st.tabs(["📌 Mantenimientos Disponibles", "📋 Mis Órdenes de Trabajo"])
    
    # ---- PESTAÑA 1: INTERFAZ ESTILO UBER/RAPPI ----
    with tab_disponibles:
        st.subheader("⚡ Solicitudes en tu Zona (Boca del Río / Veracruz)")
        st.caption("Toma un servicio de la lista para asignártelo de inmediato.")
        
        pool_disponible = [m for m in st.session_state.mantenimientos if m["estado"] == "Disponible"]
        
        if not pool_disponible:
            st.info("No hay servicios disponibles en el pool en este momento. ¡Buen trabajo!")
        else:
            for m in pool_disponible:
                with st.container(border=True):
                    col_detalles, col_ganancia = st.columns([3, 1])
                    
                    with col_detalles:
                        st.markdown(f"### 🚛 {m['equipo']}")
                        st.markdown(f"**📍 Ubicación:** {m['municipio']}")
                        st.markdown(f"**📅 Requerido para:** {m['fecha_prog']}")
                        st.markdown(f"**📝 Trabajo:** {m['descripcion']}")
                    
                    with col_ganancia:
                        st.metric(label="Pago por Servicio", value=m["monto"])
                        st.write("")
                        
                    col_b1, col_b2, col_blank = st.columns([1, 1, 2])
                    with col_b1:
                        if st.button("Aceptar Trabajo ⚡", key=f"accept_{m['id']}", type="primary"):
                            m["estado"] = "Aceptado"
                            m["tecnico"] = "Carlos Gómez"
                            st.success(f"¡Trabajo {m['id']} asignado a tu cuenta!")
                            st.rerun()
                    with col_b2:
                        if st.button("Ver Detalles 🔍", key=f"details_{m['id']}"):
                            st.toast(f"Detalles ampliado de la orden {m['id']}: Cliente {m['cliente']}.", icon="ℹ️")

    # ---- PESTAÑA 2: ÓRDENES PROPIAS Y SEMAFORIZACIÓN ----
    with tab_mis_ordenes:
        st.subheader("📊 Control General de mis Órdenes")
        
        mis_servicios = [m for m in st.session_state.mantenimientos if m["tecnico"] == "Carlos Gómez"]
        
        if not mis_servicios:
            st.info("Aún no tienes órdenes asignadas o completadas. Ve a la pestaña de 'Disponibles'.")
        else:
            for m in mis_servicios:
                with st.container(border=True):
                    c_main, c_semaforo = st.columns([3, 1])
                    
                    with c_main:
                        st.markdown(f"### 📦 Orden #{m['id']} - {m['equipo']}")
                        st.markdown(f"**Cliente:** {m['cliente']}")
                        st.markdown(f"**Fecha programada de entrega:** {m['fecha_prog']}")
                        if m["estado"] == "Completado":
                            st.markdown(f"✅ *Finalizado el:* {m['fecha_fin']}")
                    
                    with c_semaforo:
                        if m["estado"] == "Completado":
                            st.success("✅ COMPLETADO")
                        else:
                            # Uso seguro de .get() para evitar caídas imprevistas
                            m_semaforo = m.get("semaforo", "🟢 En tiempo")
                            if "Retrasado" in m_semaforo:
                                st.error(m_semaforo)
                            elif "Próximo" in m_semaforo:
                                st.warning(m_semaforo)
                            else:
                                st.info(m_semaforo)
                    
                    if m["estado"] == "Aceptado":
                        st.markdown("---")
                        st.markdown("**📋 Check-list de Ejecución:**")
                        p1 = st.checkbox("Inspección visual general y Check-list de fluidos inicial.", key=f"p1_{m['id']}")
                        p2 = st.checkbox("Limpieza de filtros y fluidos.", key=f"p2_{m['id']}")
                        p3 = st.checkbox("Prueba de presión y arranque.", key=f"p3_{m['id']}")
                        
                        if p1 and p2 and p3:
                            if st.button("Finalizar y Entregar Unidad 🏁", type="primary", key=f"fin_{m['id']}"):
                                m["estado"] = "Completado"
                                m["fecha_fin"] = "30/05/2026"
                                m["semaforo"] = "✅ Finalizado"
                                st.success("¡Orden completada con éxito!")
                                st.rerun()

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
