from __future__ import annotations

from app.services.github_client import TreeEntry

MERMAID_RULES = """\
Para os campos flowchart e diagram, gere Mermaid sintaticamente válido. Regras obrigatórias:
- IDs de nó sem espaços, acentos ou caracteres especiais (use A, B, Step1, etc.).
- Texto legível dentro de colchetes: A[Texto do nó].
- Evite aspas duplas dentro de labels; se precisar, escape-as.
- Não use parênteses/colchetes aninhados sem abrir/fechar corretamente.
- Não use "end" como texto de label sem aspas (é palavra reservada do Mermaid em subgraphs).
- Evite os caracteres &, < e > soltos dentro de labels sem aspas.
- Não envolva a saída em blocos de código markdown (```mermaid); apenas a sintaxe Mermaid pura.

Para flowchart: comece exatamente com "flowchart TD". Use losangos para decisões
(B{Condição?} --> |Sim| C / |Não| D). Represente o fluxo de execução real
(ex.: entrypoint -> parsing de input -> lógica principal -> output), não a árvore de diretórios.

Para diagram: comece exatamente com "graph LR" (esquerda para direita — evita um layout
achatado/largo quando há muitos módulos no mesmo nível). Represente módulos/componentes/
camadas e as dependências entre eles (setas indicando "depende de"/"chama"). Agrupe com
"subgraph" quando fizer sentido (ex.: subgraph Frontend ... end), e prefira uma estrutura
em camadas (ex.: Frontend -> Backend -> Dados) em vez de muitos nós ligados diretamente a
um único nó raiz."""


def build_file_tree_text(entries: list[TreeEntry]) -> str:
    return "\n".join(sorted(entry.path for entry in entries if entry.type == "blob"))


def build_prompt(
    owner: str,
    repo: str,
    description: str | None,
    primary_language: str | None,
    tree_entries: list[TreeEntry],
    file_urls: list[str],
) -> str:
    tree_text = build_file_tree_text(tree_entries)
    urls_section = "\n".join(file_urls)

    return f"""Você é um engenheiro de software sênior analisando um repositório GitHub.

## Repositório
Nome: {owner}/{repo}
Descrição: {description or "Não informada"}
Linguagem principal: {primary_language or "Não informada"}

## Estrutura de arquivos (árvore, pode estar parcial em repos muito grandes)
{tree_text}

## Arquivos selecionados para leitura
Use a ferramenta de busca de URL para abrir e ler o conteúdo de cada uma destas URLs
antes de responder:
{urls_section}

## Instruções

1. Escreva summary_overview e summary_detailed em português, claros e objetivos, e em
   Markdown rico: use **negrito** para termos-chave, listas com marcadores para qualquer
   coisa enumerável (dependências, módulos, passos, responsabilidades) e `código inline`
   para nomes de arquivos/funções/comandos. Não escreva blocos de texto corrido sem
   nenhuma estrutura — quebre em parágrafos curtos, listas e subtítulos.
2. Baseie-se apenas no conteúdo obtido dessas URLs; se algo não estiver claro, diga isso
   explicitamente na visão detalhada em vez de inventar.
3. {MERMAID_RULES}
"""
