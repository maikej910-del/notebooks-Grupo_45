<div align="center">
  <img src="https://raw.githubusercontent.com/maikej910-del/notebooks-Grupo_45/main/logo.jpeg" alt="Logo Terra Fita" width="250">
</div>

# 🏥 Terra Fit: Sistema Preditivo de Diagnóstico Ponderal

## Tech Challenge FIAP (Fase 4) - Grupo 45 | Machine Learning aplicado à Saúde

🔗 **Acesse a aplicação em produção:** [Clique aqui para abrir o Sistema](https://notebooks-grupo45-xngddkmfv7koeyvmubsqco.streamlit.app/)

---

## 📌 Visão Geral Executiva

A **Terra Fit** nasce como uma marca e um conceito de inteligência voltados para a medicina preventiva e a análise de dados clínicos. O nome e sua identidade visual representam o equilíbrio entre o cuidado humano e a precisão tecnológica, unindo o acolhimento à exatidão analítica dos dados.

Este projeto foi desenvolvido como parte do Tech Challenge da FIAP (Fase 4) com foco na construção de um pipeline de Machine Learning de ponta a ponta para apoio à tomada de decisão clínica.

A solução consiste em um modelo preditivo treinado para classificar o risco e a classe de peso de um paciente com base em variáveis demográficas, comportamentais, histórico familiar e dados físicos. O algoritmo foi empacotado e disponibilizado em produção por meio de uma aplicação web interativa construída com a framework Streamlit.

O objetivo estratégico da solução é mitigar a subjetividade em avaliações limítrofes, acelerar a triagem de pacientes e fornecer uma ferramenta baseada em dados para suporte diagnóstico qualificado.

---

## 🎯 Objetivo de Negócio

Desenvolver um sistema inteligente e de alta performance capaz de:

- Auxiliar profissionais de saúde na identificação precoce do nível de sobrepeso/obesidade de forma padronizada.
- Automatizar o cálculo de indicadores cruciais (como o IMC) e variáveis compostas de estilo de vida no backend.
- Apoiar estratégias preventivas e tratamentos personalizados.
- Transformar dados brutos de rotina e saúde em informação clínica acionável em tempo real.

---

## 🧠 Arquitetura da Solução

A solução foi arquitetada utilizando práticas sólidas de Engenharia de Dados e Ciência de Dados, dividida em duas camadas principais:

### 1️⃣ Camada de Machine Learning (Modelagem)
- **Seleção de Features Estratégica:** Remoção intencional das variáveis brutas de "Peso" e "IMC" do conjunto de treino. Esta abordagem elimina o viés de multicolinearidade e força o algoritmo a avaliar o quadro clínico somente a partir das rotinas comportamentais do paciente ou seu historico familiar.
- **Pipeline de Transformação:** Utilização de `ColumnTransformer` associado ao `RobustScaler` (para tratar dados numéricos com maior tolerância a discrepâncias) e `OneHotEncoder` (binarização categórica), mitigando completamente o risco de *Data Leakage*.
- **Algoritmo Preditivo:** Implementação de um modelo ensemble `RandomForestClassifier` com pesos balanceados (`class_weight='balanced'`) e restrições de profundidade para evitar o sobreajuste (overfitting).
- **Alta Performance:** O modelo calibrado atingiu uma **acurácia global de 94.64%** nos dados de validação.
- **Artefato Gerado:** O pipeline completo foi serializado no arquivo:
  `modelo_obesidade_rf.pkl`

### 2️⃣ Camada de Aplicação Web (Interface)
- Desenvolvida integralmente em **Streamlit** focando em usabilidade clínica e produtividade.
- **Entrada Nominativa:** Inclusão de campo para identificação do paciente, permitindo centralizar a consulta.
- **Interface Segura (Campos Vazios):** Todos os seletores e campos numéricos iniciam completamente limpos (`None` / `""`). Isso elimina valores padrões na tela e obriga o profissional de saúde a preencher cada informação de forma consciente, evitando diagnósticos acidentais.
- **Mapeamento Reverso no Backend:** Implementação de um dicionário de conversão oculto no código. O usuário seleciona opções textuais intuitivas na tela (ex: "Sempre", "Raramente"), e o sistema traduz automaticamente para os códigos numéricos exatos que o modelo exige.
- **Cálculo de Índices em Tempo Real:** Processamento automático das entradas com injeção instantânea do cálculo do IMC e do cálculo cruzado de score de atividade física, somente informativo ao paciente. O intuito mesmo da aplicação é apresentar que as rotinas comportamentais do paciente ou seu historico familiar influciam e aumentam a probabilidade nas categorias de peso.
- **Exportação de Relatórios:** Geração automatizada de relatórios em formato Excel (`.xlsx`) contendo os dados coletados do paciente e o respectivo diagnóstico clínico, facilitando o arquivamento ou a impressão dos resultados.

---

## 📂 Estrutura do Repositório

    notebooks-grupo_45/
    │
    ├── Tech_Fase_4_Grupo_45.ipynb   # Notebook principal com EDA, ETL e Treinamento
    ├── app.py                       # Código-fonte da aplicação web (Streamlit)
    ├── modelo_obesidade_rf.pkl      # Modelo de ML treinado e serializado
    ├── requirements.txt             # Dependências e versões exatas para o deploy
    ├── Obesity.csv                  # Base de dados bruta utilizada na ingestão
    ├── log.jpeg                     # Logotipo oficial do projeto (Terra Fita)
    └── obesity_tratada_grupo45.csv  # Base consolidada exportada para consumo em Data Viz

---

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.10+
- **Manipulação de Dados:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn
- **Serialização:** Joblib
- **Desenvolvimento Web:** Streamlit
- **Geração de Relatórios:** XlsxWriter (Exportação para Excel)
- **Visualização de Dados:** Matplotlib, Seaborn
- **Controle de Versão:** Git & GitHub

---

## 🚀 Deploy e Produção

A aplicação encontra-se publicada na nuvem através do **Streamlit Community Cloud**, com um fluxo de deploy contínuo (CI/CD) conectado diretamente à branch `main` deste repositório.

**Link de Acesso:** [https://notebooks-grupo45-xngddkmfv7koeyvmubsqco.streamlit.app/](https://notebooks-grupo45-xngddkmfv7koeyvmubsqco.streamlit.app/)

**Diferenciais da Infraestrutura:**
- **Sincronização de Versões:** O arquivo `requirements.txt` trava as versões exatas de todas as bibliotecas (incluindo o motor gráfico e o gerador de planilhas), eliminando incompatibilidades do modelo em produção.
- **Inferências em Milissegundos:** O modelo de *Random Forest* permanece residente na memória do servidor, garantindo respostas imediatas assim que o formulário é validado.

---

## 📊 Impacto Estratégico

Esta solução comprova a viabilidade da aplicação prática de Ciência de Dados no cotidiano corporativo e hospitalar, garantindo:

- **Escalabilidade:** Uma ferramenta web leve que elimina a necessidade de softwares locais ou instalações pesadas.
- **Confiabilidade:** Padronização do diagnóstico através de um algoritmo robusto contra variabilidade clínica humana.
- **Eficiência:** Redução drástica do esforço manual em cálculos de triagem nutricional e geração de relatórios de avaliação.
