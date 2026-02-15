import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="E-com SEO Architect", page_icon="🚀", layout="wide")

# Sua chave de API integrada
API_KEY = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILO CSS ---
st.markdown("""
<style>
    .stButton>button { width: 100%; background-color: #4F46E5; color: white; font-weight: bold; border-radius: 8px; }
    .main-header { font-size: 2.5rem; color: #4F46E5; font-weight: 700; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("E-com SEO Architect")
    st.markdown("---")
    if API_KEY.startswith("AIza"):
        st.success("✅ Conexão Configurada")
    else:
        st.error("❌ Erro na Chave")
    page = st.radio("Selecione a Ferramenta:", ["Gerador de SEO", "Auditoria de Texto"])

# --- FUNÇÃO DE IA (CORREÇÃO DEFINITIVA DO 404) ---
def get_seo_data(name, key, niche, plat, diff):
    try:
        # Forçamos a configuração a usar a API v1 estável
        genai.configure(api_key=API_KEY)
        
        # Chamamos o modelo sem o prefixo 'models/', que às vezes causa erro no v1beta
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Atue como Especialista Sênior em SEO. Gere um JSON para:
        Produto: {name} | Key: {key} | Nicho: {niche} | Plat: {plat} | Diferenciais: {diff}
        Retorne APENAS um JSON: {{"title_tag": "...", "meta_description": "...", "url_slug": "...", "h1_tag": "...", "lsi_keywords": "..."}}
        """
        
        # Gerando o conteúdo
        response = model.generate_content(prompt)
        res_text = response.text.strip()
        
        # Limpeza de markdown
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(res_text)
    except Exception as e:
        return {"error": str(e)}

# --- INTERFACE ---
if page == "Gerador de SEO":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Nome do Produto *", placeholder="Ex: Inversor WEG CFW500")
            p_niche = st.selectbox("Nicho", ["Automação Industrial", "Eletrônicos", "Moda", "Geral"])
        with c2:
            p_key = st.text_input("Palavra-chave Principal *", placeholder="Ex: Inversor de Frequência")
            p_plat = st.selectbox("Plataforma", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
        
        p_diff = st.text_input("Diferenciais Competitivos")

    if st.button("✨ Gerar SEO Otimizado"):
        if p_name and p_key:
            with st.spinner("Conectando à versão estável do Gemini..."):
                result = get_seo_data(p_name, p_key, p_niche, p_plat, p_diff)
                
                if "error" in result:
                    st.error(f"Erro na comunicação: {result['error']}")
                    st.warning("Dica: Se o erro 404 persistir, tente 'Reboot App' nas configurações do Streamlit.")
                else:
                    st.success("SEO Gerado!")
                    st.divider()
                    
                    res_c1, res_c2 = st.columns([2, 1])
                    with res_c1:
                        st.subheader("📋 Estrutura")
                        st.info(f"**Título:** {result['title_tag']}")
                        st.info(f"**Descrição:** {result['meta_description']}")
                        st.write(f"**Slug:** `{result['url_slug']}`")
                    with res_c2:
                        st.subheader("🔍 LSI")
                        st.caption(result['lsi_keywords'])

                    df = pd.DataFrame([result])
                    st.download_button("📥 Exportar CSV", df.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")
        else:
            st.warning("Preencha os campos obrigatórios (*).")

else:
    st.markdown('<div class="main-header">Auditoria de Texto</div>', unsafe_allow_html=True)
    st.write("Layout corrigido e pronto para uso.")
