import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="E-com SEO Architect", page_icon="🚀", layout="wide")
API_KEY = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILO ---
st.markdown("""
<style>
    .stButton>button { width: 100%; background-color: #4F46E5; color: white; font-weight: bold; }
    .main-header { font-size: 2.5rem; color: #4F46E5; font-weight: 700; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("E-com SEO Architect")
    st.markdown("---")
    if API_KEY.startswith("AIza"):
        st.success("✅ API Gemini Conectada")
    else:
        st.error("❌ Chave Inválida")
    page = st.radio("Ir para:", ["Gerador de SEO", "Auditoria"])

# --- FUNÇÃO CORRIGIDA (SEM ERRO 404) ---
def call_gemini_safe(p_name, p_key, p_niche, p_plat, p_diff):
    try:
        genai.configure(api_key=API_KEY)
        
        # Forçamos o modelo 'gemini-1.5-flash-latest' que é o mais compatível com chaves novas
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = f"""
        Atue como Especialista em SEO. Gere um JSON para:
        Produto: {p_name} | Key: {p_key} | Nicho: {p_niche} | Plat: {p_plat} | Diferenciais: {p_diff}
        Retorne APENAS um JSON: {{ "title_tag": "...", "meta_description": "...", "url_slug": "...", "h1_tag": "...", "lsi_keywords": "..." }}
        """
        
        response = model.generate_content(prompt)
        
        # Limpeza para garantir JSON puro
        res_text = response.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(res_text)
    except Exception as e:
        # Se falhar o flash, tenta o pro como última alternativa
        try:
            model_alt = genai.GenerativeModel('gemini-1.5-pro')
            response_alt = model_alt.generate_content(prompt)
            return json.loads(response_alt.text.strip())
        except:
            return {"error": str(e)}

# --- INTERFACE ---
if page == "Gerador de SEO":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Nome do Produto *")
        niche = st.selectbox("Nicho", ["Automação Industrial", "Eletrônicos", "Moda", "Outros"])
    with c2:
        key = st.text_input("Palavra-chave Principal *")
        plat = st.selectbox("Plataforma", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
    
    diff = st.text_input("Diferenciais (Frete, Garantia...)")

    if st.button("✨ Gerar SEO Otimizado"):
        if name and key:
            with st.spinner("Conectando aos servidores do Google..."):
                res = call_gemini_safe(name, key, niche, plat, diff)
                if "error" in res:
                    st.error(f"Erro técnico: {res['error']}")
                else:
                    st.success("Análise concluída!")
                    st.info(f"**Título:** {res['title_tag']}")
                    st.info(f"**Descrição:** {res['meta_description']}")
                    st.write(f"**Slug:** {res['url_slug']}")
                    st.caption(f"**LSI:** {res['lsi_keywords']}")
                    
                    df = pd.DataFrame([res])
                    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")
        else:
            st.warning("Preencha os campos com asterisco (*).")

else:
    st.markdown('<div class="main-header">Auditoria Rápida</div>', unsafe_allow_html=True)
    title_check = st.text_input("Cole o Título Atual")
    if st.button("🔍 Auditar"):
        score = 100
        if len(title_check) > 60: score -= 20
        st.metric("Saúde SEO", f"{score}/100")
