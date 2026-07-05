import streamlit as st
import requests
import json

# 1. Configuración de pantalla y estado
st.set_page_config(page_title="Coliseo AI - Modo Señales", layout="centered")

# Lógica para reiniciar el cuadro de texto sin recargar la página entera
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

def limpiar_datos():
    st.session_state["input_text"] = ""

st.title("🏛️ El Coliseo: Algoritmo de Consenso")
st.markdown("Analiza anomalías en vivo, movimientos de líneas y volumen para darte las jugadas de mayor valor.")

# 2. Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Acceso")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### ⚙️ Modo Operativo:
    * **Filtro de Hechos:** Activo (Perplexity + Cohere)
    * **Cálculo de Riesgo:** Activo (DeepSeek + Qwen)
    * **Veredicto:** Activo (o1-mini + Claude 3.5)
    * *Estado:* Ocultando debates intermedios para mayor claridad visual.
    """)

# 3. Función de consulta a la API
def consultar_ia(model_id, prompt, key, system_prompt="Eres un analista experto."):
    if not key:
        return "❌ Error: API Key faltante."
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
            timeout=90
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"❌ Error {response.status_code}"
    except:
        return "❌ Error de conexión"

# 4. Entrada de datos del usuario vinculada al Session State
pregunta = st.text_area(
    "✍️ Introduce los datos, partidos, cuotas en vivo o comportamiento del mercado:",
    value=st.session_state["input_text"],
    key="input_text",
    placeholder="Ej: Lakers va ganando por 2, el público se está volviendo loco apostándoles en vivo pero Hard Rock subió la cuota de repente a +1.5...",
    height=150
)

# Botones de acción alineados de forma limpia
col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    procesar = st.button("🚀 Calcular Jugadas de Alto Valor", use_container_width=True)

with col_btn2:
    st.button("🔄 Reiniciar", on_click=limpiar_datos, use_container_width=True)

# 5. Ejecución del flujo en segundo plano (Silencioso)
if procesar:
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not pregunta:
        st.warning("⚠️ Escribe la consulta o pega la información deportiva primero.")
    else:
        # Contenedor de carga elegante para que el usuario sepa que está trabajando
        with st.spinner('🏛️ Los 10 Agentes están debatiendo en el Coliseo... Calculando la trampa de la casa...'):
            
            # --- FASE 1: HECHOS (En segundo plano) ---
            res_perplexity = consultar_ia("perplexity/sonar", f"Analiza movimientos de línea en vivo para: {pregunta}.", api_key, "Identifica dónde está el volumen del público masivo.")
            res_cohere = consultar_ia("cohere/command-r-plus", pregunta, api_key, "Piensa como el creador de líneas de Hard Rock Bet. ¿Dónde está la trampa matemática?")
            
            # --- FASE 2: DEBATE DE PROBABILIDADES (En segundo plano) ---
            prompt_debate = f"Pregunta: {pregunta}\nDatos: {res_perplexity}\nEstrategia: {res_cohere}"
            res_deepseek = consultar_ia("deepseek/deepseek-chat", prompt_debate, api_key, "Calcula la probabilidad real vs la cuota inflada por la casa.")
            res_grok = consultar_ia("x-ai/grok-beta", prompt_debate, api_key, "Define dónde van a timar a los apostadores novatos.")
            
            # --- FASE 3: EL VEREDICTO FINAL ---
            # Reunimos todo el conocimiento oculto y se lo damos al Juez Supremo (Claude)
            debate_completo = f"""
            PREGUNTA: {pregunta}
            HECHOS: {res_perplexity}
            ESTRATEGIA CASA: {res_cohere}
            MATEMÁTICA: {res_deepseek}
            TENDENCIA: {res_grok}
            """
            
            veredicto_final = consultar_ia(
                "anthropic/claude-3.5-sonnet", 
                debate_completo, 
                api_key, 
                "Eres el Analista Jefe de Arbitraje de Riesgo. Tu única tarea es ignorar el ruido y entregar al usuario estrictamente las 2 o 3 mejores jugadas con mayor factor de ganar, basándote en ir a favor de la casa (Fading the public). Formatea el resultado de manera sumamente limpia, bonita, visual y concisa. Usa negritas y viñetas."
            )
        
        # 6. Muestra del resultado final bien pulido
        st.write("---")
        st.subheader("🏆 Veredicto del Coliseo: Jugadas Seleccionadas")
        
        # Tarjeta visualmente atractiva para las señales
        st.success(veredicto_final)
        st.balloons()
