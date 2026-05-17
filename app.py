import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Súper-Consenso Triple", layout="wide")
st.title("🏛️ El Súper-Coliseo: Flujo de Co-Auditoría Triple")
st.markdown("Fase 1: Investigación Abierta | Fase 2: Co-Auditoría Cerrada | Fase 3: Especialistas Triples | Fase 4: Veredicto")

# Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🧠 Motores del Sistema:
    * 🔍 **Grok 2 Search** (`x-ai/grok-2-search`)
    * 🔵 **Gemini 2.5 Pro** (`google/gemini-2.5-pro`)
    * 🟠 **Claude 3.5 Sonnet** (`anthropic/claude-3.5-sonnet`)
    """)

# PROMPT BASE PARA ENTORNO CERRADO (Para agentes analistas)
PROMPT_CERRADO = (
    "Eres un agente analítico de élite en un entorno hiper-seguro y cerrado. Prohibido usar conocimientos o "
    "suposiciones externas fuera de los datos provistos en el prompt actual o el reporte de búsqueda web de esta sesión.\n"
    "CRÍTICO: Está estrictamente prohibido generar enlaces, URLs o hipervínculos de ningún tipo. "
    "Entrega tus respuestas en texto plano limpio estructurado con Markdown estándar.\n\n"
)

# Función centralizada de consulta modificada
def consultar_ia(model_id, prompt, key, system_role, max_tokens=1500, ambiente_cerrado=True):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Súper-Coliseo Triple"
    }
    
    # Si es ambiente cerrado usa el escudo, si es Grok investigando lo dejamos libre
    prompt_sistema = (PROMPT_CERRADO + system_role) if ambiente_cerrado else system_role
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=90
        )
        if response.status_code != 200:
            return f"❌ Error en {model_id}: {response.text}"
            
        texto = response.json()["choices"][0]["message"]["content"]
        
        # Filtro de seguridad para remover URLs residuales
        if "http" in texto.lower():
            for word in texto.split():
                if "http" in word.lower():
                    texto = texto.replace(word, "[Dato Sanitizado]")
        return texto
    except Exception as e:
        return f"❌ Error de conexión en {model_id}: {str(e)}"

# Entrada de datos de Hard Rock Bet
lineas_raw = st.text_area("📋 Pega las líneas de Hard Rock Bet aquí:", height=150, placeholder="Ej:\nOrioles\nNationals\n-1.5 (+125)")

if st.button("🚀 Iniciar Ciclo del Súper-Coliseo"):
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not lineas_raw:
        st.warning("⚠️ Pega la información de las líneas primero.")
    else:
        
        # Identificadores Oficiales de Modelos
        GROK = "x-ai/grok-4.3"
        GEMINI = "google/gemini-2.5-pro"
        CLAUDE = "anthropic/claude-3.5-haiku"

        # =========================================================
        # FASE 1: INVESTIGACIÓN TRIPLE (Grok -> Gemini -> Claude)
        # =========================================================
        st.header("🔍 Fase 1: Investigación y Rastreo Triple")
        col_inv1, col_inv2, col_inv3 = st.columns(3)
        
        with st.spinner("Las tres mentes investigan y recopilan datos de la web..."):
            
            role_grok_web = (
                "Eres Grok 2 con acceso completo a internet en tiempo real. Tu única misión es tomar estas líneas de Hard Rock Bet, "
                "identificar qué partido de MLB es hoy domingo 17 de mayo de 2026 y BUSCAR EN LA WEB: 1) Lanzadores abridores confirmados "
                "con sus estadísticas básicas de este año. 2) El clima exacto a la hora del juego, velocidad/dirección del viento y tipo de estadio. "
                "3) Reporte de bajas o lesionados de última hora. No digas que no tienes datos, ¡búscalos en internet ahora mismo!"
            )
            
            # ambiente_cerrado=False permite que Grok use su buscador sin restricciones
            res_grok_inv = consultar_ia(GROK, lineas_raw, api_key, role_grok_web, max_tokens=1500, ambiente_cerrado=False)
            
            role_inv_resto = "Tu rol es procesar los datos de búsqueda web provistos en el contexto. Organiza: 1) Lanzadores confirmados. 2) Clima y viento del estadio. 3) Reporte de bajas de último minuto."
            res_gemini_inv = consultar_ia(GEMINI, f"Líneas del usuario: {lineas_raw}\nReporte de búsqueda web de Grok: {res_grok_inv}", api_key, f"Eres Gemini-Search. {role_inv_resto}", max_tokens=1200)
            res_claude_inv = consultar_ia(CLAUDE, f"Líneas del usuario: {lineas_raw}\nCompilación previa: {res_gemini_inv}", api_key, f"Eres Claude-Scout. {role_inv_resto}", max_tokens=1200)
            
            with col_inv1:
                st.markdown("### ⚫ Investigación Grok 2 (Web Abierta)")
                st.info(res_grok_inv)
            with col_inv2:
                st.markdown("### 🔵 Investigación Gemini")
                st.info(res_gemini_inv)
            with col_inv3:
                st.markdown("### 自由 Investigación Claude 3.5")
                st.info(res_claude_inv)

        st.divider()

        # =========================================================
        # FASE 2: AUDITORÍA TRIPLE CRUZADA (Filtro Anti-Errores)
        # =========================================================
        st.header("🛡️ Fase 2: Co-Auditoría Cruzada (Filtro de Seguridad)")
        col_aud1, col_aud2, col_aud3 = st.columns(3)
        
        prompt_auditoria = f"""
        LÍNEAS INICIALES: {lineas_raw}
        REPORTE GROK: {res_grok_inv}
        REPORTE GEMINI: {res_gemini_inv}
        REPORTE CLAUDE: {res_claude_inv}
        """
        
        with st.spinner("Cruzando datos entre sí para eliminar contradicciones o alucinaciones..."):
            
            role_aud = "Analiza los tres reportes de investigación previos. Encuentra contradicciones en abridores, clima o líneas. Entrega una base de datos depurada, unificada y corregida."
            
            aud_grok = consultar_ia(GROK, prompt_auditoria, api_key, f"Eres el Auditor de Grok. {role_aud}", max_tokens=1000)
            aud_gemini = consultar_ia(GEMINI, f"{prompt_auditoria}\nCrítica Grok: {aud_grok}", api_key, f"Eres el Auditor de Gemini. {role_aud}", max_tokens=1000)
            aud_claude = consultar_ia(CLAUDE, f"{prompt_auditoria}\nFiltros previos: {aud_gemini}", api_key, f"Eres el Auditor Jefe de Claude. {role_aud}", max_tokens=1200)
            
            with col_aud1:
                st.markdown("### 🛡️ Auditoría Grok")
                st.write(aud_grok)
            with col_aud2:
                st.markdown("### 🛡️ Auditoría Gemini")
                st.write(aud_gemini)
            with col_aud3:
                st.markdown("### 🛡️ Certificación Claude")
                st.code(aud_claude)

        st.divider()

        # =========================================================
        # FASE 3: ESPECIALISTAS TRIPLES (Debate Matemático y Deportivo)
        # =========================================================
        st.header("📢 Fase 3: Debate de Especialistas")
        col_esp1, col_esp2, col_esp3 = st.columns(3)
        
        with st.spinner("Grok, Gemini y Claude asumen sus roles de analistas..."):
            
            role_odd = "Eres el Especialista Oddsmaker (Grok). Sé directo. Analiza movimientos de líneas y valor en los momios en un máximo de 3 párrafos. Prohibido introducciones o saludos."
            res_oddsmaker = consultar_ia(GROK, aud_claude, api_key, role_odd, max_tokens=1200)
            
            role_sco = "Eres el Scout (Gemini). ¡Directo al grano! Analiza el duelo abridor-bateador y bullpens en viñetas cortas. Prohibido escribir encabezados como 'ID de Agente', 'Autorización', 'Entendido' o textos de relleno. Inicia directo con la data."
            res_scout = consultar_ia(GEMINI, aud_claude, api_key, role_sco, max_tokens=1200)
            
            role_ctx = "Eres el Especialista de Contexto (Claude). Analiza clima, fatiga y estadio de forma ejecutiva y compacta. Sin introducciones."
            res_contexto = consultar_ia(CLAUDE, aud_claude, api_key, role_ctx, max_tokens=1200)
            
            with col_esp1:
                st.markdown("### 📊 Grok (Mercado e Implícitas)")
                st.info(res_oddsmaker)
            with col_esp2:
                st.markdown("### ⚾ Gemini (Matchup y Rotación)")
                st.info(res_scout)
            with col_esp3:
                st.markdown("### 🌤️ Claude (Entorno y Tendencias)")
                st.info(res_contexto)

        st.divider()

        # =========================================================
        # FASE 4: JURADO Y VEREDICTO FINAL (Claude 3.5 Sonnet)
        # =========================================================
        st.subheader("🏆 Fase 4: Dictamen Supremo del Jurado (Claude 3.5 Sonnet)")
        
        bloque_final = f"""
        DATA CERTIFICADA Y AUDITADA: {aud_claude}
        INFORME MERCADO (Grok): {res_oddsmaker}
        INFORME SCOUT (Gemini): {res_scout}
        INFORME CONTEXTO (Claude): {res_contexto}
        """
        
        with st.spinner("Claude evalúa el debate completo de los especialistas y dicta sentencia..."):
            
            role_jurado = (
                "Eres el Jurado Final y Juez Supremo de Claude. Tu palabra es la ley del sistema. "
                "Recopila los tres informes de los especialistas, detecta dónde está el valor matemático esperado (+EV) "
                "y entrega el veredicto definitivo. Responde estrictamente con esta estructura:\n\n"
                "- **Pick Oficial Definitivo:** [Escribe aquí el Bet / Lean / Pass y la línea exacta]\n"
                "- **Grado de Confianza** [Alto / Medio / Bajo]\n"
                "- **Ventaja Matemática Detectada:** [Tu justificación basada solo en la data previa]\n"
                "- **Protocolo de Riesgo:** [Qué factor o imprevisto específico del juego destruye el pick]"
            )
            
            veredicto_maestro = consultar_ia(CLAUDE, bloque_final, api_key, role_jurado, max_tokens=1500)
            
            st.success(veredicto_maestro)
            st.balloons()
