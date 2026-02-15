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
# Sua chave configurada para acesso automático
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
        font-weight: bold;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4F46E5;
        font-weight: 700;
        margin-bottom: 20px;
    }
    code {
        color: #4F46E5 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1006/1006771.png", width=50)
    st.title("E-com SEO Architect")
    st.markdown("---")
    
    if API_KEY_INTEGRADA.startswith("AIza"):
        st.success("✅ API Gemini Conectada")
    else:
        st.error("❌ Chave de API Inválida")
    
    st.markdown("### Navegação")
    page = st.radio("Ir para:", ["Gerador de Estrutura", "Auditoria de URL"])

# --- FUNÇÃO DE INTELIGÊNCIA (AJUSTADA PARA GEMINI-PRO) ---
def generate_seo_logic(product, keyword, niche, platform, differentials):
    try:
        genai.configure(api_key=API_KEY_INTEGRADA)
        # Ajuste para modelo estável para evitar Erro 404
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""
        Atue como Especialista Sênior em SEO para E-commerce.
        Gere uma estrutura de SEO para o produto abaixo.
        
        DADOS:
        Produto: {product}
        Palavra-chave: {keyword}
        Nicho: {niche}
        Plataforma: {platform}
        Diferenciais: {differentials}
        
        REGRAS:
        1. Title Tag: Max 60 chars, Title Case.
        2. Meta Description: Max 155 chars, use gatilhos mentais.
        3. Slug: Amigável para a plataforma {platform}.
        4. LSI: 5 termos técnicos separados por vírgula.
        
        RETORNE APENAS UM JSON VÁLIDO (sem blocos de código markdown):
        {{
            "title_tag": "...",
            "meta_description": "...",
            "url_slug": "...",
            "h1_tag": "...",
            "lsi_keywords": "..."
        }}
        """
        response = model.generate_content(prompt)
        
        # Limpeza de resposta para tratar possíveis blocos de código da IA
        json_text = response.text.strip()
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(json_text)
    except Exception as e:
        return {"error": str(e)}

# --- PÁGINA: GERADOR ---
if page == "Gerador de Estrutura":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Nome do Produto/Categoria *", placeholder="Ex: Inversor de Frequência WEG")
        niche = st.selectbox("Nicho de Mercado", ["Automação Industrial", "E-commerce Geral", "Eletrônicos", "Moda"])
    with col2:
        keyword_input = st.text_input("Palavra-chave Principal *", placeholder="Ex: Inversor Monofásico")
        platform_input = st.selectbox("Plataforma da Loja", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
    
    diff_input = st.text_input("Diferenciais (Ex: Frete Grátis, 2 anos de garantia)")

    if st.button("✨ Gerar Estrutura Otimizada"):
        if not product_name or not keyword_input:
            st.warning("Por favor, preencha os campos obrigatórios (*).")
        else:
            with st.spinner("Analisando dados e gerando estratégia de SEO..."):
                result = generate_seo_logic(product_name, keyword_input, niche, platform_input, diff_input)
                
                if "error" in result:
                    st.error(f"Erro na análise: {result['error']}")
                else:
                    st.success("Estrutura gerada com sucesso!")
                    st.divider()
                    
                    res_col1, res_col2 = st.columns([2, 1])
                    with res_col1:
                        st.subheader("📋 Estrutura Sugerida")
                        st.write("**Title Tag:**")
                        st.code(result['title_tag'], language="text")
                        
                        st.write("**Meta Description:**")
                        st.code(result['meta_description'], language="text")
                        
                        st.write("**URL Slug:**")
                        st.code(result['url_slug'], language="text")
                    
                    with res_col2:
                        st.subheader("🔍 Detalhes Técnicos")
                        st.info(f"**H1:** {result['h1_tag']}")
                        st.write("**Palavras-chave LSI:**")
                        st.caption(result['lsi_keywords'])
                    
                    # Botão para Download
                    df = pd.DataFrame([result])
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Baixar Relatório CSV", csv_data, "seo_expert.csv", "text/csv")

# --- PÁGINA: AUDITORIA ---
else:
    st.markdown('<div class="main-header">Auditoria de URL</div>', unsafe_allow_html=True)
    st.write("Análise rápida de conformidade com as normas do Google.")
    
    audit_title = st.text_input("Título Atual para Auditoria")
    if st.button("🔍 Auditar Agora"):
        if audit_title:
            score = 100
            checks = []
            
            if len(audit_title) > 60:
                score -= 20
                checks.append("❌ Título muito longo (ideal até 60 caracteres).")
            if audit_title.isupper():
                score -= 30
                checks.append("❌ Título em CAIXA ALTA (prejudica o ranqueamento).")
            
            st.metric("Nota de Saúde SEO", f"{score}/100")
            for check in checks:
                st.write(check)
            if score == 100:
                st.success("✅ Título dentro das normas básicas!")
