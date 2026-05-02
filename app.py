import streamlit as st
import requests
import json

st.set_page_config(page_title="IA Grupal: Panel de Expertos", layout="wide")
st.title("🤖 Panel de Expertos: Chat Grupal")

with st.sidebar:
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.info("Modelos: GPT-4o, Gemini 1.5 Pro y Grok 3")

def consultar_ia(model_id, prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501", # Necesario para OpenRouter
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
        resultado = response.json()
        
        # Si la API nos da un error, lo mostramos
        if 'error' in resultado:
            return f"❌ Error de la IA ({model_id}): {resultado['error']['message']}"
        
        return resultado['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

pregunta = st.text_area("¿Qué quieres preguntar al grupo?", placeholder="Escribe aquí tu consulta...")

if st.button("Iniciar Debate"):
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not pregunta:
        st.warning("⚠️ Escribe una pregunta primero.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with st.spinner('Llamando a los expertos...'):
            # Consultas individuales
            r_gpt = consultar_ia("openai/gpt-4o", pregunta, api_key)
            r_gemini = consultar_ia("google/gemini-pro-1.5", pregunta, api_key)
            r_grok = consultar_ia("x-ai/grok-3", pregunta, api_key)

            with col1:
                st.subheader("ChatGPT-4o")
                st.info(r_gpt)
            
            with col2:
                st.subheader("Gemini 1.5 Pro")
                st.info(r_gemini)
                
            with col3:
                st.subheader("Grok 3")
                st.info(r_grok)

        # Solo si al menos uno respondió bien, hacemos la síntesis
        if "❌" not in r_gpt or "❌" not in r_gemini:
            st.divider()
            with st.spinner('Generando consenso final...'):
                prompt_consenso = f"Actúa como un juez experto. Analiza estas 3 respuestas, corrige sus errores y da una única respuesta final perfecta:\n\n1: {r_gpt}\n\n2: {r_gemini}\n\n3: {r_grok}"
                final = consultar_ia("google/gemini-pro-1.5", prompt_consenso, api_key)
                st.header("🏆 Respuesta Final Decantada")
                st.success(final)
