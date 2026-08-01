// GEMINI_ERROR expõe o texto bruto da exceção do SDK (ex: "503 UNAVAILABLE {...}"),
// por isso é o único código com mensagem fixa em vez da mensagem vinda do backend.
const FRIENDLY_OVERRIDES = {
  GEMINI_ERROR: 'A IA está sobrecarregada no momento. Tente novamente em instantes.',
}

export default function ErrorState({ code, message, onRetry }) {
  const friendlyMessage = FRIENDLY_OVERRIDES[code] ?? message ?? 'Ocorreu um erro inesperado.'

  return (
    <div className="error-state" role="alert">
      <span className="error-flare" aria-hidden="true" />
      <p>{friendlyMessage}</p>
      {onRetry && (
        <button type="button" onClick={onRetry}>
          Tentar novamente
        </button>
      )}
    </div>
  )
}
