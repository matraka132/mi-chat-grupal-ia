import streamlit as st
import requests
import json

# 1. Configuración de la pantalla
st.set_page_config(page_title="Super Panel de Expertos IA", layout="wide")
st.title("🤖 Super Panel: 5 IAs en Debate")
st.markdown("GPT-4o + Gemini 1.5 + Grok 3 + Claude 3.5 + DeepSeek R1")

# 2. Barra lateral para la API Key
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.info("Este panel cruzará las respuestas de los 5 mejores modelos del mundo para darte una verdad decantada.")

# 3. Función robusta para llamar a las IAs
def consultar_ia(model_id, prompt, key):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Panel de Expertos AI v2"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "Eres un experto de alto nivel. Tu objetivo es ser preciso, crítico y evitar alucinaciones."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=90 # Más tiempo porque DeepSeek y Grok pueden tardar
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
pregunta = st.text_area("¿Cuál es el desafío para el panel?", placeholder="Escribe tu consulta detallada aquí...")

if st.button("🚀 Iniciar Debate Multilateral"):
    if not api_key:
        st.error("⚠️ Introduce tu API Key a la izquierda.")
    elif not pregunta:
        st.warning("⚠️ Escribe una pregunta.")
    else:
        # FASE 1: GENERACIÓN INDIVIDUAL
        st.subheader("📢 Fase 1: Análisis de los Expertos")
        
        # Creamos 5 columnas
        cols = st.columns(5)
        modelos = [
            ("openai/gpt-4o", "🟢 GPT-4o"),
            ("~google/gemini-pro-latest", "🔵 Gemini 1.5 Pro"),
            ("x-ai/grok-3", "⚫ Grok 3"),
            ("anthropic/claude-3.5-sonnet", "🟠 Claude 3.5"),
            ("deepseek/deepseek-r1", "🔴 DeepSeek R1")
        ]
        
        respuestas = []
        
        with st.spinner('Consultando al panel...'):
            for i, (m_id, m_nombre) in enumerate(modelos):
                res = consultar_ia(m_id, pregunta, api_key)
                respuestas.append(res)
                with cols[i]:
                    st.markdown(f"### {m_nombre}")
                    st.write(res)

        # FASE 2: EL CONSENSO MAESTRO
        st.divider()
        st.subheader("🏆 Fase 2: Veredicto Final Decantado")
        
        with st.spinner('Unificando criterios y eliminando errores...'):
            # Construimos el prompt de síntesis con las 5 respuestas
            texto_respuestas = "\n\n".join([f"RESPUESTA {i+1}: {r}" for i, r in enumerate(respuestas)])
            
            prompt_final = f"""
            Actúa como un Auditor Jefe de Inteligencia Artificial. Tienes frente a ti 5 respuestas de diferentes modelos (GPT, Gemini, Grok, Claude y DeepSeek).
            
            Tu misión es:
            1. Analizar si algún modelo cometió un error técnico o lógico.
            2. Extraer los datos más certeros y profundos de cada respuesta.
            3. Redactar una solución única, perfectamente estructurada y 'decantada' que sea superior a cualquier respuesta individual.
            
            Aquí están las respuestas:
            {texto_respuestas}
            """
            
            # Usamos Claude 3.5 o Gemini Pro para la síntesis por su excelente juicio
            veredicto = consultar_ia("anthropic/claude-3.5-sonnet", prompt_final, api_key)
            
            st.success(veredicto)
