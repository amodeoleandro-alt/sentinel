// ---------- Traducciones ----------
const CENTINEL_TRADUCCIONES = {
  es: {
    nav_inicio: "Inicio",
    nav_camaras: "Cámaras",
    nav_grabaciones: "Grabaciones",
    nav_ajustes: "Ajustes",
    nav_administracion: "Administración",
    nav_salir: "Salir",
    live: "EN VIVO",
    footer_text: "Centinel © 2026 - Sistema de Monitoreo de Cámaras",

    inicio_bienvenida: "Bienvenido a Centinel. Desde acá podés visualizar tus cámaras en tiempo real y consultar las grabaciones almacenadas.",

    camaras_titulo: "Cámaras",
    camaras_subtitulo: "Vista en vivo (simulada) de las cámaras registradas.",
    camaras_expandir: "Expandir",
    camaras_volver: "Volver",

    grab_titulo: "Grabaciones",
    grab_subtitulo: "Listado de grabaciones (simuladas). Se obtiene dinámicamente desde el backend.",
    grab_vacio: "No hay grabaciones.",
    grab_col_fecha: "Fecha",
    grab_col_hora: "Hora",
    grab_col_camara: "Cámara",
    grab_col_duracion: "Duración",
    grab_col_accion: "Acción",
    grab_ver: "Ver",
    almacenamiento_titulo: "Almacenamiento",
    almacenamiento_usado: "utilizado",

    ajustes_titulo: "Ajustes",
    ajustes_subtitulo: "Personalizá la apariencia y preferencias del sistema.",
    ajustes_apariencia: "Apariencia",
    ajustes_tema: "Tema",
    ajustes_tema_oscuro: "Modo oscuro",
    ajustes_tema_claro: "Modo claro",
    ajustes_idioma: "Idioma",
    ajustes_zona: "Zona horaria",
    ajustes_guardar: "Guardar cambios",
    ajustes_guardado: "Guardado",
    ajustes_notif: "Notificaciones",
    ajustes_notif_mov: "Alertas de movimiento detectado",
    ajustes_notif_desc: "Alertas de cámara desconectada",
    ajustes_notif_mail: "Recibir resumen diario por correo",
    ajustes_estado: "Estado del sistema",
    ajustes_zona_actual: "Zona horaria actual",
    ajustes_idioma_actual: "Idioma actual",
    ajustes_tema_actual: "Tema actual",
    ajustes_nota: "Las preferencias se guardan en este navegador. La persistencia por usuario en base de datos se agrega en la siguiente iteración.",

    admin_titulo: "Administración de usuarios",
    admin_buscar: "Buscar por nombre o correo...",
    admin_col_nombre: "Nombre",
    admin_col_correo: "Correo",
    admin_col_rol: "Rol",
    admin_col_activo: "Activo",
    admin_col_creado: "Creado",
    admin_col_acceso: "Último acceso",
    admin_col_acciones: "Acciones",

    perfil_titulo: "Mi perfil",
    perfil_nombre: "Nombre",
    perfil_correo: "Correo",
    perfil_rol: "Rol",
    perfil_creacion: "Fecha de creación",
    perfil_acceso: "Último acceso",
    perfil_cambiar_pass: "Cambiar contraseña",
  },
  en: {
    nav_inicio: "Home",
    nav_camaras: "Cameras",
    nav_grabaciones: "Recordings",
    nav_ajustes: "Settings",
    nav_administracion: "Administration",
    nav_salir: "Log out",
    live: "LIVE",
    footer_text: "Centinel © 2026 - Camera Monitoring System",

    inicio_bienvenida: "Welcome to Centinel. From here you can view your cameras live and check stored recordings.",

    camaras_titulo: "Cameras",
    camaras_subtitulo: "Live (simulated) view of registered cameras.",
    camaras_expandir: "Expand",
    camaras_volver: "Back",

    grab_titulo: "Recordings",
    grab_subtitulo: "List of (simulated) recordings. Fetched dynamically from the backend.",
    grab_vacio: "No recordings found.",
    grab_col_fecha: "Date",
    grab_col_hora: "Time",
    grab_col_camara: "Camera",
    grab_col_duracion: "Duration",
    grab_col_accion: "Action",
    grab_ver: "View",
    almacenamiento_titulo: "Storage",
    almacenamiento_usado: "used",

    ajustes_titulo: "Settings",
    ajustes_subtitulo: "Customize the system's appearance and preferences.",
    ajustes_apariencia: "Appearance",
    ajustes_tema: "Theme",
    ajustes_tema_oscuro: "Dark mode",
    ajustes_tema_claro: "Light mode",
    ajustes_idioma: "Language",
    ajustes_zona: "Time zone",
    ajustes_guardar: "Save changes",
    ajustes_guardado: "Saved",
    ajustes_notif: "Notifications",
    ajustes_notif_mov: "Motion detection alerts",
    ajustes_notif_desc: "Camera disconnected alerts",
    ajustes_notif_mail: "Receive daily summary by email",
    ajustes_estado: "System status",
    ajustes_zona_actual: "Current time zone",
    ajustes_idioma_actual: "Current language",
    ajustes_tema_actual: "Current theme",
    ajustes_nota: "Preferences are saved in this browser. Per-user database persistence will be added in the next iteration.",

    admin_titulo: "User administration",
    admin_buscar: "Search by name or email...",
    admin_col_nombre: "Name",
    admin_col_correo: "Email",
    admin_col_rol: "Role",
    admin_col_activo: "Active",
    admin_col_creado: "Created",
    admin_col_acceso: "Last login",
    admin_col_acciones: "Actions",

    perfil_titulo: "My profile",
    perfil_nombre: "Name",
    perfil_correo: "Email",
    perfil_rol: "Role",
    perfil_creacion: "Creation date",
    perfil_acceso: "Last login",
    perfil_cambiar_pass: "Change password",
  }
};

