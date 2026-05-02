import streamlit as st
import requests
import json

# Configuración visual
st.set_page_config(page_title="IA Grupal: Panel de Expertos", layout="wide")
st.title("🤖 Panel de Expertos: Chat Grupal")
st.markdown("---")

# Barra lateral
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.info("Este panel usa: \n- GPT-4o\n- Gemini Pro 1.5\n- Grok 3")

def consultar_ia(model_id, prompt, key):
    # Estos headers son los que OpenRouter pide para identificar la app
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app", 
        "X-Title": "Panel de Expertos AI",
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "Eres un experto colaborativo. Da respuestas precisas."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=60 # Esperamos hasta 60 segundos por Grok
        )
        
        # Si la respuesta no es 200 (OK), hay un problema
        if response.status_code != 200:
            return f"❌ Error {response.status_code}: {response.text}"
            
        data = response.json()
        
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"❌ Error de OpenRouter: {data['error']['message']}"
        else:
            return "❌ Error: Respuesta inesperada del servidor."
            
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# Área de texto para el usuario
pregunta = st.text_area("¿Cuál es el tema de debate?", placeholder="Escribe tu duda aquí...")

if st.button("🚀 Iniciar Debate e Inter-Corrección"):
    if not api_key:
        st.error("Por favor, pega tu API Key en la izquierda.")
    elif not pregunta:
        st.warning("Escribe algo para preguntar.")
    else:
        # FASE 1: GENERACIÓN
        st.subheader("📢 Fase 1: Respuestas Individuales")
        col1, col2, col3 = st.columns(3)
        
        with st.spinner("Los expertos están redactando..."):
            # Usamos IDs de modelos más estándar de OpenRouter
           res_gpt = consultar_ia("openai/gpt-4o", pregunta, api_key)
           res_gemini = consultar_ia("google/gemini-flash-1.5", pregunta, api_key) # Cambiado a Flash para asegurar compatibilidad
           res_grok = consultar_ia("x-ai/grok-3", pregunta, api_key)

            with col1:
                st.markdown("### 🟢 ChatGPT-4o")
                st.write(res_gpt)
            
            with col2:
                st.markdown("### 🔵 Gemini 1.5 Pro")
                st.write(res_gemini)
                
            with col3:
                st.markdown("### ⚫ Grok 3")
                st.write(res_grok)

        # FASE 2: SÍNTESIS (Si al menos uno respondió)
        if "❌" not in res_gpt or "❌" not in res_gemini:
            st.markdown("---")
            st.subheader("🏆 Fase 2: Consenso y Corrección")
            with st.spinner("Decantando la respuesta final..."):
                prompt_final = f"""
                Analiza estas tres respuestas de IA. Identifica si alguna cometió un error o alucinación.
                Crea una respuesta final que sea la mejor combinación de todas, corrigiendo fallos.
                
                Respuestas a analizar:
                1: {res_gpt}
                2: {res_gemini}
                3: {res_grok}
                """
                # Usamos Gemini para la síntesis final por su gran capacidad de razonamiento
               res_final = consultar_ia("google/gemini-flash-1.5", prompt_final, api_key)
                st.success(res_final)
