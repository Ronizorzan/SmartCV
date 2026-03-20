import json
import requests
import pandas as pd
from weasyprint import HTML
from langchain_groq import ChatGroq
from langchain_classic.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser
import streamlit as st
import os


# Loads the model from Groq API
@st.cache_resource
def load_llm(model, temperature=0.5, max_tokens=None, max_retries=3, timeout=None, verbose=False):
    """
    Carrega um modelo LLM da API Groq com cache para otimizar chamadas.

    Parameters
    ----------
    model : str
        Nome ou identificador do modelo a ser carregado.
    temperature : float, optional
        Grau de aleatoriedade nas respostas (default=0.5).
    max_tokens : int, optional
        Número máximo de tokens na resposta.
    max_retries : int, optional
        Número máximo de tentativas em caso de falha.
    timeout : int, optional
        Tempo limite para requisição.
    verbose : bool, optional
        Define se logs detalhados devem ser exibidos.

    Returns
    -------
    ChatGroq
        Instância do modelo carregado.
    """
    llm = ChatGroq(model=model, temperature=temperature, max_tokens=max_tokens,
                   max_retries=max_retries, timeout=timeout, verbose=verbose)
    return llm


# Loads the content from PDFs
def parse_documents(file_path):
    """
    Carrega documentos PDF usando PyMuPDFLoader.

    Parameters
    ----------
    file_path : str
        Caminho do arquivo PDF.

    Returns
    -------
    list of Document
        Lista de documentos extraídos do PDF.
    """
    loader = PyMuPDFLoader(str(file_path)) # Garante que seja string
    docs = loader.load()
    return docs


# Creates the prompt template
def create_prompt_template(template: str) -> ChatPromptTemplate:
    """
    Cria um template de prompt para interação com LLM.

    Parameters
    ----------
    template : str
        Texto base do prompt.

    Returns
    -------
    ChatPromptTemplate
        Template configurado para uso em modelos de linguagem.
    """
    prompt_template = ChatPromptTemplate.from_template(template)
    return prompt_template

# Extracts the reponse from a structured Json
def get_response_text(response, required_fields: list) -> dict:
    """
    Extrai e valida informações em formato JSON da resposta do modelo.

    Parameters
    ----------
    response : object
        Objeto de resposta do modelo contendo o atributo `content`.
    required_fields : list
        Lista de campos obrigatórios a serem garantidos no JSON.

    Returns
    -------
    dict
        Dicionário com os campos extraídos e validados.
    """
    try:
        res = response.content
        if "<think>" in res:
            res = res.split("</think>")[-1].strip() 

        start_index = res.find("{")
        final_index = res.rfind("}") + 1    
        if start_index == -1 or final_index == 0:
            raise json.JSONDecodeError("Nenhum JSON encontrado.", res, 0)
        
        json_text = res[start_index:final_index]
        info_cv = json.loads(json_text)
        
        for field in required_fields:
            if field not in info_cv:
                info_cv[field] = "Não aplicável"
        
        return info_cv
    except json.JSONDecodeError as e:
        print("Erro ao decodificar JSON:", e)
        return {field: "Erro na extração" for field in required_fields}

# Creates a CSV file with several results
def process_results_to_df(dict_responses: dict) -> pd.DataFrame:
    """
    Converte respostas extraídas em um DataFrame estruturado.

    Parameters
    ----------
    dict_responses : dict
        Dicionário com nome do arquivo como chave e dados extraídos como valor.

    Returns
    -------
    pandas.DataFrame
        DataFrame formatado com os resultados.
    """
    formatted_data = []
    for filename, data in dict_responses.items():
        row = {"Arquivo": filename}
        row.update(data)
        formatted_data.append(row)
    return pd.DataFrame(formatted_data)


