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



# --- ESTILIZAÇÃO CSS (Visual Dark/Tech) ---

st.markdown("""

<style>

    .stButton>button {

        width: 100%;

        background-color: #4F46E5;

        color: white;

        border-radius: 8px;

        height: 3em;

    }

    .stTextInput>div>div>input {

        border-radius: 8px;

    }

    .main-header {

        font-size: 2.5rem;

        color: #4F46E5;

        font-weight: 700;

    }

</style>

""", unsafe_allow_html=True)



# --- CONFIGURAÇÃO DA API (SIDEBAR) ---

with st.sidebar:

    st.image("https://cdn-icons-png.flaticon.com/512/1006/1006771.png", width=50)

    st.title("E-com SEO Architect")

    st.markdown("---")

    

    # Campo para chave de API (Segurança)

    api_key = st.text_input("AIzaSyDlXoCn3GLsgYgmRMxhiU702oxD4EEWuYY", type="password")

    

    st.markdown("### Navegação")

    page = st.radio("Ir para:", ["Gerador de Estrutura", "Auditoria de URL"])

    

    st.info("💡 Dica: Selecione a plataforma correta para garantir a URL amigável ideal.")



# --- FUNÇÃO DO CÉREBRO (AI) ---

def generate_seo(product, keyword, niche, platform, differentials, key):

    genai.configure(api_key=key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    

    prompt = f"""

    Atue como um Especialista Sênior em SEO para E-commerce.

    Sua tarefa é gerar uma estrutura JSON para o seguinte produto:

    

    DADOS:

    - Produto: {product}

    - Palavra-chave: {keyword}

    - Nicho: {niche}

    - Plataforma: {platform}

    - Diferenciais: {differentials}

    

    REGRAS OBRIGATÓRIAS:

    1. Title Tag: Max 60 chars. Title Case. Padrão: Produto + Specs + Marca.

    2. Meta Description: Max 155 chars. Use gatilhos mentais (Frete, Oferta).

    3. Slug:

       - Se Shopify: /products/slug-com-hifens

       - Se Vtex: /slug-com-hifens

       - Padrão: /slug-com-hifens

    4. LSI Keywords: 5 termos técnicos separados por vírgula.

    5. H1: Nome limpo do produto.

    

    RETORNE APENAS UM JSON VÁLIDO NESTE FORMATO:

    {{

        "title_tag": "...",

        "meta_description": "...",

        "url_slug": "...",

        "h1_tag": "...",

        "lsi_keywords": "..."

    }}

    """

    

    try:

        response = model.generate_content(prompt)

        return json.loads(response.text.strip().replace('```json', '').replace('```', ''))

    except Exception as e:

        return {"error": str(e)}



# --- PÁGINA 1: GERADOR ---

if page == "Gerador de Estrutura":

    st.markdown('<div class="main-header">Gerador de Estrutura SEO</div>', unsafe_allow_html=True)

    st.markdown("Crie títulos e descrições otimizados para o Google em segundos.")

    

    col1, col2 = st.columns(2)

    

    with col1:

        product_name = st.text_input("Nome do Produto *", placeholder="Ex: Inversor WEG CFW500...")

        niche = st.selectbox("Nicho de Mercado", ["Automação Industrial", "Moda", "Eletrônicos", "Casa e Decor", "Outro"])

        differentials = st.text_input("Diferenciais", placeholder="Ex: Frete Grátis, 10% Off, Pronta Entrega")



    with col2:

        keyword = st.text_input("Palavra-chave Principal *", placeholder="Ex: Inversor de Frequência")

        platform = st.selectbox("Plataforma da Loja", ["Nuvemshop", "Shopify", "Vtex", "WooCommerce", "Outra"])

    

    if st.button("✨ Gerar Estrutura Otimizada"):

        if not api_key:

            st.error("Por favor, insira sua Chave de API na barra lateral.")

        elif not product_name:

            st.warning("Preencha o nome do produto.")

        else:

            with st.spinner("A IA está analisando as melhores palavras-chave..."):

                result = generate_seo(product_name, keyword, niche, platform, differentials, api_key)

                

                if "error" in result:

                    st.error("Erro ao conectar com Gemini. Verifique sua chave.")

                else:

                    st.success("Estrutura gerada com sucesso!")

                    

                    # Exibição dos Resultados

                    st.subheader("📋 Resultado Final")

                    

                    c1, c2 = st.columns([3, 1])

                    with c1:

                        st.markdown(f"**Title Tag ({len(result['title_tag'])} chars):**")

                        st.code(result['title_tag'], language="text")

                        

                        st.markdown(f"**Meta Description ({len(result['meta_description'])} chars):**")

                        st.code(result['meta_description'], language="text")

                        

                        st.markdown("**URL Slug:**")

                        st.code(result['url_slug'], language="text")



                    with c2:

                        st.markdown("**Palavras-chave LSI:**")

                        st.info(result['lsi_keywords'])

                        

                        st.markdown("**H1 Sugerido:**")

                        st.write(result['h1_tag'])



                    # Botão CSV

                    df = pd.DataFrame([result])

                    csv = df.to_csv(index=False).encode('utf-8')

                    st.download_button(

                        label="📥 Baixar Relatório (CSV)",

                        data=csv,

                        file_name='seo_estrutura.csv',

                        mime='text/csv',

                    )



# --- PÁGINA 2: AUDITORIA ---

elif page == "Auditoria de URL":

    st.markdown('<div class="main-header">Auditoria de Conteúdo</div>', unsafe_allow_html=True)

    st.write("Compare seus dados atuais com as regras do Google.")

    

    col1, col2 = st.columns(2)

    with col1:

        current_title = st.text_area("Título Atual", height=100)

    with col2:

        current_meta = st.text_area("Meta Descrição Atual", height=100)

        

    if st.button("🔍 Auditar Agora"):

        score = 100

        issues = []

        

        # Lógica de Auditoria (Python Puro - Mais rápido que IA)

        if len(current_title) > 60:

            score -= 20

            issues.append(f"⚠️ Título muito longo: {len(current_title)} caracteres (Ideal: < 60)")

        elif len(current_title) < 30:

            score -= 10

            issues.append(f"⚠️ Título muito curto: {len(current_title)} caracteres")

            

        if len(current_meta) > 160:

            score -= 20

            issues.append(f"⚠️ Meta Descrição muito longa: {len(current_meta)} caracteres")

        if current_title.isupper():

            score -= 30

            issues.append("⛔ Título em CAIXA ALTA (Gritando). Google penaliza isso.")

            

        # Exibição

        st.divider()

        c1, c2 = st.columns([1, 2])

        

        with c1:

            st.metric("Nota de Saúde SEO", f"{score}/100")

            if score < 60:

                st.error("Precisa de Atenção Crítica")

            elif score < 90:

                st.warning("Pode Melhorar")

            else:

                st.success("Excelente!")

        

        with c2:

            st.subheader("Diagnóstico:")

            if issues:

                for issue in issues:

                    st.write(issue)

            else:

                st.write("✅ Nenhum erro grave encontrado na contagem de caracteres.")
