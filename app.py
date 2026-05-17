import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Consenso Automatizado", layout="wide")
st.title("🏛️ Consenso Deportivo v3: Búsqueda y Auditoría Automática")
st.markdown("Pega solo las líneas de Hard Rock Bet. El sistema buscará el clima, abridores y lesiones, y los auditará antes del debate.")

# Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🔄 Flujo de Automatización:
    1. **Agente Investigador** (Busca clima, abridores y bajas en la Web)
    2. **Agente Auditor** (Cruza y rectifica datos para evitar alucinaciones)
    3. **Especialistas en Paralelo** (Oddsmaker, Scout, Contexto)
    4. **Tribunal Interno y Veredicto** (DeepSeek R1 y GPT-4o)
    """)

# PROMPT BASE CRÍTICO CON REGLA DE NO LINKS
PROMPT_BASE = (
    "Eres un agente en un ambiente cerrado. Prohibido usar conocimiento previo que no esté en el texto de entrada "
    "o en los datos web recuperados por el investigador. Si falta información crucial, decláralo explícitamente.\n"
    "CRÍTICO: Está estrictamente prohibido generar enlaces, hipervínculos o URLs (como enlaces de Google Maps o OpenAI). "
    "Entrega tu análisis únicamente en texto plano estructurado con Markdown estándar.\n\n"
)

# Función centralizada para consultar OpenRouter con filtro de salida
def consultar_agente(model_id, prompt, key, system_role, max_tokens=1500):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Consenso Deportivo Automatizado"
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
            return f"❌ Error {response.status_code}: {response.text}"
            
        texto_salida = response.json()["choices"][0]["message"]["content"]
        
        # Filtro de seguridad por si la IA ignora la instrucción y mete links de mapas
        if "(https://www.google.com/maps" in texto_salida:
            texto_salida = texto_salida.split("(https://www.google.com/maps")[0] + "\n\n*[Nota: Enlace de mapa truncado por seguridad del script]*"
            
        return texto_salida
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Entrada de datos en bruto (Solo las líneas)
lineas_hardrock = st.text_area("📋 Pega SOLO las líneas de Hard Rock Bet aquí (1 hora antes del juego):", height=150, placeholder="Ej:\nOrioles\nNationals\n-1.5 (+125)\nO 10.5 (-120)")

if st.button("🚀 Iniciar Búsqueda y Consenso"):
    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key en la barra lateral.")
    elif not lineas_hardrock:
        st.warning("⚠️ Pega las líneas del partido para poder trabajar.")
    else:
        
        # Modelos bandera estables
        MODELO_CORE = "openai/gpt-4o-mini"
        MODELO_WEB = "perplexity/sonar"
        MODELO_JUEZ = "deepseek/deepseek-v4-pro"

        # ---------------------------------------------------------
        # PASO 1: AGENTE INVESTIGADOR (Búsqueda Web en Tiempo Real)
        # ---------------------------------------------------------
        with st.spinner("🔍 1. Agente Investigador rastreando abridores, clima y lesiones en la web..."):
            role_web = (
                "Eres un Investigador Deportivo Avanzado con acceso a internet. Tu objetivo es tomar las líneas de apuesta "
                "provistas por el usuario, identificar qué equipos juegan hoy domingo 17 de mayo de 2026, y buscar en la web: "
                "1) Lanzadores abridores confirmados. 2) Clima exacto a la hora del juego y condiciones del estadio. "
                "3) Reporte de lesiones o bajas de última hora para ambos equipos. Entrega un reporte limpio y detallado sin incluir URLs."
            )
            reporte_web = consultar_agente(MODELO_WEB, lineas_hardrock, api_key, role_web, max_tokens=2000)
            
            with st.expander("🌐 Reporte Encontrado en la Web (Perplexity)", expanded=True):
                st.write(reporte_web)

        # ---------------------------------------------------------
        # PASO 2: AGENTE AUDITOR (Rectificación de Datos)
        # ---------------------------------------------------------
        with st.spinner("🛡️ 2. Agente Auditor rectificando y blindando los datos..."):
            role_auditor = (
                "Eres el Auditor y Filtro de Seguridad. Tu trabajo es analizar el reporte web traído por el investigador "
                "y cruzarlo con las líneas de Hard Rock Bet provistas por el usuario. "
                "Verifica que los lanzadores realmente correspondan a los equipos, que el clima sea lógico para la ubicación del estadio "
                "y que no haya contradicciones o datos inventados. Genera una lista estandarizada limpia y 100% VERIFICADA. No incluyas enlaces."
            )
            prompt_auditoria = f"LÍNEAS DEL USUARIO:\n{lineas_hardrock}\n\nREPORTE WEB A AUDITAR:\n{reporte_web}"
            datos_verificados = consultar_agente(MODELO_CORE, prompt_auditoria, api_key, role_auditor, max_tokens=1500)
            
            with st.expander("✅ Datos Finales Auditados y Rectificados", expanded=True):
                st.code(datos_verificados)

        # ---------------------------------------------------------
        # PASO 3: DEBATE DE ESPECIALISTAS (Ambiente Cerrado sobre datos auditados)
        # ---------------------------------------------------------
        st.subheader("📢 Análisis de los Especialistas")
        col1, col2, col3 = st.columns(3)
        
        with st.spinner("Especialistas evaluando el escenario auditado..."):
            
            # Agente Oddsmaker
            role_2 = "Tu función es analizar movimientos de líneas, cuotas y calcular la probabilidad implícita basándote SOLO en los datos auditados. No generes enlaces."
            res_oddsmaker = consultar_agente(MODELO_CORE, datos_verificados, api_key, role_2, max_tokens=1200)
            
            # Agente Scout
            role_3 = "Tu función es evaluar el matchup deportivo puro, impacto de alineaciones y efecto de lesiones basándote SOLO en los datos auditados. No generes enlaces."
            res_scout = consultar_agente(MODELO_CORE, datos_verificados, api_key, role_3, max_tokens=1200)
            
            # Agente Contexto
            role_4 = "Tu función es evaluar factores exógenos: impacto del clima, condiciones del estadio, fatiga y descanso basándote SOLO en los datos auditados. No generes enlaces."
            res_contexto = consultar_agente(MODELO_CORE, datos_verificados, api_key, role_4, max_tokens=1200)

            with col1:
                st.markdown("### 📊 Agente Oddsmaker")
                st.info(res_oddsmaker)
            with col2:
                st.markdown("### ⚾ Agente Scout")
                st.info(res_scout)
            with col3:
                st.markdown("### 🌤️ Agente de Contexto")
                st.info(res_contexto)

        st.divider()

        # ---------------------------------------------------------
        # PASO 4: TRIBUNAL DE CONSENSO Y DICTAMEN FINAL
        # ---------------------------------------------------------
        st.subheader("🏛️ Tribunal de Consenso y Dictamen")
        
        debate_acumulado = f"""
        DATOS AUDITADOS: {datos_verificados}
        ANÁLISIS MERCADO: {res_oddsmaker}
        ANÁLISIS DEPORTIVO: {res_scout}
        ANÁLISIS ENTORNO: {res_contexto}
        """

        col_jueces, col_veredicto = st.columns([1, 1])

        with st.spinner("Tribunal deliberando y emitiendo Pick Oficial..."):
            
            role_tribunal = (
                "Actúa como un Tribunal de 3 Jueces Internos (Juez Conservador, Juez Agresivo y Juez Estadístico). "
                "Presenta el debate resumido de los tres jueces analizando los riesgos y el valor esperado basándote en los reportes previos. No pongas enlaces."
            )
            votos_tribunal = consultar_agente(MODELO_JUEZ, debate_acumulado, api_key, role_tribunal, max_tokens=1500)
            
            role_final = (
                "Eres el Agente Final de Veredicto. Consolida los análisis previos y el debate del tribunal. "
                "Entrega obligatoriamente este formato sin incluir links externos:\n"
                "- **Pick Oficial** (Bet / Lean / Pass)\n"
                "- **Grado de Confianza** (Alto / Medio / Bajo)\n"
                "- **Justificación Clave**\n"
                "- **Riesgos Principales**"
            )
            input_veredicto = f"{debate_acumulado}\n\nDEBATE DEL TRIBUNAL:\n{votos_tribunal}"
            veredicto_final = consultar_agente(MODELO_CORE, input_veredicto, api_key, role_final, max_tokens=1500)

            with col_jueces:
                st.markdown("### ⚖️ Deliberación del Tribunal (DeepSeek R1)")
                st.write(votos_tribunal)
                
            with col_veredicto:
                st.markdown("### 🏆 Veredicto Final Decantado")
                st.success(veredicto_final)
                
        st.balloons()
