import streamlit as st
import google.generativeai as genai
import pandas as pd
import json

# --- CONFIGURAÇÃO DA PÁGINA (Sempre no topo) ---
st.set_page_config(page_title="E-com SEO Architect", page_icon="🚀", layout="wide")

# Chave integrada conforme solicitado
API_KEY = "AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY"

# --- ESTILO CSS ---
st.markdown("""
<style>
    .stButton>button { width: 100%; background-color: #4F46E5; color: white; font-weight: bold; border-radius: 8px; }
    .main-header { font-size: 2.5rem; color: #4F46E5; font-weight: 700; margin-bottom: 20px; }
    .card { background-color: #1E1E1E; padding: 20px; border-radius: 10px; border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR FIXA ---
with st.sidebar:
    st.title("E-com SEO Architect")
    st.markdown("---")
    if API_KEY.startswith("AIza"):
        st.success("✅ Conexão Configurada")
    else:
        st.error("❌ Erro na Chave")
    
    st.markdown("### Navegação")
    page = st.radio("Selecione a Ferramenta:", ["Gerador de SEO", "Auditoria de Texto"])

# --- FUNÇÃO DE IA COM FALLBACK (CORREÇÃO ERRO 404) ---
def get_seo_data(name, key, niche, plat, diff):
    try:
        genai.configure(api_key=API_KEY)
        
        # Usamos o identificador estável que evita o erro de v1beta
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Atue como Especialista Sênior em SEO. Gere um JSON para:
        Produto: {name} | Key: {key} | Nicho: {niche} | Plat: {plat} | Diferenciais: {diff}
        Retorne APENAS um JSON: {{"title_tag": "...", "meta_description": "...", "url_slug": "...", "h1_tag": "...", "lsi_keywords": "..."}}
        """
        
        response = model.generate_content(prompt)
        res_text = response.text.strip()
        
        # Limpeza de markdown caso a IA envie
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(res_text)
    except Exception as e:
        return {"error": str(e)}

# --- LOGICA DAS PÁGINAS ---
if page == "Gerador de SEO":
    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)
    
    # Grid de entrada
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Nome do Produto *")
            p_niche = st.selectbox("Nicho", ["Automação Industrial", "Eletrônicos", "Moda", "Geral"])
        with c2:
            p_key = st.text_input("Palavra-chave Principal *")
            p_plat = st.selectbox("Plataforma", ["Nuvemshop", "Shopify", "Vtex", "Outra"])
        
        p_diff = st.text_input("Diferenciais Competitivos")

    st.markdown("---")

    if st.button("✨ Gerar SEO Otimizado"):
        if p_name and p_key:
            with st.spinner("A IA está processando..."):
                result = get_seo_data(p_name, p_key, p_niche, p_plat, p_diff)
                
                if "error" in result:
                    # Mostra o erro sem quebrar a página
                    st.error(f"Houve um problema na comunicação: {result['error']}")
                    st.info("Dica: Verifique se sua chave tem acesso ao modelo 1.5 Flash no Google AI Studio.")
                else:
                    st.success("SEO Gerado com Sucesso!")
                    
                    # Exibição organizada
                    res_c1, res_c2 = st.columns([2, 1])
                    with res_c1:
                        st.subheader("📋 Estrutura Sugerida")
                        st.write(f"**Título:** {result['title_tag']}")
                        st.write(f"**Descrição:** {result['meta_description']}")
                        st.write(f"**Slug:** `{result['url_slug']}`")
                    with res_c2:
                        st.subheader("🔍 Dados Técnicos")
                        st.write(f"**H1:** {result['h1_tag']}")
                        st.caption(f"**Keywords LSI:** {result['lsi_keywords']}")

                    df = pd.DataFrame([result])
                    st.download_button("📥 Exportar CSV", df.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")
        else:
            st.warning("Preencha os campos obrigatórios (*).")

else:
    st.markdown('<div class="main-header">Auditoria Rápida</div>', unsafe_allow_html=True)
    st.write("Esta página está pronta para receber sua lógica de análise de textos.")
    t_input = st.text_input("Cole o texto atual para auditar:")
    if st.button("Analisar"):
        st.write(f"Analisando: {t_input}")