# Generates a PDF document with weasyprint
def save_to_pdf(df, mode, file_path="curriculo.pdf"):
    """
    Gera um PDF formatado a partir de dados estruturados.

    Parameters
    ----------
    df : pandas.DataFrame or dict
        Dados a serem convertidos em PDF. Pode ser DataFrame (modo RH) ou dict (modo CV).
    mode : str
        Define o tipo de relatório: "RH" para triagem executiva ou "CV" para currículo.
    file_path : str, optional
        Caminho de saída do arquivo PDF (default="curriculo.pdf").

    Returns
    -------
    bytes
        Conteúdo binário do PDF gerado, útil para download em Streamlit.
    """
    if mode == "RH":
        # Placeholder - URL da logo personalizada da empresa 
        logo_url = "https://www.bing.com/th/id/OIG4.CkhC9D4TeOfL0IT2UmTg?w=540&h=540&c=6&r=0&o=5&pid=ImgGn"
        
        # Cabeçalho e estilo aprimorado
        html_header = f"""
        <html>
        <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; color: #333; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ max-height: 70px; margin-bottom: 10px; }}
            h1 {{ color: #1F77B4; border-bottom: 2px solid #1F77B4; padding-bottom: 10px; font-size: 24px; }}
            table {{ width: 100%; margin-top: 20px; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 12px; }}
            th {{ background-color: #f4f6f9; color: #1F77B4; font-weight: bold; text-transform: uppercase; }}
            tr:nth-child(even) {{ background-color: #fbfbfb; }}
            .section {{ margin-top: 30px; }}
            .section h2 {{ color: #1F77B4; margin-bottom: 10px; font-size: 18px; }}
            .page-break {{ page-break-before: always; }} /* Pula para a próxima página no PDF */
            .score-badge {{ background-color: #1F77B4; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }}
        </style>
        </head>
        <body>
        <div class="header">
            <img src="{logo_url}" alt="Logo" class="logo">
            <h1>Relatório Executivo de Triagem</h1>
        </div>
        <table>
            <tr>
                <th>Nome</th>
                <th>Área</th>                
                <th>Principais Skills</th>                                
                <th>Score</th>
            </tr>
        """

        # Linhas da tabela (Resumo Geral)
        rows = ""
        for _, candidato in df.iterrows():
            skills = candidato.get("skills", [])
            skills_str = ", ".join(skills) if isinstance(skills, list) else str(skills)
            
            rows += f"""
            <tr>
                <td><strong>{candidato.get("name","N/A")}</strong></td>
                <td>{candidato.get("area","N/A")}</td>                
                <td>{skills_str}</td>
                <td><span class="score-badge">{candidato.get("score","N/A")}</span></td>
            </tr>
            """

        html_table = f"{html_header}{rows}</table>"

        # Seções detalhadas (Com quebra de página)
        html_sections = ""
        for idx, candidato in df.iterrows():
            # A partir do segundo candidato, forçamos uma quebra de página
            page_break_class = "page-break" if idx > 0 else ""
            
            strengths = candidato.get("strengths", [])
            dev_areas = candidato.get("areas_for_development", [])
            questions = candidato.get("interview_questions", [])
            
            html_sections += f"""
            <div class="section {page_break_class}">
                <h2>Análise Detalhada: {candidato.get("name","N/A")}</h2>
                <p><strong>Resumo:</strong> {candidato.get("summary","N/A")}</p>
                <p><strong>Pontos Fortes:</strong> {", ".join(strengths) if isinstance(strengths, list) else strengths}</p>
                <p><strong>Áreas para Desenvolvimento:</strong> {", ".join(dev_areas) if isinstance(dev_areas, list) else dev_areas}</p>
                <p><strong>Formação:</strong> {candidato.get("education","N/A")}</p>
                
                <p><strong>Perguntas Sugeridas para Entrevista:</strong></p>
                <ul>
                    {''.join([f"<li>{q}</li>" for q in (questions if isinstance(questions, list) else [])])}
                </ul>
                
                <p><strong>Recomendação Final:</strong> {candidato.get("final_recommendations","N/A")}</p>
                <div style="background-color: #f4f6f9; padding: 15px; border-left: 4px solid #1F77B4; margin-top: 15px;">
                    <strong>Feedback para o Candidato:</strong><br>
                    {candidato.get('personalized_feedback', 'N/A')}
                </div>
            </div>
            """

        html_content = f"{html_table}{html_sections}</body></html>"

    elif mode == "CV":
        resume = df

        # Estilo de Currículo Limpo (Clean & Modern Standard)
        html_content = f"""
        <html>
        <head>
        <style>
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 40px; color: #222; line-height: 1.5; }}
            h1 {{ text-align: center; color: #2C3E50; font-size: 26px; margin-bottom: 5px; }}
            h2 {{ color: #2C3E50; font-size: 16px; text-transform: uppercase; border-bottom: 1px solid #bdc3c7; padding-bottom: 3px; margin-top: 25px; margin-bottom: 10px; letter-spacing: 1px; }}
            p {{ font-size: 14px; margin-bottom: 8px; margin-top: 0; }}
            ul {{ font-size: 14px; margin-top: 5px; margin-bottom: 15px; padding-left: 20px; }}
            li {{ margin-bottom: 4px; }}
            .job-header {{ font-weight: bold; font-size: 15px; margin-bottom: 2px; }}
            .job-period {{ font-style: italic; color: #7f8c8d; font-size: 13px; margin-bottom: 5px; }}
        </style>
        </head>
        <body>
            <h1>{resume.get('name','N/A')}</h1>

            <h2>Objetivo profissional</h2>
            <p>{resume.get('objective','N/A')}</p>

            <h2>Resumo Profissional</h2>
            <p>{resume.get('summary','N/A')}</p>

            <h2>Principais Habilidades</h2>
            <ul>{''.join([f"<li>{s}</li>" for s in resume.get('skills',[])])}</ul>

            <h2>Experiência Profissional</h2>
            {''.join([
                f"<div class='job-header'>{exp.get('role','')} - {exp.get('company','')}</div>"
                f"<div class='job-period'>{exp.get('period','')}</div>"
                f"<ul>{''.join([f'<li>{a}</li>' for a in exp.get('achievements',[])])}</ul>"
                for exp in resume.get('experience',[])
            ])}

            <h2>Educação</h2>
            <ul>{''.join([f"<li><strong>{edu.get('degree','')}</strong> - {edu.get('institution','')} ({edu.get('year','')})</li>" for edu in resume.get('education',[])])}</ul>

            <h2>Atividades Extracurriculares</h2>
            <ul>{''.join([f"<li>{e}</li>" for e in resume.get('extracurricular',[])])}</ul>

            <h2>Idiomas e Links</h2>
            <p><strong>Idiomas:</strong> {', '.join(resume.get('languages',[]))}</p>
            <p><strong>Links:</strong> {', '.join(resume.get('links',[]))}</p>
        </body>
        </html>
        """

    # Gerar PDF
    HTML(string=html_content).write_pdf(file_path)

    # Retornar bytes para o botão de Download do Streamlit
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    
    return pdf_bytes


