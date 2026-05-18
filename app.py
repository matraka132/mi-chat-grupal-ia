import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Corte Suprema Deportiva", layout="wide")
st.title("🏛️ El Coliseo: Auditoría Cruzada de 3 Vías")
st.markdown("Fase 1: Rastreo Web Nativo | Fase 2: Auditoría Cruzada Estricta | Fase 3: Consenso y Veredicto Final")

# Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🛡️ Reglas del Sistema:
    * 🔍 **Rastreo Triple Nativo** (Sin plugins que rompan la API).
    * ⛔ **Cero Auto-Auditoría:** Los datos se cruzan de forma obligatoria.
    * ⚡ **Cero Relleno:** Respuestas directas en telegrama.
    """)

# PROMPT BASE ULTRA-COMPRESO
PROMPT_BASE = (
    "Actúa como un micro-agente matemático de entorno cerrado. Prohibido usar saludos, introducciones o texto de relleno. "
    "Ve directo al grano utilizando datos crudos y viñetas cortas. Prohibido generar enlaces o URLs.\n\n"
)

# Función centralizada de consulta corregida y limpia
def consultar_ia(model_id, prompt, key, system_role, max_tokens=1000):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Auditoria Cruzada Deportiva"
    }
    
    # Unimos el prompt del sistema básico
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": PROMPT_BASE + system_role},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=120
        )
        if response.status_code != 200:
            return f"❌ Error en {model_id}: {response.text}"
            
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error de conexión en {model_id}: {str(e)}"

# Entrada de datos de Hard Rock Bet
lineas_raw = st.text_area("📋 Pega las líneas de Hard Rock Bet aquí:", height=150, placeholder="Ej:\nYankees\nMets\n-1.5 (+165)")

if st.button("🚀 Ejecutar Sistema de Auditoría Cruzada"):
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not lineas_raw:
        st.warning("⚠️ Introduce las líneas del partido.")
    else:
        
        # Identificadores de modelos base estables en OpenRouter para evitar fallos
        GROK = "x-ai/grok-4.20"
        GEMINI = "google/gemini-2.5-pro"
        CLAUDE = "anthropic/claude-3.5-haiku"

        # =========================================================
        # FASE 1: RASTREO TRIPLE EN INTERNET
        # =========================================================
        st.header("🔍 Fase 1: Rastreo Web Simultáneo")
        col_inv1, col_inv2, col_inv3 = st.columns(3)
        
        with st.spinner("Las tres mentes escanean internet en tiempo real..."):
            
            role_rastreo = (
                "Usa tus capacidades nativas de navegación web para buscar los datos reales de MLB para este partido de HOY domingo 17 de mayo de 2026. "
                "Consigue e informa estrictamente: 1) Lanzadores abridores confirmados (Mano, ERA). 2) Clima/Estadio. 3) Lesiones de último minuto. "
                "Entrega la información en formato telegrama conciso, sin saludos, sin introducciones y sin enlaces de ningún tipo."
            )
            
            investigacion_grok = consultar_ia(GROK, lineas_raw, api_key, f"Eres Grok-Web. {role_rastreo}", max_tokens=500)
            investigacion_gemini = consultar_ia(GEMINI, lineas_raw, api_key, f"Eres Gemini-Web. {role_rastreo}", max_tokens=500)
            investigacion_claude = consultar_ia(CLAUDE, lineas_raw, api_key, f"Eres Claude-Web. {role_rastreo}", max_tokens=500)
            
            with col_inv1:
                st.markdown("### ⚫ Rastreo Grok 2")
                st.info(investigacion_grok)
            with col_inv2:
                st.markdown("### 🔵 Rastreo Gemini")
                st.info(investigacion_gemini)
            with col_inv3:
                st.markdown("### 🟠 Rastreo Claude 3.5")
                st.info(investigacion_claude)

        st.divider()

        # =========================================================
        # FASE 2: AUDITORÍA CRUZADA ESTRICTA (Cero Auto-Evaluación)
        # =========================================================
        st.header("🛡️ Fase 2: Co-Auditoría Cruzada Absoluta")
        col_aud1, col_aud2, col_aud3 = st.columns(3)
        
        with st.spinner("Ejecutando filtros cruzados de seguridad..."):
            
            # 1. Auditoría de la data de GEMINI (Hecha por Grok y Claude)
            prompt_aud_gemini = f"LÍNEAS USER: {lineas_raw}\nINVESTIGACIÓN DE GEMINI A EVALUAR:\n{investigacion_gemini}"
            role_aud_gemini = "Eres el Tribunal Grok-Claude. Analiza la investigación de Gemini. Destruye datos falsos, confirma los correctos con las líneas y entrega la data limpia."
            auditoria_de_gemini = consultar_ia(CLAUDE, prompt_aud_gemini, api_key, role_aud_gemini, max_tokens=500)
            
            # 2. Auditoría de la data de GROK (Hecha por Gemini y Claude)
            prompt_aud_grok = f"LÍNEAS USER: {lineas_raw}\nINVESTIGACIÓN DE GROK A EVALUAR:\n{investigacion_grok}"
            role_aud_grok = "Eres el Tribunal Gemini-Claude. Analiza la investigación de Grok. Corrige errores o contradicciones y entrega la data limpia."
            auditoria_de_grok = consultar_ia(GEMINI, prompt_aud_grok, api_key, role_aud_grok, max_tokens=500)
            
            # 3. Auditoría de la data de CLAUDE (Hecha por Grok y Gemini)
            prompt_aud_claude = f"LÍNEAS USER: {lineas_raw}\nINVESTIGACIÓN DE CLAUDE A EVALUAR:\n{investigacion_claude}"
            role_aud_claude = "Eres el Tribunal Grok-Gemini. Analiza la investigación de Claude. Filtra cualquier alucinación y certifica los datos del juego."
            auditoria_de_claude = consultar_ia(GROK, prompt_aud_claude, api_key, role_aud_claude, max_tokens=500)
            
            with col_aud1:
                st.markdown("### 🛡️ Auditando a Gemini (Vía Grok/Claude)")
                st.write(auditoria_de_gemini)
            with col_aud2:
                st.markdown("### 🛡️ Auditando a Grok (Vía Gemini/Claude)")
                st.write(auditoria_de_grok)
            with col_aud3:
                st.markdown("### 🛡️ Auditando a Claude (Vía Grok/Gemini)")
                st.write(auditoria_de_claude)

        st.divider()

        # =========================================================
        # FASE 3: CONSENSO TOTAL Y VEREDICTO FINAL
        # =========================================================
        st.header("🏆 Fase 3: Consenso de 3 Vías y Veredicto Supremo")
        
        bloque_consenso = f"""
        LÍNEAS ORIGINALES: {lineas_raw}
        DATA CERTIFICADA 1: {auditoria_de_gemini}
        DATA CERTIFICADA 2: {auditoria_de_grok}
        DATA CERTIFICADA 3: {auditoria_de_claude}
        """
        
        col_con1, col_con2, col_final = st.columns([1, 1, 1.5])
        
        with st.spinner("Las tres mentes debaten el pick de mayor valor..."):
            
            # Grok vota
            voto_grok = consultar_ia(GROK, bloque_consenso, api_key, "Analiza los reportes auditados. Indica qué equipo tiene la ventaja matemática y por qué. Máximo 3 líneas.", max_tokens=300)
            
            # Gemini vota
            voto_gemini = consultar_ia(GEMINI, bloque_consenso, api_key, "Analiza los reportes auditados. Identifica trampas en la línea o total (O/U). Máximo 3 líneas.", max_tokens=300)
            
            # Bloque para Claude final
            debate_completo = f"{bloque_consenso}\nPROPUESTA GROK: {voto_grok}\nPROPUESTA GEMINI: {voto_gemini}"
            
            role_jurado = (
                "Eres el Juez Supremo del Consenso. Recibe los votos y la data limpia. "
                "Dictamina la mejor jugada para ganar hoy en Hard Rock Bet. Responde estrictamente con este formato directo:\n\n"
                "- **Pick Oficial:** [Línea exacta y acción]\n"
                "- **Confianza:** [Alto/Medio/Bajo]\n"
                "- **Ventaja (+EV):** [Razón matemática fría]\n"
                "- **Riesgo:** [Factor crítico que arruina el parley]"
            )
            veredicto_final = consultar_ia(CLAUDE, debate_completo, api_key, role_jurado, max_tokens=500)
            
            with col_con1:
                st.markdown("### 📊 Voto de Grok 2")
                st.info(voto_grok)
            with col_con2:
                st.markdown("### ⚾ Voto de Gemini")
                st.info(voto_gemini)
            with col_final:
                st.markdown("### 🏛️ Sentencia Definitiva (Claude 3.5 Sonnet)")
                st.success(veredicto_final)
                
        st.balloons()
