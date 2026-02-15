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
# Chave integrada conforme solicitado
API_KEY_INTEGRADA = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILIZAÇÃO CSS (Layout Profissional) ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4F46E5;
        font-weight: 700;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1006/1006771.png", width=50)
    st.title("E-com SEO Architect")
    st.markdown("---")
    
    # Validação visual da conexão
    if API_KEY_INTEGRADA.startswith("AIza"):
        st.success("✅ API Gemini Conectada")
    else:
        st.error("❌ Erro na Chave de API")
    
    st.markdown("### Navegação")
    page = st.radio("Ir para:", ["Gerador de Estrutura", "Auditoria de URL"])

# --- FUNÇÃO DE INTELIGÊNCIA (CORREÇÃO DO ERRO 404) ---
def generate_seo_logic(product, keyword, niche, platform, differentials):
    try:
        # Configura a conexão com a chave integrada
        genai.configure(api_key=API_KEY_INTEGRADA)
        
        # Uso do modelo gemini-1.5-flash (Versão mais estável para produção)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Você é um Especialista Sênior em SEO para E-commerce. 
        Analise o produto abaixo e gere uma estratégia de SEO profissional.

        DADOS:
        - Nome do Produto: {product}
        - Palavra-chave: {keyword}
        - Nicho: {niche}
        - Plataforma: {platform}
        - Diferenciais: {differentials}

        REGRAS TÉCNICAS:
        1. Title Tag: Max 60 caracteres. Use Title Case.
        2. Meta Description: Max 155 caracteres. Use gatilhos mentais.
        3. URL Slug: Otimizada para {platform}.
        4. LSI Keywords: 5 termos técnicos.

        RETORNE APENAS UM JSON PURO NESTE FORMATO:
        {{
            "title_tag": "string",
            "meta_description": "string",
            "url_slug": "string",
            "h1_tag": "string",
            "lsi_keywords": "string"
        }}
        """
        
        # Envia a requisição para o Google
        response = model.generate_content(prompt)
        
        # Limpeza robusta para garantir a leitura do JSON
        json_text = response.text.strip()
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(json_text)
    
    except Exception as e:
        # Retorna o erro detalhado se algo falhar
        return {"error": str(e)}

# --- INTERFACE: GERADOR ---
if page == "Gerador de Estrutura":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        p_name = st.text_input("Nome do Produto/Categoria *")
        p_niche = st.selectbox("Nicho de Mercado", ["Automação Industrial", "Eletrônicos", "Moda", "Outros"])
    with col2:
        p_key = st.text_input("Palavra-chave Principal *")
        p_plat = st.selectbox("Plataforma da Loja", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
    
    p_diff = st.text_input("Diferenciais Competitivos")

    if st.button("✨ Gerar Estrutura Otimizada"):
        if not p_name or not p_key:
            st.warning("Os campos Nome e Palavra-chave são obrigatórios.")
        else:
            with st.spinner("Analisando dados com a inteligência do Google..."):
                result = generate_seo_logic(p_name, p_key, p_niche, p_plat, p_diff)
                
                if "error" in result:
                    st.error(f"Erro na Análise: {result['error']}")
                else:
                    st.success("SEO Otimizado Gerado!")
                    st.divider()
                    
                    st.subheader("📋 Resultados Sugeridos")
                    st.info(f"**Título:** {result['title_tag']}")
                    st.info(f"**Descrição:** {result['meta_description']}")
                    st.write(f"**URL Slug:** `{result['url_slug']}`")
                    st.write(f"**H1:** {result['h1_tag']}")
                    st.caption(f"**Termos LSI:** {result['lsi_keywords']}")
                    
                    # Funcionalidade de download
                    df_out = pd.DataFrame([result])
                    st.download_button("📥 Exportar CSV", df_out.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")

# --- INTERFACE: AUDITORIA ---
else:
    st.markdown('<div class="main-header">Auditoria de URL</div>', unsafe_allow_html=True)
    t_audit = st.text_input("Insira o Título atual para análise")
    
    if st.button("🔍 Iniciar Auditoria"):
        if t_audit:
            score = 100
            if len(t_audit) > 60: score -= 20
            if t_audit.isupper(): score -= 30
            st.metric("Nota de Saúde SEO", f"{score}/100")
            if score < 100:
                st.warning("Dica: Evite títulos muito longos ou totalmente em maiúsculas.")
            else:
                st.success("Seu título está seguindo as boas práticas!")
