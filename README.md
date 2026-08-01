# Graph View — Cartografia de repositórios GitHub via IA

Cole a URL de um repositório GitHub público e receba, gerados por IA (Gemini): um fluxograma do fluxo de execução, um diagrama de arquitetura e um resumo em duas camadas.

---

## Technologies

![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Python](https://img.shields.io/badge/Python-1F2194?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini%20API-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Mermaid](https://img.shields.io/badge/Mermaid.js-FF3670?style=for-the-badge&logo=mermaid&logoColor=white)

---

## Sample

Deploy ao vivo: **[repo-explainer-weld.vercel.app](https://repo-explainer-weld.vercel.app)**

---

## About

O usuário cola a URL de um repositório público do GitHub e recebe três outputs gerados por IA: um fluxograma do fluxo de execução/lógica do código, um diagrama da arquitetura/estrutura do projeto e um resumo em duas camadas (visão geral + visão detalhada).

O backend busca apenas os metadados e a árvore de arquivos do repositório via GitHub REST API (sem autenticação obrigatória) e aplica uma heurística para selecionar os arquivos mais relevantes (README, arquivos de configuração na raiz, entrypoints, diretórios rasos). O **conteúdo** desses arquivos não é baixado pelo backend — é o próprio Gemini que lê diretamente as URLs `raw.githubusercontent.com` através da tool `url_context`, o que evita estourar o rate limit não-autenticado do GitHub (60 req/hora).

Uma única chamada estruturada ao Gemini (`response_schema`) retorna os quatro campos (resumo geral, resumo detalhado, fluxograma e diagrama, ambos em sintaxe Mermaid), que o frontend renderiza com `mermaid.js` e `react-markdown`.

---

## Project structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, exception handlers
│   ├── config.py            # Configurações via variáveis de ambiente
│   ├── routers/analyze.py   # Endpoint POST /analyze
│   └── services/
│       ├── github_client.py   # Metadados + árvore do GitHub
│       ├── file_selector.py   # Heurística de seleção de arquivos
│       ├── prompt_builder.py  # Monta o prompt para o Gemini
│       └── gemini_client.py   # Chamada estruturada ao Gemini (url_context)
└── tests/

frontend/
└── src/
    ├── App.jsx                        # Estado principal (idle/loading/success/error)
    ├── api/analyzeRepo.js             # Cliente HTTP do backend
    └── components/
        ├── RepoUrlForm.jsx            # Input + validação da URL
        ├── ResultTabs.jsx             # Abas: geral / detalhada / fluxograma / arquitetura
        ├── MermaidDiagram.jsx         # Renderização + zoom/pan dos diagramas
        └── SummaryPanel.jsx           # Renderização Markdown do resumo
```

---

## Installation

```bash
# backend
cd backend
python -m venv .venv
.venv/Scripts/activate      # Windows
pip install -r requirements.txt

# frontend
cd ../frontend
npm install
```

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua-chave-aqui
GEMINI_MODEL=gemini-flash-latest
GITHUB_TOKEN=            # opcional, aumenta o rate limit da API do GitHub
MAX_FILES_TO_ANALYZE=20
MAX_FILE_SIZE_BYTES=50000
MAX_TOTAL_PROMPT_BYTES=400000
GEMINI_TIMEOUT_SECONDS=60
```

Obtenha a chave do Gemini em [Google AI Studio](https://aistudio.google.com/).

> Se o projeto estiver dentro de uma pasta sincronizada pelo Google Drive/OneDrive, pause a sincronização antes de rodar `npm install` — a sincronização em tempo real pode travar arquivos durante a escrita de `node_modules` e causar erros (EBADF/EPERM).

### Rodando localmente

Opção rápida (Git Bash) — sobe os dois juntos, Ctrl+C encerra ambos:

```bash
./start.sh
```

Ou manualmente, em dois terminais:

```bash
# backend (porta 8000)
cd backend
.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000

# frontend (porta 5173)
cd frontend
npm run dev
```

> Use sempre `.venv/Scripts/python.exe -m uvicorn ...` (não só `uvicorn ...`). Se a venv não estiver ativada no shell, chamar `uvicorn` direto pode acabar usando uma instalação global do Python (sem as dependências do projeto) em vez da venv.

Abra `http://localhost:5173`, cole a URL de um repositório público (ex: `https://github.com/octocat/Hello-World`) e clique em Analisar.

### Testes

```bash
cd backend
.venv/Scripts/python -m pytest
```

### Deploy

- **Frontend (Vercel)**: deployado a partir da pasta `frontend/` (`vercel --prod`). A env var `VITE_API_BASE_URL` aponta para o backend.
- **Backend (Render)**: configurado via `render.yaml` na raiz (Blueprint). No dashboard do Render: **New +** → **Blueprint** → conecte o repositório → preencha os secrets `GEMINI_API_KEY` e `GITHUB_TOKEN`.

> Plano free do Render "dorme" após inatividade — a primeira requisição depois de um tempo pode demorar ~30-60s extra pra acordar o serviço.

---

## License

This project is licensed under the MIT License.

---

## Contact

[![LinkedIn](https://img.shields.io/badge/LinkedIn-78d?style=for-the-badge&logo=linkedin&logoColor=0A0AAF)](https://www.linkedin.com/in/diogo-oike-kanefuku-23639b223/)
[![E-mail](https://img.shields.io/badge/-Email-e9a?style=for-the-badge&logo=gmail&logoColor=E94D5F)](mailto:diogooikejapan@gmail.com)
