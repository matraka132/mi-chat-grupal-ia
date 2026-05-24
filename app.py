import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Comité Multideporte 5-IA", layout="wide")
st.title("🏛️ El Coliseo: Súper-Comité de 5 Predicciones (MLB & NBA)")
st.markdown("Fase 1: Auditoría de Gemini | Fase 2: 5 Predicciones Ciegas de Élite | Fase 3: Veredicto de Máxima Seguridad")

# Barra lateral
with st.sidebar:
    st.header("⚙️ Configuración del Pleno")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🗳️ Los 5 Votos del Comité:
    * 🔵 **Gemini 2.5 Pro** (Auditor y Scout)
    * ⚫ **Perplexity Sonar** (Tendencias)
    * 🛡️ **GPT-4o** (Matchup / Rotaciones)
    * 🧠 **DeepSeek R1** (Lógica de Mercado)
    * 🟠 **Claude 3.5 Sonnet** (Juez y Votante)
    """)

# PROMPT BASE ULTRA-COMPRESO
PROMPT_CERRADO = "Actúa en un entorno cerrado. Ve directo al grano utilizando datos crudos y viñetas cortas. Prohibido introducciones, saludos o relleno.\n\n"

def consultar_ia(model_id, prompt, key, system_role, max_tokens=1000, es_busqueda=False):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Gran Comite Multideporte"
    }
    
    if es_busqueda or "deepseek-r1" in model_id:
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
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload), timeout=120)
        if response.status_code != 200:
            return f"❌ Error en {model_id}: {response.text}"
        data = response.json()
        if "choices" in data and data["choices"][0]["message"]["content"] is not None:
            return data["choices"][0]["message"]["content"]
        return "⚠️ Sin respuesta/Procesado internamente."
    except Exception as e:
        return f"❌ Error de conexión en {model_id}: {str(e)}"

# Entrada de datos unificada
st.subheader("📋 Datos Iniciales de Hard Rock Bet (MLB o NBA)")
lineas_raw = st.text_area("Pega las líneas aquí:", height=120, placeholder="Ej. NBA:\nLakers\nCeltics\nSpread: Celtics -5.5\nTotal: O/U 224.5\n\nEj. MLB:\nYankees\nMets\n-1.5 (+165)")
datos_usuario = st.text_area("Notas o datos adicionales conocidos (Ej. Jugadores descartados, cansancio, etc.):", height=80)

if st.button("🚀 Iniciar Pleno de 5 Predicciones Multideporte"):
    if not api_key or not lineas_raw:
        st.error("⚠️ Verifica la API Key y las líneas del partido.")
    else:
        # Los 5 Motores Oficiales
        GEMINI = "google/gemini-3.1-flash-lite"
        PERPLEXITY = "perplexity/sonar"
        GPT4O = "openai/gpt-4o"
        DEEPSEEK = "deepseek/deepseek-v3.2"
        CLAUDE = "anthropic/claude-sonnet-4.5"

        bloque_entrada = f"PARTIDO:\n{lineas_raw}\n\nNOTAS EXTRA:\n{datos_usuario}"

        # =========================================================
        # FASE 1: AUDITORÍA DE DATOS DE TERRENO (Gemini 2.5 Pro)
        # =========================================================
        st.header("🛡️ Fase 1: Certificación y Filtro de Datos (Gemini)")
        with st.spinner("Gemini detectando deporte y escaneando internet..."):
            
            role_auditor = (
                "Eres el Senior Auditor de Gemini. Tu función es identificar si el partido ingresado es de MLB o de NBA y buscar en la web los datos reales de HOY.\n\n"
                "SI ES MLB, extrae estrictamente: 1) Lanzadores abridores confirmados (Mano, ERA). 2) Clima, viento y estadio. 3) Lesionados.\n"
                "SI ES NBA, extrae estrictamente: 1) Reporte oficial de lesionados de última hora (Confirmados OUT, Questionable o Probable). 2) Rendimiento reciente (Racha en los últimos 5 juegos y si es el segundo juego de un Back-to-Back). 3) Eficiencia ofensiva/defensiva de ambos equipos.\n\n"
                "Genera una base de datos 100% verídica en formato telegrama conciso. Cero especulaciones, cero relleno, solo datos fríos."
            )
            data_certificada = consultar_ia(GEMINI, bloque_entrada, api_key, role_auditor, max_tokens=650, es_busqueda=True)
            st.code(data_certificada)

        st.divider()

        # =========================================================
        # FASE 2: PREDICCIONES SIMULTÁNEAS EN PARALELO (Las 5 IAs)
        # =========================================================
        st.header("🔮 Fase 2: Las 5 Predicciones del Comité")
        
        prompt_analisis = f"DATA CERTIFICADA DE HOY:\n{data_certificada}\n\nLÍNEAS EN HARD ROCK BET:\n{lineas_raw}"
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with st.spinner("El pleno de las 5 IAs calculando sus picks de forma aislada..."):
            
            # 1. Predicción de Gemini
            role_gem_pred = "Eres el Analista Scout de Gemini. Estudia la data y las líneas. Genera tu predicción directa del partido indicando la ventaja de las rotaciones/abridores y tu pick propuesto."
            prediccion_gemini = consultar_ia(GEMINI, prompt_analisis, api_key, role_gem_pred, max_tokens=450)
            
            # 2. Predicción de Perplexity
            role_perp = "Eres el Analista de Tendencias (Perplexity). Estudia la data certificada y las líneas. Genera una predicción corta indicando qué lado tiene valor histórico o tendencia a favor y tu pick."
            prediccion_perp = consultar_ia(PERPLEXITY, prompt_analisis, api_key, role_perp, max_tokens=450)
            
            # 3. Predicción de GPT-4o
            role_gpt = "Eres el Analista de Matchups (GPT-4o). Analiza el emparejamiento directo entre plantillas (Abridor vs Bateadores en MLB, o Quinteto titular/Banca en NBA) basándote en la data certificada. Da tu pick."
            prediccion_gpt = consultar_ia(GPT4O, prompt_analisis, api_key, role_gpt, max_tokens=450)
            
            # 4. Predicción de DeepSeek R1
            role_deep = "Eres el Oddsmaker de DeepSeek R1. Analiza el valor matemático de las cuotas de Hard Rock Bet (Moneylines, Spreads o Totales) contra la data certificada. Calcula probabilidad implícita y da tu pick definitivo."
            prediccion_deep = consultar_ia(DEEPSEEK, prompt_analisis, api_key, role_deep, max_tokens=700)
            
            # 5. Predicción de Claude 3.5 Sonnet
            role_claude_pred = "Eres el Analista de Contexto de Claude. Evalúa la data y define cuál es la jugada más sensata, estable y de menor riesgo según las variables del juego. Entrega tu pick en una frase."
            prediccion_claude = consultar_ia(CLAUDE, prompt_analisis, api_key, role_claude_pred, max_tokens=450)
            
            with col1:
                st.markdown("### 🔵 Gemini")
                st.info(prediccion_gemini)
            with col2:
                st.markdown("### ⚫ Perplexity")
                st.info(prediccion_perp)
            with col3:
                st.markdown("### 🛡️ GPT-4o")
                st.info(prediccion_gpt)
            with col4:
                st.markdown("### 🧠 DeepSeek R1")
                st.info(prediccion_deep)
            with col5:
                st.markdown("### 🟠 Claude 3.5")
                st.info(prediccion_claude)

        st.divider()

        # =========================================================
        # FASE 3: CONSENSO TOTAL Y JUGADAS MÁS SEGURAS
        # =========================================================
        st.subheader("🏆 Fase 3: Consenso Judicial y Selección de Jugadas Seguras")
        
        bloque_consenso = f"""
        DATA CERTIFICADA DE ORIGEN: {data_certificada}
        VOTO 1 (Gemini): {prediccion_gemini}
        VOTO 2 (Perplexity): {prediccion_perp}
        VOTO 3 (GPT-4o): {prediccion_gpt}
        VOTO 4 (DeepSeek): {prediccion_deep}
        VOTO 5 (Claude): {prediccion_claude}
        """
        
        with st.spinner("Claude unificando el pleno y calculando las apuestas de mayor fiabilidad..."):
            role_juez = (
                "Eres el Juez Supremo del Consenso de Claude 3.5 Sonnet. Tu objetivo es recibir las 5 predicciones del comité e identificar las jugadas más seguras del mercado (sin importar si es MLB o NBA).\n\n"
                "REGLAS:\n"
                "1. Si 3 o más IAs coinciden plenamente en un pick (sea el ganador, el spread de puntos o el Over/Under), esa es la Jugada Principal de alta fiabilidad.\n"
                "2. Si hay una división total de opiniones, debes decretar PASS/NO BET debido a alta volatilidad.\n"
                "3. Ignora textos de relleno e introducciones.\n\n"
                "Responde estrictamente con esta estructura limpia:\n"
                "- **Recuento de Votos:** [Menciona de forma directa qué pick propuso cada una de las 5 IAs]\n"
                "- **Jugada Más Segura del Día:** [Línea exacta de Hard Rock Bet y acción recomendada]\n"
                "- **Grado de Consenso:** [Unanimidad (5/5) / Mayoría Fuerte (4/5) / Mayoría Simple (3/5) / Sin Consenso (PASS)]\n"
                "- **Sustento del Dictamen:** [La razón técnica, táctica y matemática por la cual esta selección es la más sólida]\n"
                "- **Alerta de Peligro:** [Qué factor o imprevisto específico (clima en MLB o ausencias de última hora en NBA) podría tumbar la jugada]"
            )
            veredicto_final = consultar_ia(CLAUDE, bloque_consenso, api_key, role_juez, max_tokens=650)
            
            st.success(veredicto_final)
            st.balloons()
