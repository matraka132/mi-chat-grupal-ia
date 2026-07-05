import streamlit as st
import requests
import json

# 1. Configuración de pantalla y estado
st.set_page_config(page_title="Coliseo de Expertos AI", layout="centered")

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

def limpiar_datos():
    st.session_state["input_text"] = ""

st.title("🏛️ El Coliseo: Consenso de 10 Agentes de IA")
st.markdown("Monitoreo de agentes en tiempo real y veredicto de alta precisión.")

# 2. Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Acceso")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🧠 Panel de Control Activo:
    * Monitoreo de estado por agente.
    * Filtrado automático de errores.
    """)

# 3. Función de consulta modificada para validar respuestas
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
            timeout=90
        )
        if response.status_code == 200:
            res_text = response.json()["choices"][0]["message"]["content"]
            # Si la respuesta contiene texto válido y no un mensaje vacío o de error explícito
            if res_text and "❌" not in res_text:
                return {"status": "OK", "content": res_text}
        return {"status": "ERROR", "content": f"Error {response.status_code}"}
    except:
        return {"status": "ERROR", "content": "Error de conexión"}

# 4. Entrada de datos del usuario
pregunta = st.text_area(
    "✍️ Introduce los datos, partidos o cuotas a analizar:", 
    value=st.session_state["input_text"],
    key="input_text",
    placeholder="Ej: Datos de abridores, líneas de Hard Rock Bet, estadísticas recientes...",
    height=150
)

col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    procesar = st.button("🚀 Iniciar Proceso de Consenso", use_container_width=True)
with col_btn2:
    st.button("🔄 Reiniciar", on_click=limpiar_datos, use_container_width=True)

# 5. Flujo de procesamiento con Tablero de Estado Visual
if procesar:
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not pregunta:
        st.warning("⚠️ Escribe la consulta o pega la información deportiva.")
    else:
        
        st.write("---")
        st.subheader("📡 Estado del Escaneo de Agentes:")
        
        # Marcadores de posición visuales para simular los "botones/luces" de estado
        contenedor_estados = st.container()
        
        with st.spinner('Procesando debate en segundo plano...'):
            
            # --- FASE 1 ---
            call_perplexity = consultar_ia("perplexity/sonar", pregunta, api_key, "Eres el Fact-Checker. Trae datos reales, climas, estadios o lesiones de última hora.")
            call_cohere = consultar_ia("deepseek/deepseek-v3.2", pregunta, api_key, "Eres el Administrador de Datos. Cruza las estadísticas frías sin inventar nada.")
            call_llama = consultar_ia("meta-llama/llama-3.3-70b-instruct", pregunta, api_key, "Eres el Generalista Rápido. Da una perspectiva estadística directa.")

            # --- FASE 2 ---
            prompt_debate = f"Pregunta: {pregunta}\nReporte: {call_perplexity['content'] if call_perplexity['status'] == 'OK' else ''}\nEstadísticas: {call_cohere['content'] if call_cohere['status'] == 'OK' else ''}"
            
            call_deepseek = consultar_ia("deepseek/deepseek-v3.2", prompt_debate, api_key, "Eres DeepSeek Coder. Tu fuerte es la lógica matemática pura y el cálculo de probabilidades.")
            call_codestral = consultar_ia("anthropic/claude-sonnet-4.5", prompt_debate, api_key, "Eres el Auditor Eficiente. Encuentra contradicciones numéricas entre los reportes.")
            call_grok = consultar_ia("x-ai/grok-4.3", prompt_debate, api_key, "Eres Grok 3. Analiza las tendencias de última hora y el movimiento de líneas coloquiales.")
            call_gemini = consultar_ia("~google/gemini-pro-latest", prompt_debate, api_key, "Eres Gemini. Procesa todo el contexto masivo de las respuestas previas.")

            # --- FASE 3 ---
            debate_completo = f"""
            PREGUNTA: {pregunta}
            FASE 1: {call_perplexity['content']} | {call_cohere['content']}
            FASE 2: {call_deepseek['content']} | {call_grok['content']} | {call_gemini['content']}
            """
            
            call_claude = consultar_ia(
                "anthropic/claude-sonnet-4.5", 
                debate_completo, 
                api_key, 
                "Eres el Analista Clínico de Anthropic. Revisa los argumentos válidos, identifica trampas del mercado y entrega estricta y únicamente las 2 o 3 mejores jugadas con más factor de ganar de forma resumida, usando negritas y viñetas para móvil."
            )

        # Pintamos el "Tablero de Luces" en el contenedor basado en si fue OK o ERROR
        with contenedor_estados:
            # Dividimos la pantalla en columnas compactas para simular la barra/tablero de botones
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.button("🟢 Perplexity" if call_perplexity["status"] == "OK" else "🔴 Perplexity", key="btn_perp", disabled=True, use_container_width=True)
                st.button("🟢 DeepSeek" if call_deepseek["status"] == "OK" else "🔴 DeepSeek", key="btn_deep", disabled=True, use_container_width=True)
            with c2:
                st.button("🟢 Cohere (DS)" if call_cohere["status"] == "OK" else "🔴 Cohere (DS)", key="btn_coh", disabled=True, use_container_width=True)
                st.button("🟢 Codestral" if call_codestral["status"] == "OK" else "🔴 Codestral", key="btn_code", disabled=True, use_container_width=True)
            with c3:
                st.button("🟢 Llama 3" if call_llama["status"] == "OK" else "🔴 Llama 3", key="btn_llam", disabled=True, use_container_width=True)
                st.button("🟢 Grok 3" if call_grok["status"] == "OK" else "🔴 Grok 3", key="btn_grok", disabled=True, use_container_width=True)
            with c4:
                st.button("🟢 Gemini" if call_gemini["status"] == "OK" else "🔴 Gemini", key="btn_gem", disabled=True, use_container_width=True)
                st.button("🟢 Claude 3.5" if call_claude["status"] == "OK" else "🔴 Claude 3.5", key="btn_clau", disabled=True, use_container_width=True)

        # 6. Salida del resultado final
        st.write("---")
        st.subheader("🏆 Jugadas Seleccionadas con Mayor Factor de Ganar")
        
        if call_claude["status"] == "OK":
            st.success(call_claude["content"])
            st.balloons()
        else:
            st.error("⚠️ El Juez Final (Claude) no pudo procesar la conclusión. Revisa los estados de los agentes arriba.")
