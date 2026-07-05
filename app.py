import streamlit as st
import requests
import json

# 1. Configuración de pantalla y estado (Optimizado para móvil)
st.set_page_config(page_title="Coliseo de Expertos AI", layout="centered")

# Lógica para reiniciar el cuadro de texto
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

def limpiar_datos():
    st.session_state["input_text"] = ""

st.title("🏛️ El Coliseo: Consenso de 10 Agentes de IA")
st.markdown("Análisis avanzado de mercado. Procesamiento silencioso de agentes y veredicto directo.")

# 2. Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Acceso")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🧠 Roles del Panel Activos:
    * **Razonamiento:** OpenAI o1/o3, Claude 3.5 Sonnet
    * **Técnicos:** DeepSeek Coder, Codestral
    * **Open-Source:** Llama 3, Mixtral 8x22B
    * **Datos/Búsqueda:** Perplexity Sonar, Cohere Command R+
    * **Contexto/Tendencias:** Gemini 1.5 Pro, Grok 3
    """)

# 3. Función original para conectar con OpenRouter
def consultar_ia(model_id, prompt, key, system_prompt="Eres un analista experto."):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Coliseo de Expertos AI"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=90 # Tiempo extendido para modelos de razonamiento profundo
        )
        if response.status_code != 200:
            return f"❌ Error {response.status_code}: {response.text}"
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# 4. Entrada de datos del usuario vinculada al estado de reinicio
pregunta = st.text_area(
    "✍️ Introduce los datos, partidos o cuotas a analizar:", 
    value=st.session_state["input_text"],
    key="input_text",
    placeholder="Ej: Datos de abridores, líneas de Hard Rock Bet, estadísticas recientes...",
    height=150
)

# Botones alineados de forma limpia para la app móvil
col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    procesar = st.button("🚀 Iniciar Proceso de Consenso", use_container_width=True)

with col_btn2:
    st.button("🔄 Reiniciar", on_click=limpiar_datos, use_container_width=True)

# 5. Flujo de procesamiento interno (Silencioso en pantalla)
if procesar:
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not pregunta:
        st.warning("⚠️ Escribe la consulta o pega la información deportiva.")
    else:
        
        with st.spinner('🏛️ El Coliseo está debatiendo en silencio... Filtrando las mejores jugadas...'):
            
            # ==========================================
            # FASE 1: PROPUESTA E INVESTIGACIÓN DE HECHOS (Tus IDs Originales)
            # ==========================================
            res_perplexity = consultar_ia("perplexity/sonar", pregunta, api_key, "Eres el Fact-Checker. Trae datos reales, climas, estadios o lesiones de última hora e identifica hacia dónde va el público.")
            res_cohere = consultar_ia("deepseek/deepseek-v3.2", pregunta, api_key, "Eres el Administrador de Datos. Cruza las estadísticas frías sin inventar nada.")
            res_llama = consultar_ia("meta-llama/llama-3.3-70b-instruct", pregunta, api_key, "Eres el Generalista Rápido. Da una perspectiva estadística directa.")

            # ==========================================
            # FASE 2: DEBATE TÉCNICO Y CRÍTICA CRUZADA (Tus IDs Originales)
            # ==========================================
            prompt_debate = f"""
            PREGUNTA ORIGINAL DEL USUARIO: {pregunta}
            
            DATOS RECOLECTADOS POR TUS COMPAÑEROS:
            - Reporte Web (Perplexity): {res_perplexity}
            - Análisis Estadístico (Cohere): {res_cohere}
            
            Tu tarea: Analiza estos datos e identifica si la casa de apuestas (Hard Rock Bet) está moviendo la línea para atrapar al público. Busca fallos matemáticos o tendencias de última hora.
            """
            
            res_deepseek = consultar_ia("deepseek/deepseek-v3.2", prompt_debate, api_key, "Eres DeepSeek Coder. Tu fuerte es la lógica matemática pura y el cálculo de probabilidades.")
            res_codestral = consultar_ia("anthropic/claude-sonnet-4.5", prompt_debate, api_key, "Eres el Auditor Eficiente. Encuentra contradicciones numéricas entre los reportes.")
            res_grok = consultar_ia("x-ai/grok-4.3", prompt_debate, api_key, "Eres Grok 3. Analiza las tendencias de última hora y el movimiento de líneas coloquiales.")
            res_gemini = consultar_ia("~google/gemini-pro-latest", prompt_debate, api_key, "Eres Gemini. Procesa todo el contexto masivo de las respuestas previas.")

            # ==========================================
            # FASE 3: EL VEREDICTO DE LOS PESOS PESADOS (Tus IDs Originales)
            # ==========================================
            debate_completo = f"""
            PREGUNTA DEL USUARIO: {pregunta}
            
            FASE 1 (Hechos):
            Perplexity: {res_perplexity}
            Cohere: {res_cohere}
            
            FASE 2 (Debate Probabilidades):
            DeepSeek: {res_deepseek}
            Grok 3: {res_grok}
            Gemini: {res_gemini}
            """
            
            # Dejamos que Claude maneje la salida final bonita y concisa con las 2 o 3 mejores opciones
            res_claude = consultar_ia(
                "anthropic/claude-sonnet-4.5", 
                debate_completo, 
                api_key, 
                "Eres el Analista Clínico de Anthropic. Revisa los argumentos de todos, elimina contradicciones e identifica las trampas del mercado. Entrega única y estrictamente las 2 o 3 jugadas con más factor de ganar (siguiendo la corriente de la casa de apuestas). Formatea el resultado final de manera sumamente limpia, directa, estética y muy concisa para pantalla móvil usando viñetas y negritas."
            )
            
        # 6. Salida del resultado limpia e impecable
        st.write("---")
        st.subheader("🏆 Jugadas Seleccionadas con Mayor Factor de Ganar")
        st.success(res_claude)
        st.balloons()