# Fetch data from public repositories on GitHub
@st.cache_data(show_spinner=False)
def fetch_github_repos(username, max_repos=10, sort="updated", direction="desc"):
    """
    Busca repositórios públicos de um usuário no GitHub.

    Args:
        username (str): Nome de usuário do GitHub.
        max_repos (int, opcional): Número máximo de repositórios a retornar. 
            Padrão é 10.
        sort (str, opcional): Critério de ordenação dos repositórios 
            (ex.: "updated", "created"). Padrão é "updated".
        direction (str, opcional): Direção da ordenação ("asc" ou "desc"). 
            Padrão é "desc".

    Returns:
        list[Document]: Lista de objetos Document contendo informações 
        resumidas dos repositórios e conteúdo do README (limitado a 5000 caracteres).
    """
    url = f"https://api.github.com/users/{username}/repos?sort={sort}&direction={direction}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    repos = response.json()
    docs = []
    for repo in repos[:max_repos]:
        repo_info = f"""
        Nome: {repo['name']}
        Descrição: {repo.get('description', 'Sem descrição')}
        Linguagem principal: {repo.get('language', 'N/A')}        
        Última atualização: {repo['updated_at']}
        """
        
        readme_url = f"https://api.github.com/repos/{username}/{repo['name']}/readme"
        readme_resp = requests.get(readme_url, headers={"Accept": "application/vnd.github.v3.raw"})
        readme_content = readme_resp.text if readme_resp.status_code == 200 else "README não disponível."
        
        content = repo_info + "\n\nREADME:\n" + readme_content
        docs.append(Document(page_content=content[:4500], metadata={"source": repo['html_url']}))
    return docs

    
def build_candidate_context(cv_summary, github_docs):
    """
    Combina o resumo do currículo com os documentos extraídos do GitHub.

    Args:
        cv_summary (str): Texto contendo o resumo do currículo do candidato.
        github_docs (list[Document]): Lista de documentos com dados dos 
            repositórios do GitHub.

    Returns:
        str: Texto concatenado com o resumo do currículo e os dados do GitHub,
        separado por delimitadores.
    """    
    cv_doc = Document(page_content=f"RESUMO DO CURRÍCULO:\n{cv_summary}", metadata={"source": "CV"})
    all_docs = [cv_doc] + github_docs
    return "\n\n---\n\n".join([doc.page_content for doc in all_docs])


