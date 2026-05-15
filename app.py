import streamlit as st
import requests
import json

# 1. Configuración de pantalla ancha
st.set_page_config(page_title="Coliseo de Expertos AI", layout="wide")
st.title("🏛️ El Coliseo: Consenso de 10 Agentes de IA")
st.markdown("Flujo avanzado de Propuesta, Debate de Especialistas y Veredicto Final Decantado.")

# 2. Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Acceso")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🧠 Roles del Panel:
    * **Razonamiento:** OpenAI o1/o3, Claude 3.5 Sonnet
    * **Técnicos:** DeepSeek Coder, Codestral
    * **Open-Source:** Llama 3, Mixtral 8x22B
    * **Datos/Búsqueda:** Perplexity Sonar, Cohere Command R+
    * **Contexto/Tendencias:** Gemini 1.5 Pro, Grok 3
    """)

# 3. Función optimizada para conectar con OpenRouter
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

# 4. Entrada de datos del usuario
pregunta = st.text_area("✍️ Introduce los datos, partidos o cuotas a analizar:", placeholder="Ej: Datos de abridores, líneas de Hard Rock Bet, estadísticas recientes...")

if st.button("🚀 Iniciar Proceso de Consenso"):
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not pregunta:
        st.warning("⚠️ Escribe la consulta o pega la información deportiva.")
    else:
        
        # ==========================================
        # FASE 1: PROPUESTA E INVESTIGACIÓN DE HECHOS
        # ==========================================
        st.header("📋 Fase 1: Investigación de Hechos e Hipótesis")
        
        # Aquí elegimos a los especialistas en traer datos frescos y balanceados
        col1, col2, col3 = st.columns(3)
        
        with st.spinner('Perplexity investiga la web, Cohere y Llama analizan...'):
            # Usamos IDs estándar y compatibles de OpenRouter
            res_perplexity = consultar_ia("perplexity/sonar-pro-search", pregunta, api_key, "Eres el Fact-Checker. Trae datos reales, climas, estadios o lesiones de última hora.")
            res_cohere = consultar_ia("cohere/command-a", pregunta, api_key, "Eres el Administrador de Datos. Cruza las estadísticas frías sin inventar nada.")
            res_llama = consultar_ia("meta-llama/llama-3-70b-instruct", pregunta, api_key, "Eres el Generalista Rápido. Da una perspectiva estadística directa.")

            with col1:
                st.markdown("### 🔍 Perplexity (Fact-Checking)")
                st.info(res_perplexity)
            with col2:
                st.markdown("### 📊 Cohere Command R+")
                st.info(res_cohere)
            with col3:
                st.markdown("### 🦙 Llama 3 (Perspectiva)")
                st.info(res_llama)

        st.divider()

        # ==========================================
        # FASE 2: DEBATE TÉCNICO Y CRÍTICA CRUZADA
        # ==========================================
        st.header("💻 Fase 2: Filtro Técnico y Tendencias (Debate)")
        
        # Pasamos la información recolectada en la Fase 1 a los matemáticos y analistas de tendencias
        prompt_debate = f"""
        PREGUNTA ORIGINAL DEL USUARIO: {pregunta}
        
        DATOS RECOLECTADOS POR TUS COMPAÑEROS:
        - Reporte Web (Perplexity): {res_perplexity}
        - Análisis Estadístico (Cohere): {res_cohere}
        
        Tu tarea: Analiza estos datos. Si eres DeepSeek/Codestral, busca fallos matemáticos o de lógica en las probabilidades. Si eres Grok/Mixtral/Gemini, evalúa tendencias de última hora y el comportamiento de las líneas. Ofrece tu crítica.
        """
        
        col4, col5, col6, col7 = st.columns(4)
        
        with st.spinner('Los matemáticos y analistas debaten las probabilidades...'):
            res_deepseek = consultar_ia("deepseek/deepseek-chat", prompt_debate, api_key, "Eres DeepSeek Coder. Tu fuerte es la lógica matemática pura y el cálculo de probabilidades.")
            res_codestral = consultar_ia("mistralai/codestral-22b-", prompt_debate, api_key, "Eres el Auditor Eficiente. Encuentra contradicciones numéricas entre los reportes.")
            res_grok = consultar_ia("x-ai/grok-3", prompt_debate, api_key, "Eres Grok 3. Analiza las tendencias de última hora y el movimiento de líneas coloquiales.")
            res_gemini = consultar_ia("google/gemini-pro-1.5", prompt_debate, api_key, "Eres Gemini. Procesa todo el contexto masivo de las respuestas previas.")

            with col4:
                st.markdown("### 📐 DeepSeek (Matemático)")
                st.write(res_deepseek)
            with col5:
                st.markdown("### 🧮 Codestral (Auditor)")
                st.write(res_codestral)
            with col6:
                st.markdown("### ⚫ Grok 3 (Tendencias)")
                st.write(res_grok)
            with col7:
                st.markdown("### 🔵 Gemini 1.5 Pro (Contexto)")
                st.write(res_gemini)

        st.divider()

        # ==========================================
        # FASE 3: EL VEREDICTO DE LOS PESOS PESADOS
        # ==========================================
        st.header("🏆 Fase 3: Veredicto de los Pesos Pesados")
        
        # Recolectamos absolutamente TODO el hilo de la conversación
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
        
        col_juez1, col_juez2 = st.columns(2)
        
        with st.spinner('Los Jueces Finales (Modelos de Razonamiento) están dictaminando...'):
            # OpenAI o1/o3 o Claude 3.5 Sonnet actúan como el tribunal supremo
            res_openai_o = consultar_ia("openai/o1-mini", debate_completo, api_key, "Eres el Pensador Profundo de OpenAI. Tu fortaleza es la lógica estricta. Dictamina el pick con mayor valor real.")
            res_claude = consultar_ia("anthropic/claude-3.5-sonnet", debate_completo, api_key, "Eres el Analista Clínico de Anthropic. Revisa los argumentos de todos, elimina contradicciones y redacta la conclusión definitiva de forma estructurada.")
            
            with col_juez1:
                st.markdown("### 🧠 OpenAI o1-mini (Lógica Pura)")
                st.success(res_openai_o)
            with col_juez2:
                st.markdown("### 🟠 Claude 3.5 Sonnet (Editor Jefe)")
                st.success(res_claude)
                
        # Consenso definitivo unificado
        st.balloons()
