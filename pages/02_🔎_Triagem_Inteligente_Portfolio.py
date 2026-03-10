import streamlit as st
import uuid
import requests
import json
import os
import tempfile
from pathlib import Path
from langchain_classic.prompts import ChatPromptTemplate

# Importação das funções do módulo core.utils
from core.utils import (
    parse_documents, analyze_with_github,
    create_prompt_template, extract_and_optimize_cv,
    load_llm, fetch_github_repos,
    build_candidate_context, markdown, assistant_markdown
)


st.set_page_config(page_title="Triagem Inteligente (GitHub)", layout="wide")



with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --- Interface Principal ---

# Sidebar
with st.sidebar:
    st.image("https://www.bing.com/th/id/OIG4.oZJd.QjEejBJIA0uFnFd?w=540&h=540&c=6&r=0&o=5&pid=ImgGn", width=200)    
    
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = str(uuid.uuid4())
    
    with st.expander("📤 Carregar Currículo (PDF)", expanded=True):
        uploaded_file = st.file_uploader("📤 Escolha um currículo (em PDF)", 
                            type=[".pdf"], key=st.session_state["uploader_key"], help="Você pode carregar apenas um documento")

    with st.expander("📱 Contato", expanded=False):
        st.markdown(markdown, unsafe_allow_html=True)

    with st.expander("❓ Dúvidas sobre o Projeto", expanded=True):
        st.markdown(assistant_markdown, unsafe_allow_html=True)


if uploaded_file:
    
    # Layout da página
    st.markdown("<h1 style='text-align: center'>💡 Triagem Inteligente Avançada (CV + GitHub)</h1>", unsafe_allow_html=True)
    st.markdown("""<h4 style='text-align:center'>Nota: Ao enviar o currículo, qualquer repositório público do GitHub presente 
                    no mesmo será consultado para uma análise técnica profunda.</h4>""", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #1f77b4'>", unsafe_allow_html=True)

    input_col, output_col = st.columns([0.25, 0.75], gap="large")
    # Salvando o arquivo PDF em um diretório temporário para a função parse_documents ler
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    role = input_col.selectbox("Cargo alvo da análise:", ["Cientista de Dados", "Engenheiro de Dados", "Engenheiro de Machine Learning", "Desenvolvedor Full Stack"])
    
    if input_col.button("🚀 Iniciar Análise Profunda", type="primary", width="stretch"):
        
        with output_col:
            tabs = st.tabs(["📌 Resumo gerado", "💻 Repositórios analisados (GitHub)", "📊 Análise Final"], default="📊 Análise Final", width="stretch")    
            with st.spinner("Buscando repositórios e gerando parecer final"):                
                
                # Etapa 1: Processamento do CV e busca no GitHub            
                cv_docs = parse_documents(tmp_file_path)            
                extracted_data = extract_and_optimize_cv(cv_docs)
                                
                if extracted_data:                
                    with tabs[0]:
                        st.markdown("<h2 style='text-align: center'>Resumo do Currículo</h2>", unsafe_allow_html=True)                               
                        
                        st.markdown(extracted_data.get("CV"))
                        st.metric("Usuário do GitHub Identificado:", extracted_data.get("user") or "Não encontrado")
                                                
                    # Etapa 2: Extrair conteúdo do GitHub
                    with tabs[1]:                        
                        github_user = extracted_data.get("user")                   
                        github_docs = [] # Acumular o conteúdo extraído do GitHub para análise posterior
                                    
                        if github_user:
                            github_docs = fetch_github_repos(github_user)                    
                            if github_docs:
                                st.markdown(f"<h2 style='text-align: center'>Foram analisados {len(github_docs)} repositórios.</h2>", unsafe_allow_html=True)
                                for doc in github_docs:
                                    with st.expander(f"Repositório: {doc.metadata['source']}"):
                                        st.markdown(doc.page_content)
                            else:
                                st.warning("Nenhum repositório público encontrado ou erro na API.")
                        
                        else:
                            st.info("O candidato não informou o GitHub no currículo.")
                                                
                    # Etapa 3: Análise Final Combinada
                    with tabs[2]:                                                
                        final_analysis = analyze_with_github(extracted_data, github_docs, role)
                        st.markdown(final_analysis.replace("<br>", "\n"))


            # Limpa o arquivo temporário
            os.remove(tmp_file_path)
                    

else:    
    st.markdown("<h1 style='color:#e0e0e0; text-align: center'>📄 Nenhum currículo carregado", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #d9d9d9; text-align: center'>Por favor, carregue o currículo na barra lateral para iniciar a análise", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #4db6dd'>", unsafe_allow_html=True)                    
    