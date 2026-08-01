# Graph View

Cole a URL de um repositório público do GitHub e receba, gerados por IA (Gemini):

1. **Fluxograma** — fluxo de execução/lógica do código.
2. **Diagrama** — arquitetura/estrutura do projeto.
3. **Resumo** — visão geral e visão detalhada de como o repositório funciona.

Veja `plan.md` para a visão de produto completa.

## Stack

- Frontend: React + Vite.
- Backend: Python + FastAPI.
- IA: Google Gemini API (`google-genai`).
- Fonte de dados: GitHub REST API (metadados + árvore de arquivos, sem autenticação).
  O conteúdo dos arquivos selecionados é lido pelo próprio Gemini via tool
  `url_context` (URLs `raw.githubusercontent.com`), não pela API do GitHub —
  isso evita estourar o rate limit não-autenticado do GitHub (60 req/hora).
- Diagramas: Mermaid.js.

## Configuração

1. Crie um arquivo `.env` na raiz do projeto:

```
GEMINI_API_KEY=sua-chave-aqui
GEMINI_MODEL=gemini-flash-latest
GITHUB_TOKEN=            # opcional, aumenta o rate limit da API do GitHub
MAX_FILES_TO_ANALYZE=20
MAX_FILE_SIZE_BYTES=50000
MAX_TOTAL_PROMPT_BYTES=400000
GEMINI_TIMEOUT_SECONDS=60
```

2. Instale as dependências:

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

> Se o projeto estiver dentro de uma pasta sincronizada pelo Google Drive/OneDrive,
> pause a sincronização antes de rodar `npm install` — a sincronização em tempo real
> pode travar arquivos durante a escrita de `node_modules` e causar erros (EBADF/EPERM).

## Rodando localmente

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

> Use sempre `.venv/Scripts/python.exe -m uvicorn ...` (não só `uvicorn ...`). Se a venv
> não estiver ativada no shell, chamar `uvicorn` direto pode acabar usando uma instalação
> global do Python (sem as dependências do projeto) em vez da venv.

Abra `http://localhost:5173`, cole a URL de um repositório público (ex:
`https://github.com/octocat/Hello-World`) e clique em Analisar.

## Testes do backend

```bash
cd backend
.venv/Scripts/python -m pytest
```
