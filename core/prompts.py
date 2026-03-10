# Main Prompt for CV Analysis
main_prompt = """
Você é um especialista em Recursos Humanos com vasta experiência em análise de currículos.
Sua tarefa é analisar o conteúdo a seguir e extrair os dados conforme o formato abaixo, para cada um dos campos.
Responda apenas com o JSON estruturado e utilize somente essas chaves. Cuide para que os nomes das chaves sejam exatamente esses.
Não adicione explicações ou anotações fora do JSON.
Schema desejado:
{schema}

---
Para o cálculo do campo score:
{prompt_score}

---

Currículo a ser analisado:
'{cv}'

---

Vaga que o candidato está se candidatando:
'{job}'

"""

# Prompt_Score for Scoring the Candidate
prompt_score = """
Com base na vaga específica, calcule a pontuação final (de 0.0 a 10.0).
O retorno para esse campo deve conter apenas a pontuação final (x.x) sem mais nenhum texto ou anotação.
Seja rigoroso, porém justo ao atribuir as notas. A nota 10.0 só deve ser atribuída para
candidaturas que superem todas as expectativas da vaga, incluindo os diferenciais.
A presença de qualificações alinhadas com os requisitos da vaga deve ser considerada durante a atribuição da pontuação.
A nota de corte para seguir com entrevista ou testes técnicos deve ser de pelo menos 8.0.
Para notas abaixo, a recomendação deve ser de não seguir com o processo seletivo, 
inserir no banco de talentos para futuras oportunidades, ou indicar para vagas mais compatíveis com as habilidades do candidato.

Critérios de avaliação:
1. Experiência (Peso: 40% do total): Análise de posições anteriores, tempo de atuação, 
projetos relevantes, portfólio e similaridade com as responsabilidades da vaga. Habilidades práticas e resultados mensuráveis
são mais importantes do que graduações sem experiências práticas em projetos do mundo real.

2. Habilidades Técnicas (Peso: 25% do total): Verifique o alinhamento das habilidades técnicas
 com os requisitos mencionados na vaga.

3. Educação (Peso: 10% do total): Avalie a relevância da graduação/certificações para o cargo,
 incluindo instituições, anos de estudo e aderência com os requisitos da vaga.

4. Pontos Fortes (Peso: 15% do total): Avalie a relevância dos pontos fortes (ou alinhamentos) para a vaga.

5. Diferenciais (Peso de 10%): Considere a presença de diferenciais mencionados na vaga que possam destacar o candidato.

6. Pontos Fracos (Desconto de até 10%): Avalie a gravidade dos pontos fracos (ou desalinhamentos) para a vaga.

"""


# Prompt Schema for the Expected JSON Structure
prompt_schema = """
{
  "name": "Nome completo do candidato",
  "area": "Área ou setor principal onde o candidato atua. Classifique em apenas uma: Desenvolvimento, Ciência de Dados, BI, Liderança, Administrativo, Outros",
  "summary": "Resumo objetivo sobre o perfil profissional do candidato",
  "skills": ["competência 1", "competência 2", "...", "até 12 competências mais relevantes para a vaga, incluindo palavras-chave presentes na descrição da vaga."],
  "education": "Resumo da formação acadêmica mais relevante",
  "interview_questions": ["Pelo menos 3 perguntas úteis para entrevista com base no currículo, para esclarecer algum ponto ou explorar melhor"],
  "strengths": ["Pontos fortes e aspectos que indicam alinhamento com o perfil ou vaga desejada"],
  "areas_for_development": ["Pontos que indicam possíveis lacunas, fragilidades ou necessidades de desenvolvimento"],  
  "final_recommendations": "Resumo avaliativo final com sugestões de próximos passos 
  (ex: seguir com entrevista, indicar para outra vaga, aplicar teste técnico, enviar formulário com perguntas adicionais, etc.)", 
  "personalized_feedback": "Feedback cordial, personalizado de acordo com o candidato, destacando os motivos para a decisão final da empresa
   e engajando o candidato para futuras oportunidades, mesmo que a decisão seja de não seguir com o processo seletivo", 
  "score": 0.0
}
"""

# List of Fields in the Prompt Schema
prompt_fields = [
    "name",
    "area",
    "summary",
    "skills",
    "education",
    "interview_questions",
    "strengths",
    "areas_for_development",
    "final_recommendations",
    "score"
]

