import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Sistema de Decantación Blindado", layout="wide")
st.title("🏛️ El Coliseo: Decantación por Aislamiento de 5 Vías")
st.markdown("Filtros ciegos e independientes para destruir la cámara de eco y erradicar fallos en cadena.")

# Barra lateral
with st.sidebar:
    st.header("⚙️ Configuración Antisurco")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🛡️ Protocolo de Aislamiento:
    * ⛔ **Cero contaminación:** Las IAs no ven las respuestas de las otras.
    * 🔍 **Tres ojos en la Web:** Perplexity, Gemini y GPT-4o buscan por separado.
    * ⚖️ **Filtro de Contradicciones:** Claude castiga los datos que no cuadran.
    """)

# PROMPT BASE ULTRA-COMPRESO
PROMPT_CERRADO = "Ve directo al grano utilizando datos crudos y viñetas cortas. Prohibido introducciones, saludos o relleno.\n\n"

def consultar_ia(model_id, prompt, key, system_role, max_tokens=1000, es_busqueda=False):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Decantacion Blindada"
    }
    
    prompt_sistema = system_role if es_busqueda else (PROMPT_CERRADO + system_role)
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt}
        ]
    }
    if "o1-" not in model_id:
        payload["max_tokens"] = max_tokens
        
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload), timeout=120)
        if response.status_code != 200:
            return f"❌ Error: {response.text}"
        data = response.json()
        if "choices" in data and data["choices"][0]["message"]["content"] is not None:
            return data["choices"][0]["message"]["content"]
        return "⚠️ Sin datos provistos."
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Entrada de datos unificada
st.subheader("📋 Datos Originales de Hard Rock Bet")
lineas_raw = st.text_area("Pega las líneas aquí:", height=100, placeholder="Ej:\nYankees\nMets\n-1.5 (+165)")
datos_usuario = st.text_area("Notas extras (Opcional):", height=80)

if st.button("🚀 Ejecutar Decantación Blindada"):
    if not api_key or not lineas_raw:
        st.error("⚠️ Verifica la API Key y las líneas del partido.")
    else:
        # Motores oficiales
         PERPLEXITY = "perplexity/sonar"
       GPT4O = "openai/gpt-4o"
        GEMINI = "google/gemini-3.1-flash-lite"
        O1_MINI = "deepseek/deepseek-v3.2"
        CLAUDE = "anthropic/claude-sonnet-4.5"

        bloque_entrada = f"PARTIDO E INSTRUCCIÓN:\n{lineas_raw}\n\nNOTAS USER:\n{datos_usuario}"

        # =========================================================
        # FASE 1: INVESTIGACIÓN CIEGA SIMULTÁNEA
        # =========================================================
        st.header("🔍 Fase 1: Rastreo en la Web (Completamente Aislado)")
        col1, col2, col3 = st.columns(3)
        
        with st.spinner("Buscando datos de forma independiente..."):
            
            # Cada IA busca en internet partiendo ÚNICAMENTE del input original
            role_perp = "Eres Perplexity. Busca en la web los abridores de hoy para este juego de MLB, el estado del bullpen tras ayer y el viento/clima exacto. Formato corto."
            reporte_perp = consultar_ia(PERPLEXITY, bloque_entrada, api_key, role_perp, max_tokens=500, es_busqueda=True)
            
            role_gemini = "Eres Gemini. Usa tu acceso web para verificar de forma independiente los lanzadores abridores confirmados, sus efectividades este año y las bajas de último minuto para este juego. Sé estricto."
            reporte_gemini = consultar_ia(GEMINI, bloque_entrada, api_key, role_gemini, max_tokens=500)
            
            role_gpt = "Eres GPT-4o. Busca en internet las alineaciones confirmadas y reportes climáticos o de viento para este partido de MLB. Entrega datos puros."
            reporte_gpt = consultar_ia(GPT4O, bloque_entrada, api_key, role_gpt, max_tokens=500)
            
            with col1:
                st.markdown("### ⚫ Ojo 1: Perplexity")
                st.info(reporte_perp)
            with col2:
                st.markdown("### 🔵 Ojo 2: Gemini")
                st.info(reporte_gemini)
            with col3:
                st.markdown("### 🛡️ Ojo 3: GPT-4o")
                st.info(reporte_gpt)

        st.divider()

        # =========================================================
        # FASE 2: CÁLCULO MATEMÁTICO PURO (o1-mini)
        # =========================================================
        st.header("🧠 Fase 2: Análisis Matemático del Mercado Abierto")
        with st.spinner("o1-mini desglosando momios sin contaminación de entorno..."):
            
            # El Oddsmaker NO sabe quién pitchea ni el clima. Solo evalúa si los números de Hard Rock están amañados.
            role_o1 = (
                "Eres el Oddsmaker de OpenAI o1-mini. Analiza fríamente las líneas y momios de Hard Rock Bet provistos en el prompt. "
                "Calcula la probabilidad implícita y determina dónde se encuentra el valor matemático teórico (+EV). "
                "No asumas lanzadores ni variables climáticas. Limítate a la matemática de las cuotas."
            )
            reporte_o1 = consultar_ia(O1_MINI, lineas_raw, api_key, role_o1)
            st.code(reporte_o1)

        st.divider()

        # =========================================================
        # FASE 3: EL FILTRO SUPREMO Y DECANTACIÓN DE CONTRADICCIONES (Claude)
        # =========================================================
        st.subheader("🏆 Fase 3: Sentencia del Tribunal de Contradicciones (Claude 3.5 Sonnet)")
        
        # Juntamos los 4 reportes crudos para que Claude los destruya si no coinciden
        bloque_juez = f"""
        [LÍNEAS HARD ROCK]: {lineas_raw}
        [REPORTE INVESTIGACIÓN 1 (Perplexity)]: {reporte_perp}
        [REPORTE INVESTIGACIÓN 2 (Gemini)]: {reporte_gemini}
        [REPORTE INVESTIGACIÓN 3 (GPT-4o)]: {reporte_gpt}
        [ANÁLISIS MATEMÁTICO (o1-mini)]: {reporte_o1}
        """
        
        with st.spinner("Claude buscando mentiras, cruzando datos y emitiendo dictamen..."):
            role_juez = (
                "Eres el Juez Supremo de Claude 3.5 Sonnet. Tu deber es auditar con desconfianza absoluta los 4 reportes provistos.\n\n"
                "PASO 1: Encuentra contradicciones. Si Perplexity, Gemini y GPT-4o no coinciden en el abridor, las bajas o el clima, expón el fallo abiertamente.\n"
                "PASO 2: Cruza el análisis matemático de o1-mini con la realidad del terreno de juego.\n"
                "PASO 3: Decanta y emite tu veredicto. Si los datos son inestables, contradictorios o no hay una ventaja matemática clara (+EV), dicta obligatoriamente 'Pick Oficial: PASS / NO BET' y justifica el porqué.\n\n"
                "Estructura obligatoria de respuesta:\n"
                "- **Contradicciones Detectadas:** [Escribe qué IA falló o qué dato no cuadra, o 'Ninguna']\n"
                "- **Pick Oficial:** [Línea exacta y acción, o PASS / NO BET]\n"
                "- **Confianza:** [Alto / Medio / Bajo / Cero]\n"
                "- **Ventaja (+EV) o Alerta:** [Justificación fría en una sola frase]\n"
                "- **Factor de Destrucción:** [Qué imprevisto o mentira en los datos arruina el parley]"
            )
            veredicto_supremo = consultar_ia(CLAUDE, bloque_juez, api_key, role_juez, max_tokens=650)
            
            st.success(veredicto_supremo)
            st.balloons()
