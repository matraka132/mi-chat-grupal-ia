import streamlit as st
import requests
import json

st.set_page_config(page_title="IA Grupal: Panel de Expertos", layout="wide")
st.title("🤖 Panel de Expertos: Chat Grupal")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.info("Modelos: GPT-4o, Gemini 1.5 Flash y Grok 3")

def consultar_ia(model_id, prompt, key):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Panel de Expertos AI"
    }
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload), timeout=60)
        if response.status_code != 200:
            return f"❌ Error {response.status_code}: {response.text}"
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

pregunta = st.text_area("¿Qué quieres preguntar al grupo?", placeholder="Escribe aquí...")

if st.button("🚀 Iniciar Debate"):
    if not api_key:
        st.error("Falta la API Key.")
    elif not pregunta:
        st.warning("Escribe una pregunta.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with st.spinner('Consultando expertos...'):
            # Fase 1: Respuestas individuales
            r_gpt = consultar_ia("openai/gpt-4o", pregunta, api_key)
            r_gemini = consultar_ia("google/gemini-flash-1.5", pregunta, api_key)
            r_grok = consultar_ia("x-ai/grok-3", pregunta, api_key)

            with col1:
                st.subheader("ChatGPT-4o")
                st.write(r_gpt)
            
            with col2:
                st.subheader("Gemini 1.5 Flash")
                st.write(r_gemini)
                
            with col3:
                st.subheader("Grok 3")
                st.write(r_grok)

        # Fase 2: Consenso
        st.divider()
        with st.spinner('Generando respuesta final...'):
            p_final = f"Analiza estas 3 respuestas, corrige errores y da una respuesta final perfecta:\n1: {r_gpt}\n2: {r_gemini}\n3: {r_grok}"
            final = consultar_ia("google/gemini-flash-1.5", p_final, api_key)
            st.header("🏆 Respuesta Final Decantada")
            st.success(final)
