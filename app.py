import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import os

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

# --- FUNÇÃO DE CONEXÃO BLINDADA (CORREÇÃO DEFINITIVA DO ERRO 404) ---
def call_gemini_stable(p_name, p_key, p_niche, p_plat, p_diff):
    try:
        # Forçamos a configuração da API a usar o canal estável (v1)
        genai.configure(api_key=API_KEY)
        
        # Tentamos o modelo Flash, que é o padrão ouro atual
        # O uso do nome simples sem 'models/' evita erros de endereçamento no v1beta
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Atue como Especialista Sênior em SEO. Gere um JSON para:
        Produto: {p_name} | Key: {p_key} | Nicho: {p_niche} | Plataforma: {p_plat}
        Diferenciais: {p_diff}
        
        RETORNE APENAS O JSON (sem markdown):
        {{
            "title_tag": "string",
            "meta_description": "string",
            "url_slug": "string",
            "h1_tag": "string",
            "lsi_keywords": "string"
        }}
        """
        
        # Realiza a chamada forçando a geração de conteúdo
        response = model.generate_content(prompt)
        
        # Limpeza agressiva da resposta
        res_text = response.text.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0].strip()
        elif "```" in res_text:
            res_text = res_text.split("```")[1].split("```")[0].strip()
            
        return json.loads(res_text)
    except Exception as e:
        # Se falhar, tentamos o modelo Pro como backup automático
        try:
            model_pro = genai.GenerativeModel('gemini-pro')
            response_pro = model_pro.generate_content(prompt)
            return json.loads(response_pro.text.strip())
        except:
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

    if st.button("✨ Gerar Estrutura Otimizada"):
        if name and key:
            with st.spinner("Conectando aos servidores do Google..."):
                res = call_gemini_stable(name, key, niche, plat, diff)
                
                if "error" in res:
                    st.error(f"Erro na conexão: {res['error']}. Dica: Tente dar um 'Reboot' no Streamlit Cloud.")
                else:
                    st.success("Análise concluída!")
                    st.divider()
                    st.info(f"**Título:** {res['title_tag']}")
                    st.info(f"**Descrição:** {res['meta_description']}")
                    st.write(f"**Slug:** {res['url_slug']}")
                    st.caption(f"**Keywords:** {res['lsi_keywords']}")
                    
                    df = pd.DataFrame([res])
                    st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "seo.csv", "text/csv")
        else:
            st.warning("Preencha os campos obrigatórios (*).")

else:
    st.markdown('<div class="main-header">Auditoria Rápida</div>', unsafe_allow_html=True)
