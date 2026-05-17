import streamlit as st
import requests
import json

# 1. Configuración de la interfaz
st.set_page_config(page_title="Súper-Consenso Triple", layout="wide")
st.title("🏛️ El Súper-Coliseo: Flujo de Co-Auditoría Triple (Web Activa)")
st.markdown("Fase 1: Rastreo Real | Fase 2: Co-Auditoría | Fase 3: Analistas | Fase 4: Veredicto de Claude")

# Barra lateral para la API Key
with st.sidebar:
    st.header("🔑 Configuración")
    api_key = st.text_input("Introduce tu API Key de OpenRouter:", type="password")
    st.write("---")
    st.markdown("""
    ### 🧠 Motores del Sistema:
    * 🔍 **Grok 2 Search** (`x-ai/grok-2-search`)
    * 🔵 **Gemini 2.5 Pro** (`google/gemini-2.5-pro`)
    * 🟠 **Claude 3.5 Sonnet** (`anthropic/claude-3.5-sonnet`)
    """)

# PROMPT BASE ULTRA-ESTRICTO PARA AHORRO DE TOKENS
PROMPT_CERRADO = (
    "Eres un micro-agente analítico en un entorno cerrado. Prohibido usar conocimientos externos.\n"
    "REGLA DE ORO DE TOKENS: Sé ultra-conciso. Elimina saludos, introducciones, conclusiones y textos de relleno. "
    "Responde usando datos crudos, palabras clave y viñetas cortas. Prohibido generar URLs o enlaces.\n\n"
)

# Función centralizada de consulta con soporte de búsqueda web real
def consultar_ia(model_id, prompt, key, system_role, max_tokens=1000, forzar_web=False):
    headers = {
        "Authorization": f"Bearer {key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://streamlit.app",
        "X-Title": "Súper-Coliseo Web Activa"
    }
    
    # Si no es Grok buscando en la web, aplica el prompt cerrado estricto
    prompt_sistema = system_role if forzar_web else (PROMPT_CERRADO + system_role)
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    
    # ESTO FUERZA A OPENROUTER A USAR EL BUSCADOR DE GROK
    if forzar_web:
        payload["provider"] = {
            "plugins": [{"id": "web_search"}]
        }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=120
        )
        if response.status_code != 200:
            return f"❌ Error en {model_id}: {response.text}"
            
        texto = response.json()["choices"][0]["message"]["content"]
        return texto
    except Exception as e:
        return f"❌ Error de conexión en {model_id}: {str(e)}"

# Entrada de datos de Hard Rock Bet
lineas_raw = st.text_area("📋 Pega las líneas de Hard Rock Bet aquí:", height=150, placeholder="Ej:\nYankees\nMets\n-1.5 (+165)")

