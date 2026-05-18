import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Sistema de Decantación 5-IA", layout="wide")
st.title("🏛️ El Coliseo: Sistema de Decantación por Filtros Concéntricos")
st.markdown("Línea de producción automatizada usando las 5 mejores IAs del mercado para análisis deportivo de alta fidelidad.")

# Barra lateral con la asignación de roles
with st.sidebar:
    st.header("⚙️ Arquitectura de los 5 Pilares")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🧠 Roles Especializados:
    1. 🔍 **Perplexity Sonar:** El Investigador Web.
    2. 🛡️ **GPT-4o:** El Auditor (Limpia y unifica).
    3. 🔵 **Gemini 2.5 Pro:** El Scout Deportivo (Sabermetría).
    4. 🧠 **DeepSeek R1:** El Oddsmaker (Pensamiento matemático libre).
    5. 🟠 **Claude 3.5 Sonnet:** El Juez Supremo (Veredicto y Pick +EV).
    """)

# PROMPT BASE ULTRA-COMPRESO PARA AGENTES INTERMEDIOS
PROMPT_CERRADO = (
    "Actúa como un micro-agente analítico de entorno cerrado. Prohibido usar saludos, introducciones o texto de relleno. "
    "Ve directo al grano utilizando datos crudos y viñetas cortas. Prohibido generar enlaces o URLs.\n\n"
)

# Función centralizada de consulta modificada con bypass para DeepSeek
def consultar_ia(model_id, prompt, key, system_role, max_tokens=1000, es_busqueda=False, es_deepseek=False):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Decantacion 5-IA Deportiva"
    }
    
    # Si es Perplexity (búsqueda) o DeepSeek R1 (razonamiento), quitamos el bozal estricto
    if es_busqueda or es_deepseek:
        prompt_sistema = system_role
    else:
        prompt_sistema = PROMPT_CERRADO + system_role
    
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
            timeout=120
        )
        if response.status_code != 200:
            return f"❌ Error en {model_id}: {response.text}"
            
        data = response.json()
        
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"❌ Error devuelto por la API: {data['error']['message']}"
        else:
            return f"❌ Respuesta inesperada del servidor: {json.dumps(data)}"
            
    except Exception as e:
        return f"❌ Error de conexión en {model_id}: {str(e)}"

# Entrada de datos unificada
st.subheader("📋 Entrada de Datos del Juego")
lineas_raw = st.text_area("Pega las líneas de Hard Rock Bet aquí:", height=100, placeholder="Ej:\nYankees\nMets\n-1.5 (+165)")
datos_usuario = st.text_area("Agrega datos importantes que ya conozcas (Opcional):", height=100, placeholder="Ej: Bullpen de Mets cansado.")

if st.button("🚀 Iniciar Proceso de Decantación"):
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not lineas_raw:
        st.warning("⚠️ Introduce al menos las líneas básicas del partido.")
    else:
        
        # IDENTIFICADORES DE MODELOS ULTRA-ESTABLES
        PERPLEXITY = "perplexity/sonar"
        GPT4O = "openai/gpt-4o"
        GEMINI = "google/gemini-3.1-pro-preview"
        DEEPSEEK = "deepseek/deepseek-v3.2"
        CLAUDE = "anthropic/claude-sonnet-4.5"

        input_inicial = f"LÍNEAS HARD ROCK:\n{lineas_raw}\n\nDATOS EXTRA DEL USUARIO:\n{datos_usuario}"

        # =========================================================
        # FASE 1: ENRIQUECIMIENTO E INVESTIGACIÓN (Perplexity)
        # =========================================================
        st.header("🔍 Fase 1: Enriquecimiento e Investigación Web")
        with st.spinner("Perplexity rastreando y completando datos en tiempo real..."):
            role_perp = (
                "Eres el Investigador de Perplexity. Tu misión es buscar en internet para este juego de MLB de HOY: "
                "1) Lanzadores abridores confirmados (L/R) y estadísticas actuales. "
                "2) Clima del partido, velocidad/dirección del viento y si el estadio es abierto o cerrado. "
                "3) Reporte de bajas o lesionados de última hora. Responde solo con la data cruda, sin enlaces."
            )
            reporte_web = consultar_ia(PERPLEXITY, input_inicial, api_key, role_perp, max_tokens=600, es_busqueda=True)
            st.info(reporte_web)

        st.divider()

        # =========================================================
        # FASE 2: AUDITORÍA Y CONTROL DE CALIDAD (GPT-4o)
        # =========================================================
        st.header("🛡️ Fase 2: Auditoría y Certificación de Datos")
        with st.spinner("GPT-4o unificando y limpiando la base de datos..."):
            prompt_auditoria = f"INPUT USUARIO:\n{input_inicial}\n\nDATA ENCONTRADA EN WEB:\n{reporte_web}"
            role_gpt = (
                "Eres el Auditor de Datos de GPT-4o. Limpia el texto recibido. Cruza las líneas con la data de internet. "
                "Elimina contradicciones, comentarios insustanciales y genera una lista unificada en formato telegrama."
            )
            data_certificada = consultar_ia(GPT4O, prompt_auditoria, api_key, role_gpt, max_tokens=600)
            st.code(data_certificada)

        st.divider()

        # =========================================================
        # FASE 3: DEBATE DE ESPECIALISTAS (Gemini + DeepSeek Libre)
        # =========================================================
        st.header("📢 Fase 3: Debate de Especialistas en Paralelo")
        col_gemini, col_deepseek = st.columns(2)
        
        with st.spinner("Especialistas desglosando variables deportivas y de mercado..."):
            
            # Gemini con prompt compreso automático
            role_gemini = (
                "Eres el Analista Scout de Gemini. Procesa la data certificada. "
                "Desglosa el duelo directo abridor vs alineación, estatus de bullpens y bajas. Máximo 3 viñetas concisas."
            )
            analisis_deportivo = consultar_ia(GEMINI, data_certificada, api_key, role_gemini, max_tokens=400)
            
            # DeepSeek R1 LIBRE (es_deepseek=True activa el bypass del bozal)
            role_deepseek = (
                "Eres el Oddsmaker de DeepSeek R1. Analiza el movimiento de líneas y calcula la probabilidad implícita "
                "de los momios de Hard Rock Bet basados en la data provista. Encuentra si hay valor matemático (+EV). "
                "Muestra tu análisis y conclusiones de forma directa, sin preocuparte por límites estrictos de palabras."
            )
            analisis_mercado = consultar_ia(DEEPSEEK, data_certificada, api_key, role_deepseek, max_tokens=800, es_deepseek=True)
            
            with col_gemini:
                st.markdown("### 🔵 Gemini: Análisis Deportivo y Sabermetría")
                st.info(analisis_deportivo)
            with col_deepseek:
                st.markdown("### 🧠 DeepSeek R1: Análisis Matemático de Mercado")
                st.info(analisis_mercado)

        st.divider()

        # =========================================================
        # FASE 4: DECANTACIÓN Y SENTENCIA FINAL (Claude 3.5 Sonnet)
        # =========================================================
        st.subheader("🏆 Fase 4: Sentencia del Jurado Supremo (Claude 3.5 Sonnet)")
        
        bloque_final = f"""
        BASE DE DATOS CERTIFICADA: {data_certificada}
        INFORME DEPORTIVO (Gemini): {analisis_deportivo}
        INFORME DE MERCADO (DeepSeek): {analisis_mercado}
        """
        
        with st.spinner("Claude pesando los informes y decantando la mejor jugada..."):
            role_juezo = (
                "Eres el Juez Supremo de Claude 3.5 Sonnet. Recibes la data limpia, el análisis deportivo y el análisis de mercado de DeepSeek. "
                "Tu objetivo es decantar todo este flujo, encontrar el punto de máximo valor esperado (+EV) y dictaminar la jugada. "
                "Responde con rigurosidad estadística utilizando estrictamente esta estructura directa:\n\n"
                "- **Pick Oficial:** [Línea exacta de Hard Rock Bet y acción]\n"
                "- **Confianza:** [Alto / Medio / Bajo]\n"
                "- **Ventaja (+EV):** [Razón matemática y de terreno clave en una frase]\n"
                "- **Protocolo de Riesgo:** [Qué factor específico e imprevisto tumba la jugada]"
            )
            veredicto_supremo = consultar_ia(CLAUDE, bloque_final, api_key, role_juezo, max_tokens=600)
            
            st.success(veredicto_supremo)
            st.balloons()
