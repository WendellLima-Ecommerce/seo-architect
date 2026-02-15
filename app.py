import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="E-com SEO Architect", page_icon="🚀", layout="wide")

# Sua chave de API integrada
API_KEY = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILO VISUAL ---
st.markdown("""
<style>
    .stButton>button { width: 100%; background-color: #4F46E5; color: white; font-weight: bold; border-radius: 8px; }
    .main-header { font-size: 2.5rem; color: #4F46E5; font-weight: 700; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("E-com SEO Architect")
    st.markdown("---")
    if API_KEY.startswith("AIza"):
        st.success("✅ API Gemini Conectada")
    else:
        st.error("❌ Verifique a Chave")
    page = st.radio("Ir para:", ["Gerador de SEO", "Auditoria Rápida"])

# --- FUNÇÃO DE CONEXÃO (CORREÇÃO DO ERRO 404) ---
def call_gemini_stable(p_name, p_key, p_niche, p_plat, p_diff):
    try:
        # Configura a conexão usando a chave integrada
        genai.configure(api_key=API_KEY)
        
        # Forçamos o uso do modelo gemini-1.5-flash, que é o mais estável e rápido
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Atue como Especialista Sênior em SEO para E-commerce.
        Gere uma estrutura de SEO para o produto abaixo.
        
        PRODUTO: {p_name}
        PALAVRA-CHAVE: {p_key}
        NICHO: {p_niche}
        PLATAFORMA: {p_plat}
        DIFERENCIAIS: {p_diff}
        
        REGRAS:
        1. Title Tag: Max 60 chars.
        2. Meta Description: Max 155 chars.
        3. URL Slug: Amigável.
        
        RETORNE APENAS UM JSON VÁLIDO:
        {{
            "title_tag": "...",
            "meta_description": "...",
            "url_slug": "...",
            "h1_tag": "...",
            "lsi_keywords": "..."
        }}
        """
        
        # Realiza a chamada
        response = model.generate_content(prompt)
        
        # Limpeza de resposta para garantir que apenas o JSON seja lido
        clean_text = response.text.strip()
        if "```json" in clean_text:
            clean_text = clean_text.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_text:
            clean_text = clean_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(clean_text)
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
    
    diff = st.text_input("Diferenciais (Ex: Frete Grátis)")

    if st.button("✨ Gerar Estrutura Otimizada"):
        if name and key:
            with st.spinner("Conectando aos servidores estáveis do Google..."):
                res = call_gemini_stable(name, key, niche, plat, diff)
                
                if "error" in res:
                    st.error(f"Erro técnico: {res['error']}")
                else:
                    st.success("SEO Gerado!")
                    st.divider()
                    st.subheader("📋 Sugestão de SEO")
                    st.info(f"**Título:** {res['title_tag']}")
                    st.info(f"**Descrição:** {res['meta_description']}")
                    st.write(f"**URL:** {res['url_slug']}")
                    st.caption(f"**LSI:** {res['lsi_keywords']}")
                    
                    df = pd.DataFrame([res])
                    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")
        else:
            st.warning("Preencha o Nome e a Palavra-chave.")

else:
    st.markdown('<div class="main-header">Auditoria Rápida</div>', unsafe_allow_html=True)
    st.write("Verifique se o seu título atual segue as normas do Google.")
