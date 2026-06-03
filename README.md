# 📚 Desempenho Escolar no Brasil

> Projeto G2 — Análise e Visualização de Dados com Python  
> Disciplina: Linguagem de Programação — Análise e Visualização de Dados com Python  
> Tema 24 — Desempenho Escolar no Brasil

---

## 📌 Sobre o Projeto

Este projeto realiza uma análise exploratória completa do desempenho escolar no Brasil entre os anos de **2015 e 2024**, investigando indicadores educacionais como médias de notas, taxas de aprovação e reprovação, desigualdades regionais, diferenças entre redes de ensino (pública e privada) e fatores associados ao rendimento dos estudantes, como renda familiar e acesso à internet.

---

## 🎯 Perguntas Orientadoras

- Quais estados apresentam melhor desempenho escolar?
- Existem diferenças entre escolas públicas e privadas?
- Houve melhoria no desempenho ao longo do tempo?
- Existe relação entre renda e desempenho?
- Como o acesso à internet impacta o aprendizado?
- Quais disciplinas apresentam menor rendimento?
- Existem desigualdades regionais relevantes?

---

## 🗂️ Estrutura do Projeto

```
projeto-desempenho-escolar/
│
├── app.py                  # Dashboard Streamlit (multipágina)
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação do projeto
├── index.html              # Página do projeto (GitHub Pages)
│
├── dados/
│   └── simulacao_desempenho_escolar_brasil.csv
│
├── notebooks/
│   └── analise_desempenho_escolar.ipynb
│
├── database/               # Reservado para persistência SQLite
└── imagens/                # Gráficos exportados
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia      | Finalidade                       |
| --------------- | -------------------------------- |
| Python 3.11+    | Linguagem principal              |
| Pandas          | Manipulação e análise de dados   |
| NumPy           | Cálculos numéricos e correlações |
| Matplotlib      | Visualizações estáticas          |
| Seaborn         | Visualizações estatísticas       |
| Plotly          | Gráficos interativos             |
| Streamlit       | Dashboard interativo multipágina |
| GitHub          | Versionamento do código          |
| GitHub Pages    | Publicação da página do projeto  |
| Streamlit Cloud | Publicação do dashboard          |

---

## 📊 Dataset

**Arquivo:** `simulacao_desempenho_escolar_brasil.csv`

| Coluna | Descrição |
|---|---|
| ano | Ano letivo (2015–2024) |
| semestre | Semestre letivo (1 ou 2) |
| data | Data de referência |
| regiao | Região do Brasil |
| uf | Estado |
| municipio | Município |
| rede_ensino | Pública ou Privada |
| disciplina | Matemática, Português, História, Geografia, Ciências |
| media_notas | Média geral das notas |
| taxa_aprovacao | Percentual de aprovação |
| taxa_reprovacao | Percentual de reprovação |
| acesso_internet | Percentual de acesso digital |
| renda_media_familiar | Renda média familiar (R$) |
| indice_desempenho | Índice geral de desempenho |
| nivel_desempenho | Baixo, Médio, Alto ou Excelente |

---

## ⚡ Funcionalidades

### Intermediárias
- Filtros múltiplos no Streamlit (ano, semestre, região, estado, rede, disciplina, nível)
- KPIs dinâmicos atualizados conforme filtros
- Gráficos interativos com Plotly
- Análise temporal (evolução 2015–2024)
- Visualizações comparativas (regiões, estados, disciplinas)

### Avançadas
- Dashboard multipágina no Streamlit
- Correlação estatística (renda x desempenho, internet x notas) com Pandas/NumPy

---

## 🚀 Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/projeto-desempenho-escolar.git
cd projeto-desempenho-escolar

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
streamlit run app.py
```

---

## 🔗 Links do Projeto

- 📁 **Repositório GitHub:** [github.com/wikten1/projeto-desempenho-escolar](https://github.com/SEU_USUARIO/projeto-desempenho-escolar)
- 🌐 **GitHub Pages:** [SEU_USUARIO.github.io/projeto-desempenho-escolar](https://SEU_USUARIO.github.io/projeto-desempenho-escolar)
- 📊 **Dashboard Streamlit:** [SEU_USUARIO-desempenho-escolar.streamlit.app](https://SEU_USUARIO-desempenho-escolar.streamlit.app)

---

## 👤 Autor: Wikten Alves de Medeiros

Desenvolvido como parte da Avaliação G2 da disciplina de Linguagem de Programação — Análise e Visualização de Dados com Python.

---

## 📄 Licença

Este projeto é de uso acadêmico.
