import streamlit as st
import requests
import json

# 1. Configuración de la interfaz de la Corte
st.set_page_config(page_title="Tribunal de Arbitraje Deportivo", layout="wide")
st.title("🏛️ La Alta Corte: Tribunal de Decantación y Valor Real (+EV)")
st.markdown("Corte Suprema Multideporte. Gemini actúa como Servidor de Evidencias; los peritos calculan y Claude dicta sentencia.")

# Barra lateral judicial
with st.sidebar:
    st.header("⚖️ Protocolo de la Corte")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 📜 Estructura del Proceso:
    1. 🔵 **Evidencia Central (Gemini):** Rastrea, verifica y almacena la data cruda.
    2. 👥 **Peritos Judiciales (Perplexity, GPT-4o, DeepSeek):** Consumen la data de Gemini para calcular el valor real.
    3. 🟠 **Magistrado Supremo (Claude 3.5):** Dictamina si hay valor o si es trampa.
    """)

# PROMPT BASE ULTRA-ESTRICTO PARA EVITAR CÁMARAS DE ECO
PROMPT_CERRADO = "Entorno judicial cerrado. Prohibido introducciones, saludos o texto de relleno. Ve directo al grano usando datos crudos y viñetas.\n\n"

def consultar_ia(model_id, prompt, key, system_role, max_tokens=1000, es_busqueda=False):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Tribunal Arbitraje Deportivo"
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
        ]
    }
    if "deepseek-r1" not in model_id:
        payload["max_tokens"] = max_tokens
        
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload), timeout=120)
        if response.status_code != 200:
            return f"❌ Error en {model_id}: {response.text}"
        data = response.json()
        if "choices" in data and data["choices"][0]["message"]["content"] is not None:
            return data["choices"][0]["message"]["content"]
        return "⚠️ Sin evidencias procesables."
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Entrada universal de la Corte (Cualquier deporte)
st.subheader("📋 Presentación de la Línea bajo Juicio")
lineas_raw = st.text_area("Pega aquí las líneas de Hard Rock Bet (Cualquier Deporte - MLB, NBA, NHL, Fútbol, etc.):", height=120, placeholder="Ejemplo:\nAstros vs Yankees\nYankees Runline -1.5 (+120)\nTotal: O/U 8.5")
datos_usuario = st.text_area("Notas adicionales o sospechas sobre la jugada (Opcional):", height=80)

if st.button("⚖️ Iniciar Juicio de Valor"):
    if not api_key or not lineas_raw:
        st.error("⚠️ Falta la API Key o la línea a juzgar.")
    else:
        # Motores Oficiales de la Corte
        GEMINI = "google/gemini-2.5-pro"
        PERPLEXITY = "perplexity/sonar"
        GPT4O = "openai/gpt-4o"
        DEEPSEEK = "deepseek/deepseek-v3.2"
        CLAUDE = "anthropic/claude-sonnet-4.5"

        bloque_entrada = f"LÍNEA BAJO ANÁLISIS:\n{lineas_raw}\n\nNOTAS EXTRA:\n{datos_usuario}"

        # =========================================================
        # FASE 1: EL ARCHIVO DE EVIDENCIAS CENTRAL (Gemini)
        # =========================================================
        st.header("🛡️ Fase 1: El Archivo de Evidencias Central (Gemini 2.5 Pro)")
        with st.spinner("Gemini ejecutando rastreo de verificación y construyendo el expediente..."):
            
            role_auditor = (
                "Actúas como el Almacén Central de Evidencias de la Corte. Identifica de qué deporte y liga son las líneas ingresadas. "
                "Busca en internet y verifica con precisión matemática absoluta para HOY lunes 25 de mayo de 2026 lo siguiente:\n"
                "1) Alineaciones confirmadas o jugadores clave del partido.\n"
                "2) Reporte oficial de lesionados o bajas de última hora.\n"
                "3) Factores climáticos, de estadio o de fatiga (como partidos en días consecutivos).\n"
                "Entrega exclusivamente los datos crudos en formato telegrama limpio. Prohibido emitir juicios o picks. Solo datos reales verificados."
            )
            expediente_gemini = consultar_ia(GEMINI, bloque_entrada, api_key, role_auditor, max_tokens=700, es_busqueda=True)
            st.code(expediente_gemini)

        st.divider()

        # =========================================================
        # FASE 2: PONENCIA DE PERITOS (Consumen la data de Gemini)
        # =========================================================
        st.header("🔮 Fase 2: Ponencia de los Peritos Judiciales (Aislamiento)")
        col1, col2, col3 = st.columns(3)
        
        # El prompt amarra a los peritos a alimentarse ÚNICAMENTE de la verdad de Gemini
        prompt_peritos = f"EXPEDIENTE DE VERIFICACIÓN (Gemini):\n{expediente_gemini}\n\nLÍNEA ORIGINAL:\n{lineas_raw}"
        
        with st.spinner("Los peritos analizan el expediente de Gemini de forma independiente..."):
            
            # Perito 1: Tendencias e Historial
            role_perp = (
                "Eres el Perito de Tendencias (Perplexity). Utiliza el Expediente de Gemini para buscar patrones históricos similares. "
                "Determina si la jugada propuesta tiene sustento en rachas o datos históricos recientes. Da tu conclusión y tu pick."
            )
            ponencia_perp = consultar_ia(PERPLEXITY, prompt_peritos, api_key, role_perp, max_tokens=450)
            
            # Perito 2: Matchup y Táctica de Terreno
            role_gpt = (
                "Eres el Perito Táctico (GPT-4o). Extrae del Expediente de Gemini el duelo directo entre los jugadores disponibles. "
                "Evalúa cómo afectan las bajas al terreno de juego y calcula qué equipo tiene la ventaja física o táctica real hoy. Define tu pick."
            )
            ponencia_gpt = consultar_ia(GPT4O, prompt_peritos, api_key, role_gpt, max_tokens=450)
            
            # Perito 3: Oddsmaker Matemático
            role_deep = (
                "Eres el Perito Matemático (DeepSeek R1). Extrae del Expediente de Gemini las variables numéricas y analízalas contra los momios de Hard Rock Bet. "
                "Calcula la probabilidad implícita. Determina con frialdad si la línea tiene valor real esperado (+EV) o si es una trampa diseñada para atrapar el dinero del público."
            )
            ponencia_deep = consultar_ia(DEEPSEEK, prompt_peritos, api_key, role_deep, max_tokens=750)
            
            with col1:
                st.markdown("### ⚫ Perito 1: Perplexity (Tendencias)")
                st.info(ponencia_perp)
            with col2:
                st.markdown("### 🛡️ Perito 2: GPT-4o (Táctica de Terreno)")
                st.info(ponencia_gpt)
            with col3:
                st.markdown("### 🧠 Perito 3: DeepSeek R1 (Valor Matemático)")
                st.info(ponencia_deep)

        st.divider()

        # =========================================================
        # FASE 3: DICTAMEN SUPREMO Y DETERMINACIÓN DE VALOR REAL
        # =========================================================
        st.subheader("🏆 Fase 3: Dictamen Supremo y Sentencia del Magistrado (Claude 3.5 Sonnet)")
        
        expediente_completo = f"""
        EVIDENCIA CERTIFICADA (Gemini): {expediente_gemini}
        PONENCIA TENDENCIAS (Perplexity): {ponencia_perp}
        PONENCIA TÁCTICA (GPT-4o): {ponencia_gpt}
        PONENCIA MATEMÁTICA (DeepSeek): {ponencia_deep}
        """
        
        with st.spinner("El Magistrado Claude sopesando el caso y decantando el valor real..."):
            role_magistrado = (
                "Eres el Magistrado Supremo de Claude 3.5 Sonnet. Tu única misión es juzgar las ponencias de los peritos y determinar el valor real (+EV) de la línea.\n\n"
                "CRITERIOS DE SENTENCIA:\n"
                "1. Si los peritos demuestran una ventaja estadística clara sobre el casino, dicta la jugada de mayor seguridad.\n"
                "2. Dictamina con precisión matemática si la jugada ingresada por el usuario tiene 'VALOR REAL' o es una 'TRAMPA DEL CASINO'.\n"
                "3. Si los datos del expediente de Gemini muestran demasiada inestabilidad o los peritos están divididos, decreta la sentencia como 'PASS / NO APRECIABLE' para proteger la banca.\n\n"
                "Entrega tu sentencia usando estrictamente este formato directo:\n"
                "- **Evaluación de la Línea:** [¿Tiene valor real (+EV) o es una trampa? Justifica en una frase corta]\n"
                "- **Pick Oficial Dictaminado:** [Línea exacta y acción aconsejada, o PASS]\n"
                "- **Grado de Fiabilidad:** [Alto / Medio / Bajo / Nulo]\n"
                "- **Sustento del Fallo:** [Argumento definitivo que unifica la táctica de terreno con la matemática de cuotas]\n"
                "- **Peligro en el Proceso:** [Qué factor o imprevisto específico del expediente pone en riesgo la inversión]"
            )
            sentencia_final = consultar_ia(CLAUDE, expediente_completo, api_key, role_magistrado, max_tokens=650)
            
            st.success(sentencia_final)
            st.balloons()