if st.button("🚀 Iniciar Ciclo del Súper-Coliseo"):
    if not api_key:
        st.error("⚠️ Falta la API Key en la barra lateral.")
    elif not lineas_raw:
        st.warning("⚠️ Pega la información de las líneas primero.")
    else:
        
        # Identificadores Oficiales de Modelos
        GROK = "x-ai/grok-2-search"
        GEMINI = "google/gemini-2.5-pro"
        CLAUDE = "anthropic/claude-3.5-sonnet"

        # =========================================================
        # FASE 1: INVESTIGACIÓN TRIPLE (Búsqueda Web Forzada)
        # =========================================================
        st.header("🔍 Fase 1: Investigación y Rastreo Triple")
        col_inv1, col_inv2, col_inv3 = st.columns(3)
        
        with st.spinner("Forzando a Grok a navegar por internet..."):
            
            role_grok_web = (
                "Eres Grok 2 con el buscador web activado. Tu meta es buscar en internet la información real para este partido de MLB de HOY. "
                "Encuentra obligatoriamente: 1) Lanzadores abridores confirmados y su mano (L o R). 2) Clima exacto del estadio y viento. "
                "3) Lesionados de última hora. Resume todo en viñetas ultra-cortas sin enlaces."
            )
            
            # Activamos 'forzar_web=True' para obligar a OpenRouter a conectarse a internet
            res_grok_inv = consultar_ia(GROK, lineas_raw, api_key, role_grok_web, max_tokens=800, forzar_web=True)
            
            role_inv_resto = "Resume al máximo la información web provista por Grok. Formato estricto: * Lanzadores: * Clima/Estadio: * Bajas:. Sin palabras extra."
            res_gemini_inv = consultar_ia(GEMINI, f"Líneas: {lineas_raw}\nWeb de Grok: {res_grok_inv}", api_key, f"Gemini-Search. {role_inv_resto}", max_tokens=600)
            res_claude_inv = consultar_ia(CLAUDE, f"Líneas: {lineas_raw}\nData: {res_gemini_inv}", api_key, f"Claude-Scout. {role_inv_resto}", max_tokens=600)
            
            with col_inv1:
                st.markdown("### ⚫ Grok 2 (Búsqueda Web Real)")
                st.info(res_grok_inv)
            with col_inv2:
                st.markdown("### 🔵 Gemini (Compreso)")
                st.info(res_gemini_inv)
            with col_inv3:
                st.markdown("### 自由 Claude 3.5 (Compreso)")
                st.info(res_claude_inv)

        st.divider()

        # =========================================================
        # FASE 2: AUDITORÍA TRIPLE CRUZADA
        # =========================================================
        st.header("🛡️ Fase 2: Co-Auditoría Cruzada (Compactación)")
        col_aud1, col_aud2, col_aud3 = st.columns(3)
        
        prompt_auditoria = f"Líneas: {lineas_raw}\nGrok: {res_grok_inv}\nGemini: {res_gemini_inv}\nClaude: {res_claude_inv}"
        
        with st.spinner("Cruzando y unificando datos..."):
            
            role_aud = "Detecta contradicciones. Genera una única lista consolidada de datos VERIFICADOS. Elimina redundanzas. Sé ultra-breve."
            
            aud_grok = consultar_ia(GROK, prompt_auditoria, api_key, f"Auditor Grok. {role_aud}", max_tokens=600)
            aud_gemini = consultar_ia(GEMINI, f"{prompt_auditoria}\nGrok: {aud_grok}", api_key, f"Auditor Gemini. {role_aud}", max_tokens=600)
            aud_claude = consultar_ia(CLAUDE, f"{prompt_auditoria}\nGemini: {aud_gemini}", api_key, f"Auditor Jefe Claude. {role_aud}", max_tokens=800)
            
            with col_aud1:
                st.markdown("### 🛡️ Auditoría Grok")
                st.write(aud_grok)
            with col_aud2:
                st.markdown("### 🛡️ Auditoría Gemini")
                st.write(aud_gemini)
            with col_aud3:
                st.markdown("### 🛡️ Certificación Final Claude")
                st.code(aud_claude)

        st.divider()

        # =========================================================
        # FASE 3: ESPECIALISTAS TRIPLES
        # =========================================================
        st.header("📢 Fase 3: Debate de Especialistas (Formato Ejecutivo)")
        col_esp1, col_esp2, col_esp3 = st.columns(3)
        
        with st.spinner("Generando reportes analíticos ejecutivos..."):
            
            res_oddsmaker = consultar_ia(GROK, aud_claude, api_key, "Oddsmaker (Grok). Analiza momios y probabilidad implícita. Máximo 2 viñetas concisas.", max_tokens=400)
            res_scout = consultar_ia(GEMINI, aud_claude, api_key, "Scout (Gemini). Analiza duelo abridor vs bateador y bullpen. Máximo 2 viñetas concisas.", max_tokens=400)
            res_contexto = consultar_ia(CLAUDE, aud_claude, api_key, "Contexto (Claude). Analiza impacto de clima, estadio y fatiga. Máximo 2 viñetas concisas.", max_tokens=400)
            
            with col_esp1:
                st.markdown("### 📊 Grok (Mercado)")
                st.info(res_oddsmaker)
            with col_esp2:
                st.markdown("### ⚾ Gemini (Matchup)")
                st.info(res_scout)
            with col_esp3:
                st.markdown("### 🌤️ Claude (Entorno)")
                st.info(res_contexto)

        st.divider()

        # =========================================================
        # FASE 4: JURADO Y VEREDICTO FINAL (Claude 3.5 Sonnet)
        # =========================================================
        st.subheader("🏆 Fase 4: Dictamen Supremo del Jurado (Claude 3.5 Sonnet)")
        
        bloque_final = f"DATA: {aud_claude}\nMERCADO: {res_oddsmaker}\nMATCHUP: {res_scout}\nENTORNO: {res_contexto}"
        
        with st.spinner("Claude dictando sentencia..."):
            
            role_jurado = (
                "Eres el Juez Supremo de Claude. Procesa los informes compresos. "
                "Entrega el veredicto final usando estrictamente esta estructura directa:\n\n"
                "- **Pick Oficial:** [Línea exacta y acción]\n"
                "- **Confianza:** [Alto/Medio/Bajo]\n"
                "- **Ventaja (+EV):** [Razón matemática clave en una frase]\n"
                "- **Riesgo:** [Factor crítico que tumba el pick]"
            )
            
            veredicto_maestro = consultar_ia(CLAUDE, bloque_final, api_key, role_jurado, max_tokens=600)
            
            st.success(veredicto_maestro)
            st.balloons()
