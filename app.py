import streamlit as st
import requests
import json

# 1. Configuración de la pantalla
st.set_page_config(page_title="IA Grupal: Panel de Expertos", layout="wide")
st.title("🤖 Panel de Expertos: Chat Grupal")
st.markdown("Combina el poder de GPT-4o, Gemini y Grok 3 en una sola respuesta.")

# 2. Barra lateral para la API Key
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.info("Este panel consultará simultáneamente a los modelos de OpenAI, Google y xAI.")

# 3. Función para llamar a las IAs
def consultar_ia(model_id, prompt, key):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Panel de Expertos AI"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "Eres un experto analítico. Proporciona información precisa y técnica."},
            {"role": "user", "content": prompt}
        ]
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
            
        data = response.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return f"❌ Error: {data.get('error', {}).get('message', 'Error desconocido')}"
            
    except Exception as e:
        return f"❌ Error de conexión: {str(e)}"

# 4. Interfaz de usuario
pregunta = st.text_area("¿Qué quieres que debatan los expertos?", placeholder="Ej: Analiza los pros y contras de la energía nuclear...")

if st.button("🚀 Iniciar Debate"):
    if not api_key:
        st.error("⚠️ Por favor, introduce tu API Key en la barra lateral.")
    elif not pregunta:
        st.warning("⚠️ Escribe una pregunta o tema.")
    else:
        # FASE 1: GENERACIÓN INDIVIDUAL
        st.subheader("📢 Fase 1: Respuestas Individuales")
        col1, col2, col3 = st.columns(3)
        
        with st.spinner('Los expertos están redactando...'):
            # Los IDs de modelos que mejor funcionan en OpenRouter actualmente:
            res_gpt = consultar_ia("openai/gpt-4o", pregunta, api_key)
            res_gemini = consultar_ia("google/gemini-pro-1.5", pregunta, api_key)
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

        # FASE 2: CONSENSO (SÍNTESIS)
        # Solo procedemos si al menos uno no es un error
        if "❌" not in res_gpt or "❌" not in res_gemini:
            st.divider()
            st.subheader("🏆 Fase 2: Consenso y Respuesta Final")
            
            with st.spinner('Comparando respuestas y corrigiendo errores...'):
                prompt_final = f"""
                Actúa como un editor jefe científico. A continuación tienes 3 respuestas de diferentes IAs a la misma pregunta.
                Tu objetivo es:
                1. Identificar si alguna cometió un error factual o alucinación.
                2. Corregir cualquier contradicción.
                3. Fusionar lo mejor de las tres en una respuesta 'decantada', organizada y definitiva.
                
                Respuesta 1 (GPT): {res_gpt}
                Respuesta 2 (Gemini): {res_gemini}
                Respuesta 3 (Grok): {res_grok}
                """
                # Usamos Gemini Pro para la síntesis por su capacidad de razonamiento
                res_final = consultar_ia("google/gemini-pro-1.5", prompt_final, api_key)
                
                st.success(res_final)
