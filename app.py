import streamlit as st
import requests

# 1. Configuración de pantalla y memoria persistente
st.set_page_config(page_title="Coliseo de Expertos AI", layout="centered")

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""
if "saved_api_key" not in st.session_state:
    st.session_state["saved_api_key"] = ""

def limpiar_datos():
    st.session_state["input_text"] = ""

def sanitizar_key(raw_key):
    if not raw_key:
        return ""
    # Solo caracteres ASCII visibles sin espacios ni comillas
    limpia = "".join(c for c in raw_key.strip() if 33 <= ord(c) <= 126)
    limpia = limpia.replace('"', '').replace("'", "")
    if limpia.lower().startswith("bearer"):
        limpia = limpia[6:].strip()
    return limpia

st.title("🏛️ El Coliseo: Consenso Universal de IA")
st.markdown("Motor de análisis predictivo y auditoría de datos para cualquier deporte.")

# 2. Barra lateral con Diagnóstico de Chat Real
with st.sidebar:
    st.header("🔑 Acceso")
    raw_input = st.text_input(
        "Introduce tu API Key de OpenRouter:",
        value=st.session_state["saved_api_key"],
        type="default"  # Visible temporalmente para evitar que el navegador la cambie por una contraseña guardada
    )
    
    cleaned = sanitizar_key(raw_input)
    if cleaned:
        st.session_state["saved_api_key"] = cleaned
        
    api_key = st.session_state["saved_api_key"]
    
    if api_key:
        st.caption(f"🔒 Clave activa: `{api_key[:10]}...{api_key[-4:]}` ({len(api_key)} chars)")
        
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            if st.button("🔌 1. Ver Saldo", use_container_width=True):
                try:
                    r = requests.get(
                        "https://openrouter.ai/api/v1/auth/key",
                        headers={"Authorization": f"Bearer {api_key}"},
                        timeout=15
                    )
                    st.code(f"HTTP {r.status_code}\n{r.text}", language="json")
                except Exception as e:
                    st.error(f"Error: {e}")
                    
        with col_k2:
            if st.button("🧪 2. Probar Chat", use_container_width=True):
                try:
                    r_chat = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "https://localhost:8501",
                            "X-Title": "ColiseoTest"
                        },
                        json={
                            "model": "openai/gpt-4o-mini",
                            "messages": [{"role": "user", "content": "Di OK"}]
                        },
                        timeout=20
                    )
                    st.code(f"HTTP {r_chat.status_code}\n{r_chat.text[:400]}", language="json")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.write("---")
    st.markdown("""
    ### ⚙️ Motor Multideporte:
    * **Permeable:** Acepta datos crudos o consultas abiertas.
    * **Universal:** Válido para cualquier disciplina deportiva.
    * **Monitoreo:** Estado de agentes en tiempo real.
    """)

# 3. Función de consulta directa y estable
def consultar_ia(model_id, prompt, key, system_prompt="Eres un analista experto."):
    key_limpia = sanitizar_key(key)
    headers = {
        "Authorization": f"Bearer {key_limpia}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://localhost:8501",
        "X-Title": "ColiseoAI"
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
            json=payload,
            timeout=90
        )
        if response.status_code == 200:
            data = response.json()
            if "choices" in data and len(data["choices"]) > 0:
                res_text = data["choices"][0]["message"].get("content", "")
                if res_text and res_text.strip():
                    return {"status": "OK", "content": res_text}
            if "error" in data:
                return {"status": "ERROR", "content": f"Error interno ({model_id}): {data['error']}"}
            return {"status": "ERROR", "content": "Respuesta vacía del modelo"}
        else:
            return {"status": "ERROR", "content": f"HTTP {response.status_code} ({model_id}): {response.text}"}
    except Exception as e:
        return {"status": "ERROR", "content": f"Error de conexión ({model_id}): {str(e)}"}

def obtener_contenido_seguro(respuesta):
    return respuesta["content"] if respuesta["status"] == "OK" else "No disponible (Agente fuera de línea)."

# 4. Entrada de datos universal
pregunta = st.text_area(
    "✍️ Introduce tu consulta, partido o pega los datos/estadísticas (cualquier deporte):", 
    key="input_text",
    placeholder="Ej: Análisis del partido de hoy entre X e Y con estos datos... o simplemente una pregunta abierta.",
    height=150
)

col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    procesar = st.button("🚀 Iniciar Consenso del Coliseo", use_container_width=True)
with col_btn2:
    st.button("🔄 Reiniciar", on_click=limpiar_datos, use_container_width=True)