// ---------- Motor de preferencias (tema / idioma / zona) ----------
const CentinelPrefs = {
  KEY: "centinel_ajustes",

  get() {
    return JSON.parse(localStorage.getItem(this.KEY) || "{}");
  },

  set(prefs) {
    const actuales = this.get();
    const nuevas = { ...actuales, ...prefs };
    localStorage.setItem(this.KEY, JSON.stringify(nuevas));
    this.aplicarTodo(nuevas);
    return nuevas;
  },

  getIdioma() {
    return this.get().idioma || "es";
  },

  t(clave) {
    const idioma = this.getIdioma();
    return (CENTINEL_TRADUCCIONES[idioma] && CENTINEL_TRADUCCIONES[idioma][clave]) || clave;
  },

  aplicarTema(tema) {
    if (tema === "light") {
      document.body.classList.add("theme-light");
    } else {
      document.body.classList.remove("theme-light");
    }
  },

  aplicarIdioma(idioma) {
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const clave = el.getAttribute("data-i18n");
      const texto = (CENTINEL_TRADUCCIONES[idioma] && CENTINEL_TRADUCCIONES[idioma][clave]);
      if (texto) el.textContent = texto;
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
      const clave = el.getAttribute("data-i18n-placeholder");
      const texto = (CENTINEL_TRADUCCIONES[idioma] && CENTINEL_TRADUCCIONES[idioma][clave]);
      if (texto) el.setAttribute("placeholder", texto);
    });
  },

  aplicarTodo(prefs) {
    const p = prefs || this.get();
    this.aplicarTema(p.tema || "dark");
    this.aplicarIdioma(p.idioma || "es");
  }
};

window.CentinelPrefs = CentinelPrefs;

document.addEventListener("DOMContentLoaded", () => {
  CentinelPrefs.aplicarTodo();

  const toggleBtn = document.getElementById("toggleSidebar");
  const sidebar = document.getElementById("sidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", () => sidebar.classList.toggle("show"));
  }

  // Cierre de sesión automático por inactividad (requisito: sesiones)
  const INACTIVITY_LIMIT_MS = 30 * 60 * 1000; // 30 minutos
  let inactivityTimer;
  function resetTimer() {
    clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => {
      window.location.href = "/logout";
    }, INACTIVITY_LIMIT_MS);
  }
  if (document.getElementById("sidebar")) {
    ["mousemove", "keydown", "click", "scroll"].forEach(evt =>
      document.addEventListener(evt, resetTimer)
    );
    resetTimer();
  }
});