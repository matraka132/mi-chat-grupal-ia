import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Consenso Deportivo Cerrado", layout="wide")
st.title("🏛️ Sistema de Consenso Deportivo de 5 Agentes")
st.markdown("Basado estrictamente en datos de entrada del usuario | Ambiente Cerrado")

# Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🛡️ Flujo Secuencial:
    1. **Agente Normalizador** (Estructura JSON)
    2. **Agente Oddsmaker** (Mercado y Cuotas)
    3. **Agente Scout** (Matchup y Lesiones)
    4. **Agente de Contexto** (Clima y Estadio)
    5. **Tribunal de Consenso** (Juez Con, Agr, Est)
    6. **Veredicto Final** (Pick Oficial)
    """)

# PROMPT BASE CRÍTICO (Tu regla de oro)
PROMPT_BASE = (
    "Eres un agente en un ambiente cerrado. Prohibido usar conocimiento externo. "
    "Tu única fuente de verdad son los datos proporcionados en el texto. Si falta información, "
    "decláralo explícitamente. Debes citar variables específicas del texto para justificar tu análisis.\n\n"
)

# Función centralizada para consultar OpenRouter con control de tokens
def consultar_agente(model_id, prompt, key, system_role, max_tokens=1500):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Consenso Deportivo Cerrado"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": PROMPT_BASE + system_role},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens # ESTA LÍNEA ARREGLA EL ERROR 402 limiting the collateral required
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )
        if response.status_code != 200:
            return f"❌ Error {response.status_code}: {response.text}"
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Entrada de datos en bruto
datos_brutos = st.text_area("📋 Pega las líneas de Hard Rock Bet, Clima, Lanzadores y Lesiones aquí:", height=200, placeholder="Ej: Orioles vs Nationals, líneas, abridores, clima...")

if st.button("🚀 Ejecutar Consenso Multilateral"):
    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key en la barra lateral.")
    elif not datos_brutos:
        st.warning("⚠️ El campo de datos está vacío.")
    else:
        
        # MODELO ELEGIDO PARA EL PROCESO
        MODELO_CORE = "anthropic/claude-opus-4.7-fast"
        # MODELO DE RAZONAMIENTO PARA EL TRIBUNAL
        MODELO_JUEZ = "openai/o4-mini-deep-research"

        # ---------------------------------------------------------
        # AGENTE 1: NORMALIZADOR
        # ---------------------------------------------------------
        with st.spinner("1. Agente Normalizador estructurando datos..."):
            role_1 = "Tu función es estructurar datos de entrada en un formato claro o JSON estandarizado. Extrae líneas, alineaciones, clima y estadio. No analices, solo organiza."
            datos_estructurados = consultar_agente(MODELO_CORE, datos_brutos, api_key, role_1, max_tokens=1000)
            
            with st.expander("✅ Datos Estandarizados (Agente Normalizador)", expanded=True):
                st.code(datos_estructurados)

        # ---------------------------------------------------------
        # AGENTES 2, 3 Y 4: ANÁLISIS EN PARALELO
        # ---------------------------------------------------------
        st.subheader("📢 Análisis de los Especialistas (Ambiente Cerrado)")
        col1, col2, col3 = st.columns(3)
        
        with st.spinner("Especialistas analizando los datos normalizados..."):
            
            # Agente 2: Oddsmaker
            role_2 = "Tu función es analizar movimientos de líneas, cuotas y calcular la probabilidad implícita. Detecta desbalances de valor."
            res_oddsmaker = consultar_agente(MODELO_CORE, datos_estructurados, api_key, role_2, max_tokens=1200)
            
            # Agente 3: Scout
            role_3 = "Tu función es evaluar el matchup deportivo puro, impacto de alineaciones, efecto de lesiones e índice de fuerza."
            res_scout = consultar_agente(MODELO_CORE, datos_estructurados, api_key, role_3, max_tokens=1200)
            
            # Agente 4: Contexto
            role_4 = "Tu función es evaluar factores exógenos: impacto del clima, condiciones del estadio, fatiga y descanso reportado."
            res_contexto = consultar_agente(MODELO_CORE, datos_estructurados, api_key, role_4, max_tokens=1200)

            with col1:
                st.markdown("### 📊 2. Agente Oddsmaker")
                st.info(res_oddsmaker)
            with col2:
                st.markdown("### ⚾ 3. Agente Scout")
                st.info(res_scout)
            with col3:
                st.markdown("### 🌤️ 4. Agente de Contexto")
                st.info(res_contexto)

        st.divider()

        # ---------------------------------------------------------
        # FASE 5: TRIBUNAL DE CONSENSO Y VEREDICTO FINAL
        # ---------------------------------------------------------
        st.subheader("🏛️ 5. Tribunal de Consenso y Dictamen")
        
        debate_acumulado = f"""
        DATOS REALES DEL PARTIDO: {datos_estructurados}
        ANÁLISIS MERCADO (Oddsmaker): {res_oddsmaker}
        ANÁLISIS DEPORTIVO (Scout): {res_scout}
        ANÁLISIS ENTORNO (Contexto): {res_contexto}
        """

        col_jueces, col_veredicto = st.columns([1, 1])

        with st.spinner("Tribunal deliberando y Agente Final decantando..."):
            
            # Simulación del Tribunal Interno (Juez Conservador, Agresivo y Estadístico votando)
            role_tribunal = (
                "Actúa como un Tribunal de 3 Jueces Internos (Juez Conservador: busca la menor exposición al riesgo; "
                "Juez Agresivo: busca cuotas altas con valor esperado positivo; Juez Estadístico: se apega a las probabilidades frías). "
                "Presenta el debate resumido de los tres jueces basándote en los reportes previos."
            )
            votos_tribunal = consultar_agente(MODELO_JUEZ, debate_acumulado, api_key, role_tribunal, max_tokens=1500)
            
            # Agente Final: Veredicto
            role_final = (
                "Eres el Agente Final de Veredicto. Tu función es consolidar absolutamente todos los análisis previos. "
                "Debes entregar de forma obligatoria el siguiente formato:\n"
                "- **Pick Oficial** (Bet / Lean / Pass)\n"
                "- **Grado de Confianza** (Alto / Medio / Bajo)\n"
                "- **Justificación Clave** (Basada solo en los datos proporcionados)\n"
                "- **Riesgos Principales**"
            )
            input_veredicto = f"{debate_acumulado}\n\nDEBATE DEL TRIBUNAL:\n{votos_tribunal}"
            veredicto_final = consultar_agente(MODELO_CORE, input_veredicto, api_key, role_final, max_tokens=1500)

            with col_jueces:
                st.markdown("### ⚖️ Deliberación del Tribunal (o1-mini)")
                st.write(votos_tribunal)
                
            with col_veredicto:
                st.markdown("### 🏆 Veredicto Final Decantado")
                st.success(veredicto_final)
                
        st.balloons()