# 5. Flujo de Procesamiento Secuencial con Barra de Progreso (Sin fallos de hilos)
if procesar:
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not pregunta.strip():
        st.warning("⚠️ Escribe tu consulta o proporciona datos deportivos primero.")
    else:
        st.write("---")
        st.subheader("📡 Estado del Escaneo de Agentes:")
        
        barra = st.progress(0, text="Iniciando Fase 1: Búsqueda de contexto y datos...")
        contenedor_estados = st.container()
        
        # FASE 1
        prompt_fact = f"Investiga a fondo y extrae el contexto real actual, estadísticas clave, noticias o datos de última hora para la siguiente consulta deportiva: {pregunta}"
        call_perplexity = consultar_ia("perplexity/sonar", prompt_fact, api_key, "Eres el Fact-Checker deportivo universal. Trae datos reales y actualizados de internet para cualquier deporte.")
        barra.progress(15, text="Perplexity completado. Consultando Administrador de Datos...")
        
        call_cohere = consultar_ia("deepseek/deepseek-chat", pregunta, api_key, "Eres el Administrador de Datos. Organiza, procesa y cruza de forma matemática la información estadística entregada, buscando patrones de valor.")
        barra.progress(30, text="Administrador de Datos completado. Consultando Generalista Llama 3...")
        
        call_llama = consultar_ia("meta-llama/llama-3.3-70b-instruct", pregunta, api_key, "Eres el Generalista Deportivo. Ofrece una perspectiva situacional rápida y directa sobre el enfrentamiento o escenario planteado.")
        barra.progress(45, text="Fase 1 completada. Iniciando Fase 2: Auditoría técnica...")

        # FASE 2
        prompt_debate = f"""
        CONSULTA ORIGINAL: {pregunta}
        
        REPORTE DE CONTEXTO WEB (Perplexity): {obtener_contenido_seguro(call_perplexity)}
        ANÁLISIS ESTADÍSTICO (Administrador): {obtener_contenido_seguro(call_cohere)}
        PERSPECTIVA SITUACIONAL (Llama): {obtener_contenido_seguro(call_llama)}
        
        Tu tarea: Evalúa críticamente esta información. Analiza las ventajas competitivas reales, tendencias del encuentro y la lógica de las probabilidades para determinar dónde está el verdadero valor del pick, neutralizando sesgos.
        """
        
        call_deepseek = consultar_ia("deepseek/deepseek-r1", prompt_debate, api_key, "Eres DeepSeek R1. Analiza con lógica matemática estricta la probabilidad de éxito de cada escenario basado en los datos recabados.")
        barra.progress(60, text="DeepSeek R1 completado. Auditando con Codestral...")
        
        call_codestral = consultar_ia("mistralai/codestral-2501", prompt_debate, api_key, "Eres el Auditor Eficiente. Identifica incongruencias numéricas, datos cruzados falsos o contradicciones entre los reportes previos.")
        barra.progress(72, text="Codestral completado. Evaluando intangibles con Grok...")
        
        call_grok = consultar_ia("x-ai/grok-2-1212", prompt_debate, api_key, "Eres Grok. Evalúa las variables intangibles, el factor de localía, motivación o comportamiento reciente en la disciplina analizada.")
        barra.progress(85, text="Grok completado. Sintetizando con Gemini...")
        
        call_gemini = consultar_ia("google/gemini-2.5-pro", prompt_debate, api_key, "Eres Gemini. Procesa todo el volumen masivo de argumentos anteriores para estructurar un panorama contextual completo del evento.")
        barra.progress(92, text="Fase 2 completada. El Juez Supremo Claude está dictando sentencia...")

        # FASE 3
        debate_completo = f"""
        CONSULTA DEL EVENTO: {pregunta}
        
        --- FASE 1: DATOS Y HECHOS ---
        Perplexity: {obtener_contenido_seguro(call_perplexity)}
        Datos/Patrones: {obtener_contenido_seguro(call_cohere)}
        Situacional: {obtener_contenido_seguro(call_llama)}
        
        --- FASE 2: DEBATE TÉCNICO Y AUDITORÍA ---
        Lógica Matemática (DeepSeek): {obtener_contenido_seguro(call_deepseek)}
        Auditoría de Contradicciones (Codestral): {obtener_contenido_seguro(call_codestral)}
        Variables Intangibles (Grok): {obtener_contenido_seguro(call_grok)}
        Síntesis Contextual (Gemini): {obtener_contenido_seguro(call_gemini)}
        """
        
        call_claude = consultar_ia(
            "anthropic/claude-3.7-sonnet", 
            debate_completo, 
            api_key, 
            "Eres el Analista Clínico de Anthropic. Actúas como el Juez Supremo del Coliseo. Filtra de forma definitiva todo el debate de tus compañeros y extrae con precisión matemática las 2 o 3 mejores opciones/jugadas con mayor factor de ganar en este deporte. Muestra los resultados finales de forma sumamente bonita, limpia y compacta para una pantalla móvil, empleando viñetas y negritas."
        )
        barra.progress(100, text="¡Análisis del Coliseo completado!")

        # Renderizado del tablero de luces del escáner
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
                st.button("🟢 Grok" if call_grok["status"] == "OK" else "🔴 Grok", key="b_grok", disabled=True, use_container_width=True)
            with c4:
                st.button("🟢 Gemini" if call_gemini["status"] == "OK" else "🔴 Gemini", key="b_gem", disabled=True, use_container_width=True)
                st.button("🟢 Juez Claude" if call_claude["status"] == "OK" else "🔴 Juez Claude", key="b_clau", disabled=True, use_container_width=True)

        # 6. Despliegue del veredicto final conciso
        st.write("---")
        st.subheader("🏆 Jugadas Seleccionadas con Mayor Factor de Ganar")
        
        if call_claude["status"] == "OK":
            st.success(call_claude["content"])
            st.balloons()
        else:
