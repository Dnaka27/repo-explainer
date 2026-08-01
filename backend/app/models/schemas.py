from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    repo_url: str


class Meta(BaseModel):
    repo_name: str
    primary_language: str | None = None
    partial_analysis: bool = False


class AnalysisResult(BaseModel):
    """Schema usado como response_schema na chamada ao Gemini."""

    summary_overview: str = Field(
        description=(
            "Visão geral em Markdown, em português, linguagem acessível: propósito do "
            "projeto, stack principal, como rodar. Use **negrito** para destacar nomes de "
            "tecnologias/stack e uma lista com marcadores para enumerar dependências ou "
            "passos de execução, quando fizer sentido — não escreva só parágrafos corridos."
        )
    )
    summary_detailed: str = Field(
        description=(
            "Visão detalhada em Markdown, em português: fluxo de execução real, "
            "como os módulos se conectam, pontos de entrada, principais funções/classes "
            "e suas responsabilidades. Use subtítulos (##/###), **negrito** para termos-chave "
            "(nomes de módulos, funções, arquivos), listas com marcadores para enumerar "
            "responsabilidades/módulos/dependências, e `código inline` para nomes de "
            "arquivos, funções e comandos. Evite parágrafos longos sem estrutura."
        )
    )
    flowchart: str = Field(
        description=(
            "Diagrama Mermaid válido, começando exatamente com 'flowchart TD', "
            "representando o fluxo de execução/lógica principal do código "
            "(não a estrutura de pastas). Não incluir blocos de código markdown, "
            "apenas a sintaxe Mermaid pura."
        )
    )
    diagram: str = Field(
        description=(
            "Diagrama Mermaid válido, começando exatamente com 'graph LR', "
            "representando a arquitetura/estrutura de módulos, componentes e suas "
            "dependências. Pode usar 'subgraph' para agrupar camadas. Não incluir "
            "blocos de código markdown, apenas a sintaxe Mermaid pura."
        )
    )


class AnalyzeResponse(BaseModel):
    summary_overview: str
    summary_detailed: str
    flowchart: str
    diagram: str
    meta: Meta
