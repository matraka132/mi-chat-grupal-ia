import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Consenso Automatizado", layout="wide")
st.title("🏛️ Consenso Deportivo v4: Multi-IA (Grok + Gemini + Claude)")
st.markdown("Automatización total: **Grok** investiga la web, **Gemini** audita y analiza como especialista, y **Claude** dicta el veredicto final.")

# Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### ⚙️ Asignación de Inteligencias:
    * 🔍 **Investigador:** `Grok 2 Search` (x-AI)
    * 🛡️ **Auditor:** `Gemini 2.5 Pro` (Google)
    * 📋 **Especialistas:** `Gemini 2.5 Pro` (Google)
    * ⚖️ **Tribunal y Dictamen:** `Claude 3.5 Sonnet` (Anthropic)
    """)

# PROMPT BASE CRÍTICO
PROMPT_BASE = (
    "Eres un agente analítico avanzado en un entorno cerrado. Prohibido usar conocimiento previo que no esté "
    "explícitamente en el texto de entrada o en los datos web recuperados en esta sesión.\n"
    "CRÍTICO: Está estrictamente prohibido generar enlaces, URLs o hipervínculos de cualquier tipo. "
    "Entrega tu respuesta utilizando únicamente texto plano estructurado con viñetas y Markdown estándar.\n\n"
)

# Función centralizada para consultar OpenRouter
def consultar_agente(model_id, prompt, key, system_role, max_tokens=1500):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Consenso Deportivo Multi-IA"
    }
    
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
            timeout=90
        )
        if response.status_code != 200:
            return f"❌ Error en {model_id} ({response.status_code}): {response.text}"
            
        texto_salida = response.json()["choices"][0]["message"]["content"]
        
        # Cortafuegos para enlaces residuales de mapas
        if "http" in texto_salida.lower():
            for word in texto_salida.split():
                if "http" in word.lower():
                    texto_salida = texto_salida.replace(word, "[Dato Limpiado]")
                    
        return texto_salida
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Entrada de datos en bruto
lineas_hardrock = st.text_area("📋 Pega SOLO las líneas de Hard Rock Bet aquí:", height=150, placeholder="Ej:\nOrioles\nNationals\n-1.5 (+125)\nO 10.5 (-120)")

if st.button("🚀 Iniciar Procesamiento Multi-IA"):
    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key en la barra lateral.")
    elif not lineas_hardrock:
        st.warning("⚠️ Pega las líneas del partido para comenzar.")
    else:
        
        # DIRECTORIO DE MODELOS SOLICITADOS
        MODELO_INVESTIGADOR = "x-ai/grok-4.3"     # Grok con acceso a Web
        MODELO_ANALISTA = "google/gemini-2.5-flash-lite-preview-09-2025"     # Gemini para análisis masivo y lógica estructurada
        MODELO_VEREDICTO = "anthropic/claude-3.5-haiku" # Claude para el cierre maestro y pick definitivo

        # ---------------------------------------------------------
        # PASO 1: INVESTIGACIÓN CON GROKK (Búsqueda Web Activa)
        # ---------------------------------------------------------
        with st.spinner("🔍 1. Grok rastreando la web en tiempo real (Abridores, Clima, Bajas)..."):
            role_web = (
                "Eres el Investigador Deportivo de Élite de Grok. Tu objetivo es tomar las líneas del usuario, "
                "identificar el partido de hoy y realizar una búsqueda exhaustiva en internet. "
                "Consigue: 1) Lanzadores abridores confirmados/probables. 2) Clima exacto, velocidad del viento y tipo de estadio. "
                "3) Reporte actualizado de lesionados de última hora. Entrega un reporte crudo, detallado y libre de enlaces."
            )
            reporte_web = consultar_agente(MODELO_INVESTIGADOR, lineas_hardrock, api_key, role_web, max_tokens=2000)
            
            with st.expander("🌐 Datos Web Recuperados por Grok", expanded=True):
                st.write(reporte_web)

        # ---------------------------------------------------------
        # PASO 2: AUDITORÍA CON GEMINI (Blindaje de datos)
        # ---------------------------------------------------------
        with st.spinner("🛡️ 2. Gemini ejecutando auditoría y control de calidad..."):
            role_auditor = (
                "Eres el Auditor de Datos de Gemini. Tu función es cruzar la información web conseguida por Grok "
                "con las líneas de apuesta pegadas por el usuario. Verifica minuciosamente que los nombres correspondan, "
                "que los equipos pertenezcan a la jornada correcta y filtra cualquier dato incoherente o contradictorio. "
                "Entrega una base de datos unificada, limpia y certificada al 100%."
            )
            prompt_auditoria = f"LÍNEAS HARDROCK:\n{lineas_hardrock}\n\nDATA ENCONTRADA POR GROK:\n{reporte_web}"
            datos_verificados = consultar_agente(MODELO_ANALISTA, prompt_auditoria, api_key, role_auditor, max_tokens=1500)
            
            with st.expander("✅ Base de Datos Certificada por Gemini", expanded=True):
                st.code(datos_verificados)

        # ---------------------------------------------------------
        # PASO 3: ESPECIALISTAS EN PARALELO CON GEMINI
        # ---------------------------------------------------------
        st.subheader("📢 Análisis Especializado (Gemini 2.5 Pro)")
        col1, col2, col3 = st.columns(3)
        
        with st.spinner("Especialistas de Gemini desglosando las variables..."):
            
            # Oddsmaker
            role_odd = "Eres el Oddsmaker de Gemini. Analiza movimientos de líneas, valor en los momios y probabilidad implícita basándote SOLO en la data certificada."
            res_oddsmaker = consultar_agente(MODELO_ANALISTA, datos_verificados, api_key, role_odd, max_tokens=1200)
            
            # Scout
            role_sco = "Eres el Scout Deportivo de Gemini. Analiza los duelos directos (Matchups), poder al bate, bullpens y el impacto exacto de las bajas basándote SOLO en la data certificada."
            res_scout = consultar_agente(MODELO_ANALISTA, datos_verificados, api_key, role_sco, max_tokens=1200)
            
            # Contexto
            role_ctx = "Eres el Experto de Contexto de Gemini. Evalúa factores externos como dirección del viento, temperatura, humedad, viajes recientes y fatiga basándote SOLO en la data certificada."
            res_contexto = consultar_agente(MODELO_ANALISTA, datos_verificados, api_key, role_ctx, max_tokens=1200)

            with col1:
                st.markdown("### 📊 Mercado e Implícitas")
                st.info(res_oddsmaker)
            with col2:
                st.markdown("### ⚾ Matchup y Rotación")
                st.info(res_scout)
            with col3:
                st.markdown("### 🌤️ Clima y Factores Externos")
                st.info(res_contexto)

        st.divider()

        # ---------------------------------------------------------
        # PASO 4: TRIBUNAL Y VEREDICTO FINAL CON CLAUDE
        # ---------------------------------------------------------
        st.subheader("🏛️ Sentencia y Dictamen Final (Claude 3.5 Sonnet)")
        
        debate_acumulado = f"""
        DATA CERTIFICADA: {datos_verificados}
        ANÁLISIS ODDMAKER: {res_oddsmaker}
        ANÁLISIS SCOUT: {res_scout}
        ANÁLISIS CONTEXTO: {res_contexto}
        """

        col_jueces, col_veredicto = st.columns([1, 1])

        with st.spinner("Claude evaluando consensos y definiendo la jugada de mayor valor esperado..."):
            
            role_tribunal = (
                "Actúas como el Tribunal Arbitral de Claude. Analiza los tres informes de Gemini. "
                "Establece los puntos de acuerdo, los puntos de conflicto entre mercado y deporte, y evalúa el nivel de riesgo teórico."
            )
            votos_tribunal = consultar_agente(MODELO_VEREDICTO, debate_acumulado, api_key, role_tribunal, max_tokens=1500)
            
            role_final = (
                "Eres el Juez Supremo de Dictamen de Claude. Tu palabra es ley. Consolida los argumentos previos y emite "
                "el veredicto final con máxima precisión analítica. Es obligatorio responder estrictamente con esta estructura:\n\n"
                "- **Pick Oficial Definitivo:** [Escribe aquí el Bet / Lean / Pass]\n"
                "- **Grado de Confianza:** [Alto / Medio / Bajo]\n"
                "- **Ventaja Matemática Detectada:** [Argumento principal de valor]\n"
                "- **Umbral de Riesgo:** [Qué factor podría arruinar la jugada]"
            )
            input_veredicto = f"{debate_acumulado}\n\nDEBATE DEL TRIBUNAL CLAUDE:\n{votos_tribunal}"
            veredicto_final = consultar_agente(MODELO_VEREDICTO, input_veredicto, api_key, role_final, max_tokens=1500)

            with col_jueces:
                st.markdown("### ⚖️ Deliberación del Tribunal Arbitral")
                st.write(votos_tribunal)
                
            with col_veredicto:
                st.markdown("### 🏆 Veredicto Maestro de Claude")
                st.success(veredicto_final)
                
        st.balloons()