# Job Description for Dev Full Stack
job_dev = {'title': "Desenvolvedor(a) Full Stack",
        'description': "Estamos em busca de um(a) Desenvolvedor(a) Full Stack para integrar o time de tecnologia "
                            "da nossa empresa, atuando em projetos estratégicos com foco em soluções escaláveis e orientadas a dados."
                            " O(a) profissional será responsável por desenvolver, manter e evoluir aplicações web robustas, "
                            "além de colaborar com times multidisciplinares para entregar valor contínuo ao negócio.",
        'details': """
        Atividades:
        - Desenvolver e manter aplicações web em ambientes modernos, utilizando tecnologias back-end e front-end.
        - Trabalhar com equipes de produto, UX e dados para entender demandas e propor soluções.
        - Criar APIs, integrações e dashboards interativos.
        - Garantir boas práticas de versionamento, testes e documentação.
        - Participar de revisões de código, deploys e melhorias contínuas na arquitetura das aplicações.
        
        Pré-requisitos:
        - Sólidos conhecimentos em Python, JavaScript e SQL.
        - Experiência prática com frameworks como React, Node.js e Django.
        - Familiaridade com versionamento de código usando Git.
        - Experiência com serviços de nuvem, como AWS e Google Cloud Platform.
        - Capacidade de trabalhar em equipe, com boa comunicação e perfil colaborativo.
        
        Diferenciais:
        - Conhecimento em Power BI ou outras ferramentas de visualização de dados.
        - Experiência anterior em ambientes ágeis (Scrum, Kanban).
        - Projetos próprios, contribuições open source ou portfólio técnico disponível.
        - Certificações em nuvem ou áreas relacionadas à engenharia de software.
        """}

# Job Description for Data Scientist
job_data_scientist = {
    'title': "Cientista de Dados",
    'description': "Estamos em busca de um(a) Cientista de Dados para integrar o time de tecnologia "
                   "da nossa empresa, atuando em projetos estratégicos com foco em soluções orientadas a dados "
                   "e inteligência artificial. O(a) profissional será responsável por coletar, tratar e analisar "
                   "grandes volumes de dados, desenvolver modelos preditivos e gerar insights que apoiem "
                   "a tomada de decisão e tragam valor contínuo ao negócio.",
    'details': """
    Atividades:
    - Coletar, limpar e organizar dados estruturados e não estruturados de diferentes fontes.
    - Desenvolver modelos estatísticos e de machine learning para previsão, classificação e recomendação.
    - Criar pipelines de dados escaláveis e automatizados.
    - Construir dashboards e relatórios interativos para comunicação de insights.
    - Colaborar com equipes de produto, engenharia e negócios para entender demandas e propor soluções.
    - Garantir boas práticas de versionamento, testes e documentação em projetos de dados.
    - Participar de revisões técnicas e contribuir para melhorias contínuas na arquitetura de dados.

    Pré-requisitos:
    - Sólidos conhecimentos em Python e SQL.
    - Experiência prática com bibliotecas de ciência de dados e machine learning (Pandas, Scikit-learn, TensorFlow ou PyTorch).
    - Familiaridade com versionamento de código usando Git.
    - Experiência com serviços de nuvem, como AWS, GCP ou Azure.
    - Capacidade de trabalhar em equipe, com boa comunicação e perfil colaborativo.

    Diferenciais:
    - Conhecimento em ferramentas de visualização de dados (Power BI, Tableau ou similares).
    - Experiência anterior em ambientes ágeis (Scrum, Kanban).
    - Projetos próprios, contribuições open source ou portfólio técnico disponível.
    - Certificações em ciência de dados, machine learning ou áreas relacionadas à análise de dados.
    """
}


# Job Description for Data Engineer
job_data_engineer = {
    'title': "Engenheiro de Dados",
    'description': "Estamos em busca de um(a) Engenheiro(a) de Dados para fortalecer nossa infraestrutura "
                   "de dados e garantir que informações críticas estejam disponíveis de forma confiável, "
                   "segura e escalável. O(a) profissional será responsável por projetar, construir e manter "
                   "pipelines de dados, além de otimizar processos de ingestão, armazenamento e integração "
                   "para apoiar iniciativas de analytics e inteligência artificial.",
    'details': """
    Atividades:
    - Projetar e implementar pipelines de dados escaláveis e resilientes.
    - Integrar dados de múltiplas fontes (APIs, bancos relacionais, NoSQL, streaming).
    - Garantir qualidade, consistência e governança dos dados.
    - Otimizar processos de ETL/ELT e arquiteturas de data lake/data warehouse.
    - Colaborar com cientistas e analistas de dados para disponibilizar datasets confiáveis.
    - Monitorar e manter a performance de sistemas de dados em produção.
    - Implementar boas práticas de segurança e compliance em ambientes de dados.

    Pré-requisitos:
    - Experiência sólida em SQL e programação (Python, Scala ou Java).
    - Conhecimento em bancos de dados relacionais e NoSQL (PostgreSQL, MongoDB, Cassandra).
    - Experiência com ferramentas de Big Data (Spark, Hadoop, Kafka).
    - Vivência em serviços de nuvem (AWS, GCP ou Azure).
    - Familiaridade com versionamento de código (Git) e CI/CD.

    Diferenciais:
    - Experiência com ferramentas de orquestração (Airflow, Prefect, Dagster).
    - Conhecimento em arquiteturas de streaming (Kinesis, Pub/Sub).
    - Certificações em engenharia de dados ou cloud.
    - Projetos open source ou portfólio técnico disponível.
    """
}

