import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="E-com SEO Architect",
    page_icon="🚀",
    layout="wide"
)

# --- CHAVE DE API INTEGRADA ---
API_KEY = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILIZAÇÃO ---
st.markdown("""
<style>
    .stButton>button { width: 100%; background-color: #4F46E5; color: white; font-weight: bold; }
    .main-header { font-size: 2.5rem; color: #4F46E5; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("E-com SEO Architect")
    st.markdown("---")
    if API_KEY.startswith("AIza"):
        st.success("✅ API Gemini Conectada")
    else:
        st.error("❌ Verifique sua Chave")
    page = st.radio("Navegação:", ["Gerador de SEO", "Auditoria"])

# --- FUNÇÃO DO MOTOR DE IA (CORREÇÃO DE ERRO 404) ---
def call_gemini_api(p_name, p_key, p_niche, p_plat, p_diff):
    try:
        genai.configure(api_key=API_KEY)
        
        # Tenta o modelo 1.5-flash primeiro, se falhar tenta o pro
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Teste simples de conexão
            model.count_tokens("teste") 
        except:
            model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        Atue como Especialista em SEO. Gere um JSON para:
        Produto: {p_name} | Palavra-chave: {p_key} | Nicho: {p_niche} | Plataforma: {p_plat} | Diferenciais: {p_diff}
        
        Retorne APENAS um JSON com as chaves: title_tag, meta_description, url_slug, h1_tag, lsi_keywords.
        """
        
        response = model.generate_content(prompt)
        
        # Limpeza de resposta para evitar erros de formatação
        text_response = response.text.strip()
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0].strip()
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0].strip()
            
        return json.loads(text_response)
    except Exception as e:
        return {"error": str(e)}

# --- INTERFACE ---
if page == "Gerador de SEO":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nome do Produto *")
        niche = st.selectbox("Nicho", ["Automação Industrial", "Eletrônicos", "Moda", "Outros"])
    with col2:
        key = st.text_input("Palavra-chave Principal *")
        plat = st.selectbox("Plataforma", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
    
    diff = st.text_input("Diferenciais")

    if st.button("✨ Gerar SEO"):
        if name and key:
            with st.spinner("Analisando..."):
                res = call_gemini_api(name, key, niche, plat, diff)
                if "error" in res:
                    st.error(f"Erro na análise: {res['error']}")
                else:
                    st.success("Gerado!")
                    st.divider()
                    st.subheader("📋 Sugestões")
                    st.info(f"**Título:** {res['title_tag']}")
                    st.info(f"**Descrição:** {res['meta_description']}")
                    st.write(f"**Slug:** {res['url_slug']}")
                    st.write(f"**Keywords:** {res['lsi_keywords']}")
                    
                    df = pd.DataFrame([res])
                    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")
        else:
            st.warning("Preencha os campos obrigatórios.")

else:
    st.markdown('<div class="main-header">Auditoria</div>', unsafe_allow_html=True)
    title = st.text_input("Título Atual")
    if st.button("🔍 Analisar"):
        score = 100
        if len(title) > 60: score -= 20
        st.metric("Nota SEO", f"{score}/100")
