from  pathlib import Path
import uuid
import base64
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_classic.prompts import ChatPromptTemplate

from core.utils import *
from core.prompts import *

st.set_page_config(page_title="Analisador de Currículos", layout="wide")


with open("style.css") as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

# Configuração da Barra Lateral
with st.sidebar:
    st.image("https://th.bing.com/th/id/OIG4._TgHf2qbRc4wE6k1IOnK?pid=ImgGn", width=200 ) # Imagem de Logo    
    
    st.markdown("")
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = str(uuid.uuid4())
    
    if "selected_cv" not in st.session_state:
        st.session_state["selected_cv"] = None
            
        
    with st.expander("📤 Carregar Currículos (PDF)", expanded=True):        
        uploaded_files = st.file_uploader("Você pode carregar vários arquivos (PDF)",
                                      accept_multiple_files=True, type=[".pdf"], key=st.session_state["uploader_key"])
    
    with st.expander("📱 Contato", expanded=False):
        st.markdown(markdown, unsafe_allow_html=True)

    with st.expander("❓ Dúvidas sobre o Projeto", expanded=True):
        st.markdown(assistant_markdown, unsafe_allow_html=True)        
        #st.markdown("<h2 style='border: 1px solid #1f77b4; padding: 20px; text-align: center; color: #1f77b4;'>Dúvidas sobre o Projeto?</h2>", unsafe_allow_html=True)
                

