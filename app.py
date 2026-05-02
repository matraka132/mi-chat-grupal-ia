import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="IA Grupal: Gemini + GPT + Grok", layout="wide")
st.title("🤖 Panel de Expertos: Chat Grupal de IAs")

# Barra lateral para la configuración
with st.sidebar:
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.info("Este panel consultará a Gemini 1.5 Pro, GPT-4o y Grok 3 simultáneamente.")

def consultar_ia(model_id, prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

pregunta = st.text_area("¿Qué quieres preguntar al grupo?", placeholder="Ej: Explícame la teoría de cuerdas y que los demás busquen errores.")

if st.button("Iniciar Debate"):
    if not api_key:
        st.error("Por favor, introduce tu API Key.")
    else:
        col1, col2, col3 = st.columns(3)
        
        with st.spinner('Consultando a los expertos...'):
            # Fase 1: Respuestas individuales
            resp_gpt = consultar_ia("openai/gpt-4o", pregunta, api_key)
            resp_gemini = consultar_ia("google/gemini-pro-1.5", pregunta, api_key)
            resp_grok = consultar_ia("x-ai/grok-3", pregunta, api_key) # Nota: Asegúrate que esté disponible en OpenRouter

            with col1:
                st.subheader("ChatGPT-4o")
                st.write(resp_gpt)
            
            with col2:
                st.subheader("Gemini 1.5 Pro")
                st.write(resp_gemini)
                
            with col3:
                st.subheader("Grok 3")
                st.write(resp_grok)

        st.divider()
        
        with st.spinner('Decantando respuesta final...'):
            # Fase 2: El Consenso
            prompt_consenso = f"""
            Aquí tienes tres respuestas a la misma pregunta. 
            Tu tarea es actuar como un editor jefe: identifica errores en cada una, combina los puntos fuertes 
            y entrega una respuesta final perfecta y "decantada".
            
            Respuesta 1: {resp_gpt}
            Respuesta 2: {resp_gemini}
            Respuesta 3: {resp_grok}
            """
            final = consultar_ia("google/gemini-pro-1.5", prompt_consenso, api_key)
            
            st.header("🏆 Respuesta Final Decantada")
            st.success(final)
