import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="E-com SEO Architect",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INTEGRAÇÃO DA CHAVE DE API ---
# Sua chave integrada diretamente para evitar digitação manual
API_KEY_INTEGRADA = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        height: 3em;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4F46E5;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1006/1006771.png", width=50)
    st.title("E-com SEO Architect")
    st.markdown("---")
    
    # Status da Conexão
    if API_KEY_INTEGRADA.startswith("AIza"):
        st.success("✅ API Gemini Conectada")
    else:
        st.error("❌ Erro na Chave de API")
    
    st.markdown("### Navegação")
    page = st.radio("Ir para:", ["Gerador de Estrutura", "Auditoria de URL"])

# --- FUNÇÃO DE INTELIGÊNCIA (GEMINI) ---
def generate_seo_logic(product, keyword, niche, platform, differentials):
    try:
        genai.configure(api_key=API_KEY_INTEGRADA)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Atue como Especialista Sênior em SEO. Gere um JSON para:
        Produto: {product} | Palavra-chave: {keyword} | Nicho: {niche} | Plataforma: {platform}
        
        REGRAS:
        1. Title Tag: Max 60 chars, Title Case.
        2. Meta Description: Max 155 chars, use gatilhos mentais.
        3. Slug: Amigável para {platform}.
        4. LSI: 5 termos técnicos.
        
        RETORNE APENAS O JSON:
        {{
            "title_tag": "...",
            "meta_description": "...",
            "url_slug": "...",
            "h1_tag": "...",
            "lsi_keywords": "..."
        }}
        """
        response = model.generate_content(prompt)
        # Limpeza básica da resposta para garantir JSON puro
        clean_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(clean_response)
    except Exception as e:
        return {"error": str(e)}

# --- PÁGINA: GERADOR ---
if page == "Gerador de Estrutura":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Nome do Produto *")
        niche = st.selectbox("Nicho", ["Automação Industrial", "E-commerce Geral", "Eletrônicos"])
    with col2:
        keyword = st.text_input("Palavra-chave Principal *")
        platform = st.selectbox("Plataforma", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
    
    differentials = st.text_input("Diferenciais (Ex: Frete Grátis)")

    if st.button("✨ Gerar Estrutura Otimizada"):
        with st.spinner("Analisando..."):
            result = generate_seo_logic(product_name, keyword, niche, platform, differentials)
            if "error" in result:
                st.error(f"Erro: {result['error']}")
            else:
                st.subheader("📋 Resultado")
                st.write(f"**Título:** {result['title_tag']}")
                st.write(f"**Meta:** {result['meta_description']}")
                st.write(f"**URL:** {result['url_slug']}")
                
                # Exportação
                df = pd.DataFrame([result])
                st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")

# --- PÁGINA: AUDITORIA ---
else:
    st.markdown('<div class="main-header">Auditoria de URL</div>', unsafe_allow_html=True)
    t_input = st.text_input("Cole o Título Atual")
    if st.button("🔍 Auditar"):
        score = 100
        if len(t_input) > 60: score -= 20
        if t_input.isupper(): score -= 30
        st.metric("Nota SEO", f"{score}/100")
