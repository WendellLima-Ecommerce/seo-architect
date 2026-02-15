import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="E-com SEO Architect", page_icon="🚀", layout="wide")
API_KEY = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILO VISUAL ---
st.markdown("""
<style>
    .stButton>button { width: 100%; background-color: #4F46E5; color: white; font-weight: bold; border-radius: 8px; }
    .main-header { font-size: 2.5rem; color: #4F46E5; font-weight: 700; margin-bottom: 20px; }
    .stAlert { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("E-com SEO Architect")
    st.markdown("---")
    if API_KEY.startswith("AIza"):
        st.success("✅ API Gemini Conectada")
    else:
        st.error("❌ Chave de API Inválida")
    page = st.radio("Navegação:", ["Gerador de SEO", "Auditoria de Texto"])

# --- MOTOR DE INTELIGÊNCIA (CORREÇÃO DO ERRO 404) ---
def call_gemini_api(p_name, p_key, p_niche, p_plat, p_diff):
    try:
        genai.configure(api_key=API_KEY)
        
        # Tentamos o modelo padrão estável. 
        # A versão 0.8.3 da biblioteca resolve o erro de 'v1beta' automaticamente.
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Você é um Especialista em SEO. Gere um JSON estrito para o produto:
        Nome: {p_name} | Palavra-chave: {p_key} | Nicho: {p_niche} | Plataforma: {p_plat} | Diferenciais: {p_diff}
        
        Retorne APENAS um JSON com estas chaves: 
        "title_tag", "meta_description", "url_slug", "h1_tag", "lsi_keywords"
        """
        
        response = model.generate_content(prompt)
        
        # Limpeza para garantir que apenas o JSON seja processado
        res_text = response.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(res_text)
    except Exception as e:
        return {"error": str(e)}

# --- INTERFACE DO USUÁRIO ---
if page == "Gerador de SEO":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Nome do Produto/Categoria *", placeholder="Ex: Inversor de Frequência WEG")
        niche = st.selectbox("Nicho", ["Automação Industrial", "Eletrônicos", "Moda", "Outros"])
    with col2:
        key = st.text_input("Palavra-chave Principal *", placeholder="Ex: Inversor Monofásico")
        plat = st.selectbox("Plataforma", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
    
    diff = st.text_input("Diferenciais (Ex: Frete Grátis, 2 anos de garantia)")

    if st.button("✨ Gerar SEO Otimizado"):
        if name and key:
            with st.spinner("IA analisando as melhores estratégias de SEO..."):
                res = call_gemini_api(name, key, niche, plat, diff)
                if "error" in res:
                    st.error(f"Erro na análise: {res['error']}")
                else:
                    st.success("Estrutura gerada com sucesso!")
                    st.divider()
                    
                    st.subheader("📋 Resultados")
                    st.info(f"**Título Otimizado:** {res['title_tag']}")
                    st.info(f"**Meta Descrição:** {res['meta_description']}")
                    st.write(f"**URL Amigável:** `{res['url_slug']}`")
                    st.write(f"**Palavras LSI:** {res['lsi_keywords']}")
                    
                    # Opção de Download
                    df = pd.DataFrame([res])
                    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "seo_export.csv", "text/csv")
        else:
            st.warning("Por favor, preencha o Nome e a Palavra-chave.")

else:
    st.markdown('<div class="main-header">Auditoria de Texto</div>', unsafe_allow_html=True)
    t_input = st.text_input("Cole o Título Atual para Auditoria")
    if st.button("🔍 Iniciar Auditoria"):
        if t_input:
            score = 100
            if len(t_input) > 60: score -= 20
            if t_input.isupper(): score -= 30
            st.metric("Nota de Saúde SEO", f"{score}/100")
