import streamlit as st
import requests
from datetime import date
import pandas as pd
import altair as alt

# ==============================
# CONFIGURACIÓN
# ==============================
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="RetNova",
    page_icon="🎯",
    layout="wide"
)

# ==============================
# HELPERS
# ==============================
def api_get(endpoint, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.get(f"{API_URL}{endpoint}", headers=headers)

def api_post(endpoint, data=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.post(f"{API_URL}{endpoint}", json=data, headers=headers)

def api_put(endpoint, data=None, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.put(f"{API_URL}{endpoint}", json=data, headers=headers)

def login_request(username: str, password: str):
    data = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return requests.post(f"{API_URL}/auth/login", data=data, headers=headers)

def require_login():
    if "token" not in st.session_state:
        st.error("Debes iniciar sesión primero.")
        st.stop()

# ==============================
# LOGIN
# ==============================
def login_screen():
    st.title("🔐 Iniciar Sesión")

    nombre_usuario = st.text_input("Nombre de usuario")
    contrasena = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        res = login_request(nombre_usuario, contrasena)

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access_token"]
            st.session_state.rol = data["usuario"]["rol"]
            st.session_state.user_id = data["usuario"]["id"]
            st.rerun()
        else:
            st.error(res.json().get("error", "LOGIN_CONTRASENA_INCORRECTA"))

# ==============================
# SIDEBAR
# ==============================
def header():
    st.sidebar.title("🎯 RetNova")
    st.sidebar.markdown(f"👤 Usuario ID: **{st.session_state.user_id}**")
    st.sidebar.markdown(f"🔑 Rol: **{st.session_state.rol}**")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()



# ==============================
# SOLICITANTE — Ver mis retos
# ==============================
def vista_mis_retos_solicitante():
    st.title("📄 Mis Retos")

    res = api_get("/retos/listar", st.session_state.token)
    if res.status_code != 200:
        st.error("Error cargando retos")
        return

    retos = res.json()
    mis = [r for r in retos if r["solicitante_id"] == st.session_state.user_id]

    for r in mis:
        st.markdown(f"""
        <div style="padding:12px;border-radius:10px;background:#eef;">
            <h4>{r['titulo']}</h4>
            <p><b>Estado:</b> {r['estado']}</p>
            <p><b>Fecha entrega:</b> {r['fecha_entrega']}</p>
            <p><b>Responsable:</b> {r['responsable_id']}</p>
            

        </div>
        """, unsafe_allow_html=True)

# ==============================
# LÍDER — Asignar responsable
# ==============================
def vista_asignar_responsable():
    st.title("🟦 Asignar Responsable")

    res_retos = api_get("/retos/listar", st.session_state.token)
    if res_retos.status_code != 200:
        st.error("No se pudieron cargar los retos.")
        return

    res_users = api_get("/auth/usuarios", st.session_state.token)
    if res_users.status_code != 200:
        st.error("No se pudieron cargar los usuarios.")
        return

    retos = res_retos.json()
    usuarios = res_users.json()
    miembros = [u for u in usuarios if u["rol"] == "Miembro"]

    reto_sel = st.selectbox("Seleccione reto", retos, format_func=lambda r: r["titulo"])
    usuario_sel = st.selectbox("Seleccione responsable", miembros, format_func=lambda u: u["nombre_usuario"])

    if st.button("Asignar"):
        url = f"/retos/asignar-responsable/{reto_sel['id']}/{usuario_sel['id']}"
        res = api_put(url, token=st.session_state.token)

        if res.status_code == 200:
            st.success("Responsable asignado")
        else:
            st.error("No se pudo asignar")

# ==============================
# MIEMBRO — Mis retos asignados
# ==============================
def vista_mis_retos_asignados():
    st.title("📝 Mis Retos Asignados")

    res = api_get("/retos/listar", st.session_state.token)
    retos = res.json()

    mis = [r for r in retos if r["responsable_id"] == st.session_state.user_id]

    for r in mis:
        st.markdown(f"""
        <div style="padding:12px;border-radius:10px;background:#dff;">
            <h4>{r['titulo']}</h4>
            <p>Estado: {r['estado']}</p>
            <p>Fecha entrega: {r['fecha_entrega']}</p>
            <p>Observaciones: {r['observaciones']}</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================
# MIEMBRO/LÍDER — Cambiar estado
# ==============================
def vista_cambiar_estado():
    st.title("🟨 Cambiar Estado")

    res_retos = api_get("/retos/listar", st.session_state.token)
    retos = res_retos.json()

    mis_retos = [r for r in retos if r["responsable_id"] == st.session_state.user_id]

    # 🔥 Cargar estados desde FastAPI
    res_est = api_get("/catalogo/ESTADOS_RETO", st.session_state.token)
    estados = res_est.json() if res_est.status_code == 200 else []

    reto_sel = st.selectbox("Seleccione reto", mis_retos, format_func=lambda r: r["titulo"])
    nuevo_estado = st.selectbox("Nuevo estado", estados)

    if st.button("Actualizar"):
        url = f"/retos/cambiar-estado/{reto_sel['id']}/{nuevo_estado}"
        res = api_put(url, token=st.session_state.token)

        if res.status_code == 200:
            st.success("Estado actualizado")
        else:
            st.error(res.json()["error"])

def vista_cambiar_estado_lider():
    st.title("🟧 Cambiar Estado (Líder)")

    # Obtener todos los retos
    res_retos = api_get("/retos/listar", st.session_state.token)
    if res_retos.status_code != 200:
        st.error(res_retos.json().get("error", "Error cargando los retos"))
        return

    retos = res_retos.json()

    if not isinstance(retos, list) or len(retos) == 0:
        st.warning("No hay retos registrados.")
        return

    # Cargar estados
    res_est = api_get("/catalogo/ESTADOS_RETO", st.session_state.token)
    estados = res_est.json() if res_est.status_code == 200 else []

    # Convertir a tuplas para selectbox seguro
    opciones_retos = [(r["id"], r["titulo"], r) for r in retos]

    opcion = st.selectbox(
        "Seleccione un reto",
        opciones_retos,
        format_func=lambda x: f"{x[0]} - {x[1]}",
    )

    # x[2] contiene el dict del reto seleccionado
    reto_sel = opcion[2]

    nuevo_estado = st.selectbox("Nuevo estado", estados)

    if st.button("Actualizar Estado"):
        url = f"/retos/cambiar-estado/{reto_sel['id']}/{nuevo_estado}"
        res = api_put(url, token=st.session_state.token)

        if res.status_code == 200:
            st.success(res.json().get("mensaje", "CAMBIAR_ESTADO_OK"))
        else:
            st.error(res.json().get("error", "CAMBIAR_ESTADO_ERROR"))



def vista_eliminar_reto():
    st.title("❌ Eliminar Reto")

    res = api_get("/retos/listar", st.session_state.token)

    if res.status_code != 200:
        st.error("No se pudieron cargar los retos.")
        return

    retos = res.json()

    opcion = st.selectbox(
        "Seleccione un reto para eliminar",
        retos,
        format_func=lambda r: f"{r['id']} - {r['titulo']}"
    )

    if st.button("Eliminar"):
        res_del = requests.delete(
            f"{API_URL}/retos/eliminar/{opcion['id']}",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )

        if res_del.status_code == 200:
            st.success(res_del.json().get("mensaje", "ELIMINAR_RETO_OK"))
        else:
            st.error(res_del.json().get("error", "ELIMINAR_RETO_ERROR"))
            
# ==============================
# SOLICITANTE — Crear reto
# ==============================
def vista_solicitar_reto():
    st.title("🟢 Registrar Reto")

    # 🔥 Cargar categorías desde FastAPI
    res_cat = api_get("/catalogo/CATEGORIAS", st.session_state.token)
    categorias = res_cat.json() if res_cat.status_code == 200 else []

    titulo = st.text_input("Título")
    descripcion = st.text_area("Descripción")
    categoria = st.selectbox("Categoría", categorias)
    fecha_entrega = st.date_input("Fecha de entrega", min_value=date.today())
    observaciones = st.text_area("Observaciones")

    if st.button("Crear"):
        payload = {
            "titulo": titulo,
            "descripcion": descripcion,
            "categoria": categoria,
            "estado": "Pendiente",
            "fecha_entrega": str(fecha_entrega),
            "solicitante_id": st.session_state.user_id,
            "responsable_id": None,
            "observaciones": observaciones
        }

        res = api_post("/retos/registrar", payload, st.session_state.token)
        if res.status_code == 200:
            st.success("Reto creado correctamente")
        else:
            st.error(res.json()["error"])


# ==============================
# ADMIN — Usuarios
# ==============================
def vista_admin_usuarios():
    st.title("🛠️ Administración de Usuarios")

    res = api_get("/auth/usuarios", st.session_state.token)

    if res.status_code != 200:
        st.error("No se pudieron cargar los usuarios.")
        return

    usuarios = res.json()

    st.subheader("👥 Lista de usuarios")

    for u in usuarios:
        col1, col2 = st.columns([4, 1])

        with col1:
            estado_color = "🟢 Activo" if u["activo"] else "🔴 Inactivo"
            st.write(
                f"**{u['id']} - {u['nombre_usuario']}** "
                f"({u['rol']}) — {estado_color}"
            )

        with col2:

            # 🚫 Evitar autodesactivación
            if u["id"] == st.session_state.user_id:
                st.button("❌", key=f"self_{u['id']}", disabled=True)
                continue

            # Si está activo → mostrar botón desactivar
            if u["activo"]:
                if st.button("Desactivar", key=f"des_{u['id']}"):
                    desactivar_usuario_admin(u["id"])
                    st.rerun()

            # Si está inactivo → mostrar botón activar
            else:
                if st.button("Activar", key=f"act_{u['id']}"):
                    activar_usuario_admin(u["id"])
                    st.rerun()


# ==============================
# ADMIN — Auditoría
# ==============================
def vista_admin_auditoria():
    st.title("📜 Auditoría")

    res = api_get("/auditoria/", st.session_state.token)

    if res.status_code != 200:
        st.error(res.json().get("error", "No se pudo cargar la auditoría"))
        return

    eventos = res.json()

    # ========================
    # DESCARGA EN CSV
    # ========================
    import pandas as pd

    df = pd.DataFrame(eventos)

    # Convertir DataFrame a CSV en memoria
    csv_bytes = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Descargar auditoría en CSV",
        data=csv_bytes,
        file_name="auditoria_retnova.csv",
        mime="text/csv"
    )

    # ========================
    # VISUALIZACIÓN
    # ========================
    st.subheader("🔍 Registros de Auditoría")

    for e in eventos:
        st.markdown(f"""
        <div style="padding:12px;margin-bottom:8px;border-radius:8px;background:#f7f7f7;">
            <b>🕒 Fecha:</b> {e['fecha_evento']}<br>
            <b>📝 Acción:</b> {e['accion']}<br>
            <b>📌 Descripción:</b> {e['descripcion']}
        </div>
        """, unsafe_allow_html=True)

def vista_admin_crear_usuario():
    st.title("👤 Crear Usuario")

    nombre_usuario = st.text_input("Nombre de usuario")
    email = st.text_input("Email")
    contrasena = st.text_input("Contraseña", type="password")
    rol = st.selectbox("Rol", ["Solicitante", "Lider", "Miembro"])

    if st.button("Crear Usuario"):
        payload = {
            "nombre_usuario": nombre_usuario,
            "email": email,
            "contrasena": contrasena,
            "rol": rol
        }

        res = api_post("/auth/registrar", payload, st.session_state.token)
        
        if res.status_code == 200:
            st.success("Usuario creado correctamente")
        else:
            st.error(res.json()["error"])



def vista_listar_todos_retos():
    st.title("📋 Lista de Todos los Retos")

    res = api_get("/retos/listar", st.session_state.token)

    if res.status_code != 200:
        try:
            st.error(res.json()["error"])
        except:
            st.error("No se pudieron cargar los retos.")
        return

    retos = res.json()

    st.subheader(f"Total de retos: {len(retos)}")

    # Mostrarlos uno por uno
    for r in retos:
        st.markdown(f"""
        <div style="padding:12px;margin-bottom:10px;border-radius:10px;background:#eef;">
            <h4>{r['titulo']}</h4>
            <p><b>Descripción:</b> {r['descripcion']}</p>
            <p><b>Categoría:</b> {r['categoria']}</p>
            <p><b>Estado:</b> {r['estado']}</p>
            <p><b>Solicitante ID:</b> {r['solicitante_id']}</p>
            <p><b>Responsable ID:</b> {r['responsable_id']}</p>
            <p><b>Fecha entrega:</b> {r['fecha_entrega']}</p>
        </div>
        """, unsafe_allow_html=True)

def badge_estado(estado: str) -> str:
    colores = {
        "Pendiente": "#f1c40f",     # Amarillo
        "Asignado": "#3498db",      # Azul
        "En progreso": "#2980b9",   # Azul oscuro
        "Finalizado": "#2ecc71",    # Verde
        "Rechazado": "#e74c3c",     # Rojo
    }

    color = colores.get(estado, "#7f8c8d")  # Default gris

    return f"""
        <span style="
            background-color:{color};
            color:white;
            padding:4px 10px;
            border-radius:8px;
            font-size:0.85rem;">
            {estado}
        </span>
    """
def desactivar_usuario_admin(usuario_id):
    res = requests.put(
        f"{API_URL}/auth/desactivar/{usuario_id}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    if res.status_code == 200:
        st.success("Usuario desactivado correctamente.")
    else:
        st.error(res.json().get("error", "Error al desactivar usuario"))


def activar_usuario_admin(usuario_id):
    res = requests.put(
        f"{API_URL}/auth/activar/{usuario_id}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    if res.status_code == 200:
        st.success("Usuario activado correctamente.")
    else:
        st.error(res.json().get("error", "Error al activar usuario"))


def vista_dashboard():
    st.title("📊 Dashboard de Gestión de Retos")

    res = api_get("/retos/listar", st.session_state.token)
    if res.status_code != 200:
        st.error("No se pudieron cargar los retos.")
        return

    retos = res.json()
    if not retos:
        st.info("No hay retos registrados aún.")
        return

    df = pd.DataFrame(retos)

    # =========================
    #  KPIs
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📌 Total de Retos", len(df))
    col2.metric("🟡 Pendientes", len(df[df["estado"] == "Pendiente"]))
    col3.metric("🟢 Finalizados", len(df[df["estado"] == "Finalizado"]))
    col4.metric("🔵 En progreso", len(df[df["estado"] == "En progreso"]))

    st.markdown("---")

    # =========================
    #  Grafico: Retos por Estado
    # =========================
    st.subheader("📌 Retos por Estado")
    chart1 = alt.Chart(df).mark_bar().encode(
        x="estado:N",
        y="count():Q",
        color="estado:N"
    )
    st.altair_chart(chart1, use_container_width=True)

    # =========================
    #  Grafico: Retos por Responsable
    # =========================
    st.subheader("👥 Retos por Responsable")

    df_resp = df.copy()
    df_resp["responsable_id"] = df_resp["responsable_id"].fillna(0)

    chart2 = alt.Chart(df_resp).mark_bar().encode(
        x="responsable_id:N",
        y="count():Q",
        color="responsable_id:N"
    )
    st.altair_chart(chart2, use_container_width=True)

    # =========================
    #  Tabla completa
    # =========================
    st.subheader("📄 Detalle de Retos")

    df2 = df.copy()
    df2["estado"] = df2["estado"].apply(badge_estado)

    st.write(df2.to_html(escape=False), unsafe_allow_html=True)

    # --- Aquí insertas el botón ---
    csv_bytes = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Descargar detalles de retos (CSV)",
        data=csv_bytes,
        file_name="retos_detalle.csv",
        mime="text/csv"
    )
# ==============================
# MAIN
# ==============================
if "token" not in st.session_state:
    login_screen()
    st.stop()

header()

rol = st.session_state.rol

if rol == "Solicitante":
    menu = st.sidebar.radio("Menú", ["Solicitar Reto", "Mis Retos"])
    if menu == "Solicitar Reto":
        vista_solicitar_reto()
    else:
        vista_mis_retos_solicitante()

elif rol == "Lider":
    menu = st.sidebar.radio("Menú", ["Asignar Responsable","Cambiar Estado de Cualquier Reto","Dashboard", "Eliminar Reto"])
    if menu == "Asignar Responsable":
        vista_asignar_responsable()
    elif menu == "Cambiar Estado de Cualquier Reto":
        vista_cambiar_estado_lider()
    elif menu == "Dashboard":
        vista_dashboard()
    elif menu == "Eliminar Reto":
        vista_eliminar_reto()
    else:
        vista_listar_todos_retos()

elif rol == "Miembro":
    menu = st.sidebar.radio("Menú", ["Mis Retos Asignados", "Cambiar Estado"])
    if menu == "Mis Retos Asignados":
        vista_mis_retos_asignados()
    else:
        vista_cambiar_estado()

elif rol == "Administrador":
    menu = st.sidebar.radio("Menú", ["Usuarios", "Auditoría", "Crear Usuario"])

    if menu == "Usuarios":
        vista_admin_usuarios()
    elif menu == "Crear Usuario":
        vista_admin_crear_usuario()

    else:
        vista_admin_auditoria()