def extract_and_optimize_cv(cv_docs):
    """
    Extrai e otimiza informações de currículos utilizando um modelo de linguagem.

    Args:
        cv_docs (list[Document]): Lista de documentos contendo o conteúdo do currículo.

    Returns:
        dict | None: Dicionário estruturado com:
            - "CV": Resumo condensado das habilidades, experiências e formação.
            - "user": Username do GitHub ou null se não encontrado.
        Retorna None em caso de falha na extração.
    """
    llm_extractor = load_llm(model="openai/gpt-oss-20b", temperature=0.2) # Temperatura baixa para JSON mais previsível    
    
    response_schema = [
        ResponseSchema(name="CV", description="Resumo condensado das habilidades, experiências e formação acadêmica do candidato com todas as informações relevantes do currículo."),
        ResponseSchema(name="user", description="Apenas o username do GitHub (ex: 'torvalds'). Se não encontrar nenhuma URL do GitHub, retorne exatamente null.")
    ]

    output_parser = StructuredOutputParser.from_response_schemas(response_schema)

    format_instructions = output_parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_template(
        """Você é um assistente de extração de dados técnicos de currículos.
         Leia o currículo abaixo e extraia as informações com precisão e ALTO NÍVEL DE DETALHAMENTO para uma análise posterior mais aprofundada.
         Extraia TODAS AS INFORMAÇÕES do currículo para um cruzamento de informações
         baseado nos dados do currículo e portfólio do candidato.
        {format_instructions}

        Contexto (Currículo):
        {context}"""
    
    )

    chain = prompt | llm_extractor | output_parser

    try:
        context_text = "\n\n".join(doc.page_content for doc in cv_docs)

        parsed_response = chain.invoke({
            "context": context_text,
            "format_instructions": format_instructions
        })            

        return parsed_response
    
    except Exception as error:
        st.error(f"Falha ao extrair os dados do currículo: {error}")
        return None

    

def analyze_with_github(condensed_json, github_docs, role, level):
    """
    Analisa o perfil do candidato com base no currículo e nos repositórios do GitHub.

    Args:
        condensed_json (dict): Dados extraídos e otimizados do currículo.
        github_docs (list[Document]): Lista de documentos com informações dos 
            repositórios do GitHub.
        role (str): Cargo alvo da análise (ex.: "Desenvolvedor Backend").
        level (str): Nível da vaga (ex.: "Júnior", "Sênior").

    Returns:
        str: Texto em formato Markdown contendo:
            - Habilidades declaradas e demonstradas.
            - Avaliação da relevância dos projetos do GitHub.
            - Dois scores (currículo e GitHub).
            - Resumo executivo com pontos fortes e áreas de desenvolvimento.
    """
    llm_analyzer = load_llm(model="openai/gpt-oss-120b", temperature=0.3)
    
    candidate_context = build_candidate_context(condensed_json.get("CV", ""), github_docs)
    
    prompt = create_prompt_template("""
   Você é um avaliador de candidatos para a vaga de {role} nível {level} com foco em identificar talentos em potencial para a empresa.
   Considere os conhecimentos que você tem sobre os requisitos tipicamente exigidos para o cargo ao realizar a análise.
   Analise os dados extraídos do currículo e os repositórios do GitHub fornecidos e retorne a resposta para ser exibida em markdown.
   Quando aplicável, utilize emojis informativos que dirija o olhar do usuário para as informações mais importantes rapidamente.
   Quando renderizar tabelas mantenha-as informativas, relevantes e sem lacunas nos campos.
            
    - Identifique habilidades declaradas e habilidades demonstradas.
    - Avalie a relevância dos projetos do GitHub para a vaga.
    - **Gere dois scores:**
        1. Score baseado no currículo.
        2. Score baseado em evidências práticas do GitHub (README, tecnologias, relevância, resultados).    
    - Produza um resumo executivo com pontos fortes e áreas de desenvolvimento.

    Contexto do candidato:
    {candidate_context}
    """)
    
    response = llm_analyzer.invoke(
        prompt.format_messages(role=role, candidate_context=candidate_context, level=level)
    )
    return response.content


markdown = """<div class="footer">
    <p><strong>Desenvolvido por: Ronivan</strong></p>    
    <a href="https://github.com/Ronizorzan/LLMs-e-Agentes-de-IA" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/128/536/536452.png" alt="GitHub">
    </a>
    <a href="https://www.linkedin.com/in/ronivan-zorzan-barbosa" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/128/1377/1377213.png" alt="LinkedIn">
    </a>
    <a href="mailto:ronizorzan1992@gmail.com" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/128/5968/5968534.png" alt="Email">
    </a>

</div>
"""

assistant_markdown = """<div class="assistant-container">
    <p class="assistant-label">Assistente do Projeto</p>
    <a href="http://100.54.239.46:5678/webhook/4091fa09-fb9a-4039-9411-7104d213f601/chat">
        <div class="assistant-icon">
            <img src="https://cdn-icons-gif.flaticon.com/17576/17576937.gif" alt="Assistente n8n">
        </div>
    </a>
</div>
"""
