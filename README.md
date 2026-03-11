# 🚀 Projeto Currículo Inteligente

*Análise, Triagem e Otimização com LLMs*

Hoje, tanto empresas quanto candidatos enfrentam desafios recorrentes no mercado de trabalho, sobretudo na área de dados.
Nesse contexto os LLMs surgem como aliados poderosos na otimização desse processo, atendendo a ambos os lados do processo seletivo:

- **RH:** milhares de candidaturas para uma única vaga sobrecarregam equipes, gerando atrasos, erros e dificuldade em identificar talentos.
- **Candidatos:** profissionais qualificados são desclassificados por não conseguirem estruturar seus currículos de forma adequada às exigências específicas da vaga


## ⚙️ Funcionalidades da Ferramenta

*Este projeto utiliza Large Language Models (LLMs) para transformar o processo seletivo em três etapas principais:*

### 📃 Analisador de Currículos
- 	Upload de múltiplos PDFs.
- 	Extração de habilidades, formação, experiências e perguntas de entrevista.
- 	Geração de feedback personalizado e score de compatibilidade com a vaga.

### 🔎 Triagem Inteligente de Portfólio
-   Varredura dos projetos mais recentes do candidato através da API do GitHub.
- 	Análise automática de portfólios públicos (quando disponíveis).
- 	Cruzamento de informações entre currículo e projetos reais.
- 	Produção de scores mais confiáveis e identificação de talentos com maior potencial.


### 🎯 Otimizador de Currículos
- 	Identificação de lacunas nos currículos e sugestões de melhoria.
- 	Geração automática de um currículo otimizado em PDF, adaptado ao ATS.
- 	Feedback detalhado com dicas de cursos, pontos de destaque e possíveis perguntas de entrevista.


## 👥 Impacto

*Para o RH*
- 	Redução de horas de trabalho manual.
- 	Minimização de erros e atrasos.
- 	Seleção mais rápida e precisa de candidatos altamente qualificados com base em conteúdo real demonstrado em porfólio.

*Para o Candidato*
- 	Currículo adaptado às exigências da vaga.
- 	Destaque das habilidades relevantes em segundos.
- 	Feedback personalizado que aumenta as chances de sucesso.


## 📂 Estrutura do Projeto

```
SmartCV/
│
├── 01_📃_Analisador_de_Curriculos.py                 # Página principal (Streamlit)
├── pages/                                            # Outras páginas
│   ├── 02_🔎_Triagem_Inteligente_Portfolio.py       # Página de triagem baseada no portfólio 
│   └── 03_🎯_Otimizador_de_Curriculos.py            # Página de Otimização de currículos
│
├── core/                                            # Módulo com funções e prompts reutilizáveis
│   ├── __init__.py
│   ├── prompts.py                             
│   └── utils.py
│
|
|── Dockerfile                                      # Arquivo para conteinerização com docker
└── pyproject.toml                                  # Arquivo de instalação das dependências
```

## 🎯 Resultado Esperado

*Uma solução personalizada que atende* **RH e candidatos**
- 	**Para empresas:** suporte inteligente na triagem e seleção, reduzindo drasticamente tempo e esforço gastos e aumentando significativamente as chances de sucesso nas contratações.
- 	**Para candidatos:** currículos otimizados, feedback claro e maior chance de destaque sem inventar ou distorcer informações, destacando de forma justa, clara e concisa as habilidades reais do candidato.


## ✨ Principais diferenciais:

- 	📃 Analisador de Currículos: extrai habilidades, experiências mais relevantes e gera feedback com score de compatibilidade.
- 	🔎 Triagem Inteligente de Portfólio: cruza informações do currículo com projetos reais, potencializando a confiabilidade das análises.
- 	🎯 Otimizador de Currículos: identifica lacunas e gera automaticamente um currículo otimizado em PDF, adaptado-se a vagas específicas e ao sitema ATS.


> **🚀 Missão:** transformar currículos em narrativas poderosas e justas, conectando oportunidades a quem realmente tem potencial.


## 🤖 Suporte N8N

### Precisa de ajuda para entender o projeto?
*O assistente do projeto responde a todas as suas dúvidas:*
**👉 http://107.22.129.114:5678/webhook/4091fa09-fb9a-4039-9411-7104d213f601/chat**

### 💻Live Demo da Interface
![Interface_Streamlit](amostra_interface.gif)





