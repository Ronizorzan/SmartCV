from  pathlib import Path
import uuid
import base64
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_classic.prompts import ChatPromptTemplate

from core.prompts import *
from core.utils import *

st.set_page_config(page_title="Otimizador de Currículos", layout="wide")

with open("style.css") as file:
    st.html(f"<style>{file.read()}</style>", unsafe_allow_javascript=True)

# Configuração da Barra Lateral
with st.sidebar:
    st.image("https://th.bing.com/th/id/OIG1.quX1n6HvUE5Yvs3RYKCv?w=270&h=270&c=6&r=0&o=5&pid=ImgGn", width=175)
    
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = str(uuid.uuid4())
    
    if "selected_cv" not in st.session_state:
        st.session_state["selected_cv"] = None

    with st.expander("📤 Carregar Currículo (PDF)", expanded=True):
        uploaded_file = st.file_uploader("📤 Escolha arquivos de currículo (PDF)", help="Você pode carregar apenas um documento",
                                      accept_multiple_files=False, type=[".pdf"], key=st.session_state["uploader_key"])
    
    with st.expander("📱 Contato", expanded=False):
        st.markdown(markdown, unsafe_allow_html=True)
        #st.markdown("<h1 style='border: 1px solid #1f77b4; padding: 20px; text-align: center; color: #1f77b4;'>Contato</h1>", unsafe_allow_html=True)

    with st.expander("❓ Dúvidas sobre o Projeto", expanded=True):
        st.markdown(assistant_markdown, unsafe_allow_html=True)        


if uploaded_file:    
    st.markdown("<h1 style='text-align: center'>🔼 Otimizador de Currículos</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center'>Nota: a IA pode cometer erros, use os resultados como apoio, mas sempre revise os currículos manualmente antes de submetê-los.</h4>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #1f77b4'>", unsafe_allow_html=True)
    input_col, output_col = st.columns([0.3, 0.7], gap="large")
    with input_col:
        st.markdown("<h2 style='text-align: center'>⚙️ Configurações da Análise</h2>", unsafe_allow_html=True)
        manual_desc = st.toggle("Deseja inserir descrição personalizada da vaga?", value=False)
        if manual_desc:
            description = st.text_area("Insira a descrição de uma vaga específica (opcional):", height=250, width=700,
                                       placeholder="Copie e cole a descrição da vaga aqui, ou insira manualmente...")                                    
        else:        
            description = None
    
        if description is None:
            role = st.selectbox("Cargo alvo da análise:",
                            options=["Cientista de Dados", "Engenheiro de Dados",
                                     "Analista de Dados", "Desenvolvedor Full Stack"])
        else:
            role = None                                    

        process_cv = st.button("Analisar Currículos", use_container_width=True, type="primary")
    
    if process_cv:
        with output_col:            #      llama-3.3-70b-versatile, openai/gpt-oss-120B, openai/gpt-oss-safeguard-20b
            llm = load_llm(model="openai/gpt-oss-safeguard-20b", temperature=0.6) # Carrega o modelo LLM

            with st.status("⌛ Otimizando currículo... Aguarde um instante", expanded=True)  as status:
                path = Path(uploaded_file.name)
                with open(path, "wb") as file:
                    file.write(uploaded_file.read())

                status.update(label=f"📄 Lendo **{uploaded_file.name}**...".replace(".pdf", ""))
                resume = parse_documents(path) # Lê e extrai o conteúdo dos currículos

                # Construção do prompt para otimização de currículos
                prompt_template = ChatPromptTemplate.from_template(prompt_optimizer)
                chain = prompt_template | llm

                status.update(label=f"🚀 Otimizando currículo **{uploaded_file.name}** para a vaga de **{role if role else 'Não especificada'}**...".replace(".pdf", ""), state="running")
                job_description = description if description is not None else (
                    job_data_scientist if role == "Cientista de Dados" else 
                        job_data_engineer if role == "Engenheiro de Dados" else
                        job_data_analyst if role == "Analista de Dados" else
                        job_dev if role == "Desenvolvedor Full Stack" else ""
                )
                response = chain.invoke(
                    {"schema": schema_optimizer, "cv": resume, "job": job_description}
                            )

                # Construção do prompt para feedback de otimização de currículos
                status.update(label=f"📑 Gerando feedback personalizado para: **{uploaded_file.name}**...".replace(".pdf", ""), state="running")
                prompt_template_feedback = ChatPromptTemplate.from_template(prompt_optimizer_feedback)
                chain_feedback = prompt_template_feedback | llm
                feedback_response = chain_feedback.invoke(
                    {"cv": resume, "job": job_description}
                )
                status.update(label=f"✅ Currículo **{path}** otimizado com sucesso!".replace(".pdf", ""), state="complete")                

            
            response_json = get_response_text(response, prompt_optimizer_fields)                                    
            tab_resume, tab_analysis, tab_json = st.tabs(["📄 Currículo Otimizado", "💡 Feedback Personalizado", "📄 Dados em JSON"])

            with tab_resume:
                st.markdown("<h2 style='text-align: center'>📄 Currículo Otimizado</h2>", unsafe_allow_html=True)
                #st.markdown("<hr style='border: 1px solid #1f77b4'>", unsafe_allow_html=True)
                #st.markdown(response.content, unsafe_allow_html=True)
                
                pdf_bytes_optimizer = save_to_pdf(response_json, "CV", path.stem + "_otimizado.pdf")
                with open(path.stem + "_otimizado.pdf", "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}"zoom="40%" width="100%" height="600" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            
            input_col.download_button(
                label="📥 Baixar Currículo Otimizado",
                data=pdf_bytes_optimizer,
                file_name=path.stem + "_otimizado.pdf",
                mime="application/pdf",
                width="stretch", type="primary")


            
            with tab_analysis:
                st.markdown("<h2 style='text-align: center'>💡 Feedback personalizado</h2>", unsafe_allow_html=True)
                #st.markdown("<hr style='border: 1px solid #1f77b4'>", unsafe_allow_html=True)
                st.markdown(feedback_response.content, unsafe_allow_html=True)

            with tab_json:
                st.markdown("<h2 style='text-align: center'>⚙️ Dados em JSON</h2>", unsafe_allow_html=True)
                #st.markdown("<hr style='border: 1px solid #1f77b4'>", unsafe_allow_html=True)                

                with st.expander("Exibir JSON completo da resposta do modelo", expanded=False):                    
                    st.json(response_json)  # Exibe os dados brutos em formato JSON                    
                

else:
    st.markdown("<h1 style='color:#e0e0e0; text-align: center'>📄 Nenhum currículo carregado", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #d9d9d9; text-align: center'>Por favor, carregue o currículo na barra lateral e pressione o botão para iniciar a análise", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #4db6dd'>", unsafe_allow_html=True)