if uploaded_files:
    st.markdown("<h1 style='text-align: center'>🎯 Triagem Inteligente de Currículos", unsafe_allow_html=True)
    st.markdown("""<h4 style='text-align: center'>Nota: a IA pode cometer erros, use os resultados como um apoio para suas decisões,
     mas sempre revise os resultados manualmente antes de tomar decisões finais.</h4>""", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid #1f77b4'>", unsafe_allow_html=True)
    input_col, output_col = st.columns([0.3, 0.7], gap="large")
    with input_col:
        st.markdown("<h2 style='text-align: center'>⚙️ Configurações da Análise</h2>", unsafe_allow_html=True)
    
        manual_desc = st.toggle("Deseja inserir descrição personalizada da vaga?", value=False)
        if manual_desc:
            description = st.text_area("Insira a descrição de uma Vaga específica:", height=300, width=700,
                                       placeholder="Copie e cole a descrição da vaga aqui, ou insira manualmente...")
        else:
            description = None
        if description is None:
            role = st.selectbox("Cargo alvo da análise",
                            options=["Cientista de Dados", "Engenheiro de Dados",
                                    "Analista de Dados", "Desenvolvedor Full Stack"])
        process_cv = st.button("🚀 Iniciar análise aprofundada", width="stretch", type="primary")

    if process_cv:     # ------   Modelos alternativos   (llama-3.1-8b-instant,  openai/gpt-oss-120b, openai/gpt-oss-safeguard-20b)  -----------
        llm = load_llm(model="openai/gpt-oss-safeguard-20b", temperature=0.1)  # Carrega o LLM para análise
        with output_col:
            with st.status("📊 Analisando currículos... Aguarde um instante", expanded=True)  as status:
                dict_responses = {} # Dicionário para organização dos resultados
                
                for upload in uploaded_files:
                    status.update(label=f"📄 Lendo **{upload.name}**...".replace(".pdf", ""))
                    path = Path(upload.name)
                    with open(path, "wb") as file:
                        file.write(upload.read())

                    # Lê e extrai o conteúdo dos currículos
                    resume = parse_documents(path)

                    status.update(label=str(f"🧠 Analisando aderência de ***{upload.name}***...").replace(".pdf", ""))
                    
                    # Construção do prompt para análise dos currículos
                    prompt_template = ChatPromptTemplate.from_template(main_prompt)
                    chain = prompt_template | llm

                    # Se a descrição não for informada na aplicação, usa as descrições de prompts (conforme a vaga)
                    job_description = description if description is not None else(
                        job_data_scientist if role == "Cientista de Dados" else 
                        job_data_engineer if role == "Engenheiro de Dados" else
                        job_data_analyst if role == "Analista de Dados" else
                        job_dev if role == "Desenvolvedor Full Stack" else ""
                    )
                    response = chain.invoke(
                        {"schema": prompt_schema, "prompt_score": prompt_score,
                        "cv": resume, "job": job_description}
                                )
                    

                    # Valicação e extração dos compos da resposta.
                    res = get_response_text(response, prompt_fields) # Valida json e verifica se todos os campos estão presentes na resposta
                    dict_responses[path.name] = res  # Adiciona a resposta ao dicionário

                                
                status.update(label=f"✅ Análise de {path} concluída com sucesso!".replace(".pdf", ""), state="complete")
                

            # ------- Visualização dos reultados (DASHBOARD) ----------
            df_results = process_results_to_df(dict_responses)
            tab_dashboard, tab_table, tab_pdf, tab_json = st.tabs(["🏆 Dashboard de Candidatos",
                        "📊 Tabela Comparativa", "📄 Relatório em PDF", "⚙️ Dados Brutos"])
            
                
                
            with tab_dashboard:
                # Criação de um card visual para cada candidato
                st.markdown("<h2 style='text-align: center'>Análise de Aderência dos Candidatos</h2>", unsafe_allow_html=True)
                for idx, row in df_results.iterrows():
                    score = float(row.get("score", 0))
                    color_score = "normal" if score > 8.0 else "off" if score >= 5.0 else "orange"

                    with st.container(border=True):
                        col1, col2 = st.columns([0.8, 0.2])
                        with col1:
                            st.subheader(f"{row.get('name', 'Candidato')}")
                            st.write(f"**Resumo:** {row.get('summary', 'Nenhum resumo disponível')}")
                            st.write(f"**Principais Habilidades:** {', '.join(row.get('skills', [])) if isinstance(row.get('skills'), list) else row.get('skills', 'Nenhuma habilidade listada')}")
                        with col2:
                            st.metric(label="Score de Aderência", value=f"{score}/10", delta=8.0, delta_color=color_score )


                        with st.expander("Mostrar mais detalhes do candidato"):
                            st.write(f"**Pontos Fortes:** {','.join(row.get('strengths', [])) if isinstance(row.get('strengths'), list) else row.get('strengths', 'Nenhum ponto forte listado')}")
                            st.write(f"**A Desenvolver:** {','.join(row.get('areas_for_development', [])) if isinstance(row.get('areas_for_development'), list) else row.get('areas_for_development', 'Nenhuma área para desenvolvimento listada')}")
                            st.write(f"**Recomendações finais:** {row.get('final_recommendations', 'Sem recomendações')}")
                            st.write(f"**Feedback personalizado para o candidato:** {row.get('personalized_feedback', 'Sem feedback personalizado')}" )
                                                                               
                

                with tab_table:
                    st.markdown("<h2 style='text-align: center'>Tabela Compatativa</h2>", unsafe_allow_html=True)                    
                    df_results_display = df_results.drop(columns=["summary", "education", "strengths", "Arquivo",
                     "areas_for_development", "final_recommendations", "interview_questions", "personalized_feedback"], errors="ignore").sort_values(by="score", ascending=False)
                    st.write(df_results_display)
                    
                    
                    
                    
                with tab_pdf:
                    st.markdown("<h2 style='text-align: center'>Relatório Completo em PDF</h2>", unsafe_allow_html=True)
                    pdf_bytes = save_to_pdf(df_results, mode="RH")
                    with open("curriculo.pdf", "rb") as f:
                        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

                    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}"zoom="40%" width="100%" height="600" type="application/pdf"></iframe>'
                    st.markdown(pdf_display, unsafe_allow_html=True)
                    
                    # Botão de Download do PDF
                    input_col.download_button(
                            label="📥 Baixar Relatório (PDF)",
                            data=pdf_bytes,
                            file_name="relatorio_RH.pdf",
                            mime="application/pdf",
                            key=f"dl_{idx}", width="stretch", type="primary"
                            )
                        
                with tab_json:
                    st.markdown("<h2 style='text-align: center'>Dados Estruturados (JSON)</h2>", unsafe_allow_html=True)
                    with st.expander("Visualizar JSON completo da resposta", expanded=False):
                        st.json(dict_responses)                        
                
             
else:
    st.markdown("<h1 style='color:#e0e0e0; text-align: center'>📄 Nenhum currículo carregado", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #d9d9d9; text-align: center'>Por favor, carregue o currículo na barra lateral para iniciar a análise", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #4db6dd'>", unsafe_allow_html=True)