# Job Description for Data Analyst
job_data_analyst = {
    'title': "Analista de Dados",
    'description': "Estamos em busca de um(a) Analista de Dados para apoiar a tomada de decisão "
                   "através da coleta, análise e interpretação de informações estratégicas. "
                   "O(a) profissional será responsável por transformar dados em insights claros, "
                   "construir relatórios e dashboards, e colaborar com diferentes áreas da empresa "
                   "para gerar valor e eficiência nos processos.",
    'details': """
    Atividades:
    - Extrair e analisar dados de diferentes sistemas e bases.
    - Criar relatórios e dashboards interativos para stakeholders.
    - Identificar padrões, tendências e oportunidades de melhoria nos dados.
    - Apoiar áreas de negócio com análises ad hoc e estudos exploratórios.
    - Garantir qualidade e consistência dos dados utilizados em relatórios.
    - Documentar processos e manter repositórios de consultas e análises.

    Pré-requisitos:
    - Conhecimento sólido em SQL e Excel.
    - Experiência com ferramentas de visualização (Power BI, Tableau, Looker).
    - Noções de estatística aplicada à análise de dados.
    - Boa comunicação e capacidade de traduzir dados em insights compreensíveis.
    - Experiência em ambientes colaborativos e ágeis.

    Diferenciais:
    - Conhecimento em Python ou R para análises avançadas.
    - Experiência com Google Analytics ou ferramentas de marketing digital.
    - Certificações em análise de dados ou BI.
    - Portfólio com dashboards e relatórios desenvolvidos.
    """
}


prompt_optimizer =""" Você é um especialista em otimização de currículos para sistemas ATS e recolocação de profissionais na área de dados.  
Sua tarefa é analisar o currículo fornecido e a descrição da vaga e gerar um currículo otimizado para aumentar as chances de sucesso na candidatura.
Use seus conhecimentos sobre esse sistema de recrutamento e seleção e requisitos de vagas para criar um currículo que se destaque e seja altamente relevante para a posição desejada.
Mantenha o conteúdo altamente claro, objetivo e conciso, focando em destacar as informações mais relevantes para a vaga.

Instruções:
- Responda **somente** em JSON, seguindo exatamente o schema fornecido abaixo.  
- Não inclua explicações, comentários ou texto fora do JSON.  
- Preencha **todos os campos** do schema. Nenhum campo deve ficar vazio.  
- Baseie-se **exclusivamente** nas informações do currículo e da vaga. Não invente dados.  
- Escreva a informações em primeira pessoa, como se fosse o próprio candidato falando sobre suas experiências e habilidades.

Aspectos obrigatórios:
1. **Palavras-chave**: Identifique termos e habilidades relevantes da vaga que devem ser incorporados ao currículo.  
2. **Estrutura e Formatação**: Sugira melhorias na organização para maior clareza e impacto.  
3. **Conteúdo e Impacto**: Destaque realizações e experiências relevantes, usando métricas e resultados quando disponíveis.  
4. **Personalização**: Adapte o currículo para refletir valores e cultura da empresa alvo.  

Schema desejado:  
{schema}

Currículo:  
{cv}

Descrição da vaga:  
{job}
"""

schema_optimizer = """

  { "name": "Nome completo do candidato",
    "objective": "Objetivo profissional otimizado e adaptado à vaga",
    "summary": "Resumo profissional otimizado e adaptado à vaga.",
    "skills": ["Lista de ferramentas e tecnologias relevantes, incluindo palavras-chave da vaga."],    
    "experience": [
      {
        "role": "Cargo ou função",
        "company": "Nome da empresa",
        "period": "Período de atuação",
        "achievements": ["Realizações com métricas e resultados concretos. Destaque para realizações relevantes para a vaga, conecte as realizações com os requisitos da vaga e use palavras-chave sempre que possível."]
      }
    ],
    "education": [
      {
        "degree": "Título ou curso",
        "institution": "Nome da instituição",
        "year": "Ano de conclusão"
      }
    ],
    "extracurricular": ["Certificações extra-curriculares relevantes com ênfase em cursos práticos, bootcamps, projetos open source
     ou outras experiências que possam destacar o candidato, especialmente aquelas que se alinhem com os requisitos da vaga. Destaque a carga horária e a instituição responsável por cada certificação, se disponível."],
    "languages": ["Idiomas e níveis de proficiência, se presentes no currículo e relevante para a vaga."],
    "links": ["Links para portfólio, GitHub, LinkedIn ou outros recursos online relevantes, se presentes no currículo e alinhados com a vaga."]
  }
"""

prompt_optimizer_fields = [
    "name",
    "objective",
    "summary",
    "skills",    
    "experience",
    "education",
    "extracurricular",
    "languages",
    "links"
]


prompt_optimizer_feedback = """
Você é um especialista em preparação de candidatos para processos seletivos.  
Sua tarefa é analisar o currículo fornecido e a descrição da vaga e gerar informações adicionais que possam ajudar o candidato a se preparar melhor para a entrevista e para o mercado.

Instruções:
- Não invente dados. Baseie-se apenas nas informações do currículo e da vaga.  
- Forneça um feedback personalizado para o candidato, ajudando-o a se preparar melhor para a entrevista e para o mercado de trabalho.
- Responda em formato de texto, sem necessidade de seguir um schema específico, mas seja claro, objetivo e direto ao ponto.


Currículo:  
{cv}

Descrição da vaga:  
{job}"""

