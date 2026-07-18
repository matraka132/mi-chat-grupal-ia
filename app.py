import streamlit as st
import requests
import json

# 1. Configuración de pantalla y estado (Optimizado para móvil)
st.set_page_config(page_title="Coliseo de Expertos AI", layout="centered")

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

def limpiar_datos():
    st.session_state["input_text"] = ""

st.title("🏛️ El Coliseo: Consenso Universal de IA")
st.markdown("Motor de análisis predictivo y auditoría de datos para cualquier deporte.")

# 2. Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Acceso")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### ⚙️ Motor Multideporte:
    * **Permeable:** Acepta datos crudos o consultas abiertas.
    * **Universal:** Válido para cualquier disciplina deportiva.
    * **Monitoreo:** Estado de agentes en tiempo real.
    """)

# 3. Función de consulta con validación de estado
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
            if res_text and "❌" not in res_text:
                return {"status": "OK", "content": res_text}
        return {"status": "ERROR", "content": f"Error {response.status_code}"}
    except:
        return {"status": "ERROR", "content": "Error de conexión"}

# 4. Entrada de datos universal
pregunta = st.text_area(
    "✍️ Introduce tu consulta, partido o pega los datos/estadísticas (cualquier deporte):", 
    value=st.session_state["input_text"],
    key="input_text",
    placeholder="Ej: Análisis del partido de hoy entre X e Y con estos datos... o simplemente una pregunta abierta.",
    height=150
)

col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    procesar = st.button("🚀 Iniciar Consenso del Coliseo", use_container_width=True)
with col_btn2:
    st.button("🔄 Reiniciar", on_click=limpiar_datos, use_container_width=True)

# 5. Flujo de Procesamiento Universal Intermedio
if procesar:
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not pregunta:
        st.warning("⚠️ Escribe tu consulta o proporciona datos deportivos primero.")
    else:
        
        st.write("---")
        st.subheader("📡 Estado del Escaneo de Agentes:")
        
        contenedor_estados = st.container()
        
        with st.spinner('🏛️ El Coliseo está auditando y cruzando la información...'):
            
            # ==========================================
            # FASE 1: BÚSQUEDA GENERAL E HIPÓTESIS (Tus direcciones)
            # ==========================================
            # Si el usuario no dio datos, Perplexity compensa buscando activamente en la web el contexto del deporte/partido indicado.
            prompt_fact = f"Investiga a fondo y extrae el contexto real actual, estadísticas clave, noticias o datos de última hora para la siguiente consulta deportiva: {pregunta}"
            call_perplexity = consultar_ia("perplexity/sonar", prompt_fact, api_key, "Eres el Fact-Checker deportivo universal. Trae datos reales y actualizados de internet para cualquier deporte.")
            
            call_cohere = consultar_ia("deepseek/deepseek-v3.2", pregunta, api_key, "Eres el Administrador de Datos. Organiza, procesa y cruza de forma matemática la información estadística entregada, buscando patrones de valor.")
            
            call_llama = consultar_ia("meta-llama/llama-3.3-70b-instruct", pregunta, api_key, "Eres el Generalista Deportivo. Ofrece una perspectiva situacional rápida y directa sobre el enfrentamiento o escenario planteado.")

            # ==========================================
            # FASE 2: AUDITORÍA TÉCNICA Y LÓGICA (Tus direcciones)
            # ==========================================
            prompt_debate = f"""
            CONSULTA ORIGINAL: {pregunta}
            
            REPORTE DE CONTEXTO WEB: {call_perplexity['content'] if call_perplexity['status'] == 'OK' else 'No disponible'}
            ANÁLISIS ESTADÍSTICO DE ENTRADA: {call_cohere['content'] if call_cohere['status'] == 'OK' else 'No disponible'}
            
            Tu tarea: Evalúa críticamente esta información. Analiza las ventajas competitivas reales, tendencias del encuentro y la lógica de las probabilidades para determinar dónde está el verdadero valor del pick, neutralizando sesgos.
            """
            
            call_deepseek = consultar_ia("deepseek/deepseek-v3.2", prompt_debate, api_key, "Eres DeepSeek Coder. Analiza con lógica matemática estricta la probabilidad de éxito de cada escenario basado en los datos recabados.")
            
            call_codestral = consultar_ia("anthropic/claude-sonnet-5", prompt_debate, api_key, "Eres el Auditor Eficiente. Identifica incongruencias numéricas, datos cruzados falsos o contradicciones entre los reportes previos.")
            
            call_grok = consultar_ia("x-ai/grok-4.3", prompt_debate, api_key, "Eres Grok 3. Evalúa las variables intangibles, el factor de localía, motivación o comportamiento reciente en la disciplina analizada.")
            
            call_gemini = consultar_ia("~google/gemini-pro-latest", prompt_debate, api_key, "Eres Gemini. Procesa todo el volumen masivo de argumentos anteriores para estructurar un panorama contextual completo del evento.")

            # ==========================================
            # FASE 3: EL VEREDICTO DE JUEZ SUPREMO (Tus direcciones)
            # ==========================================
            debate_completo = f"""
            CONSULTA DEL EVENTO: {pregunta}
            DATOS DE HECHOS: {call_perplexity['content']} | {call_cohere['content']}
            DEBATE TÉCNICO: {call_deepseek['content']} | {call_grok['content']} | {call_gemini['content']}
            """
            
            call_claude = consultar_ia(
                "anthropic/claude-sonnet-5", 
                debate_completo, 
                api_key, 
                "Eres el Analista Clínico de Anthropic. Actúas como el Juez Supremo del Coliseo. Filtra de forma definitiva todo el debate de tus compañeros y extrae con precisión matemática las 2 o 3 mejores opciones/jugadas con mayor factor de ganar en este deporte. Muestra los resultados finales de forma sumamente bonita, limpia y compacta para una pantalla móvil, empleando viñetas y negritas."
            )

        # Renderizado del tablero de luces del escáner en base al estado de la respuesta
        with contenedor_estados:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.button("🟢 Perplexity" if call_perplexity["status"] == "OK" else "🔴 Perplexity", key="b_perp", disabled=True, use_container_width=True)
                st.button("🟢 DeepSeek" if call_deepseek["status"] == "OK" else "🔴 DeepSeek", key="b_deep", disabled=True, use_container_width=True)
            with c2:
                st.button("🟢 Cohere (DS)" if call_cohere["status"] == "OK" else "🔴 Cohere (DS)", key="b_coh", disabled=True, use_container_width=True)
                st.button("🟢 Codestral" if call_codestral["status"] == "OK" else "🔴 Codestral", key="b_code", disabled=True, use_container_width=True)
            with c3:
                st.button("🟢 Llama 3" if call_llama["status"] == "OK" else "🔴 Llama 3", key="b_llam", disabled=True, use_container_width=True)
                st.button("🟢 Grok 3" if call_grok["status"] == "OK" else "🔴 Grok 3", key="b_grok", disabled=True, use_container_width=True)
            with c4:
                st.button("🟢 Gemini" if call_gemini["status"] == "OK" else "🔴 Gemini", key="b_gem", disabled=True, use_container_width=True)
                st.button("🟢 Claude 3.5" if call_claude["status"] == "OK" else "🔴 Claude 3.5", key="b_clau", disabled=True, use_container_width=True)

        # 6. Despliegue del veredicto final conciso
        st.write("---")
        st.subheader("🏆 Jugadas Seleccionadas con Mayor Factor de Ganar")
        
        if call_claude["status"] == "OK":
            st.success(call_claude["content"])
            st.balloons()
        else:
            st.error("⚠️ El Juez Final (Claude) no pudo procesar la conclusión. Verifica el estado de los agentes en el tablero superior.")
