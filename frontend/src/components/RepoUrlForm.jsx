import { useId, useState } from 'react'

const GITHUB_REPO_URL_PATTERN = /^https?:\/\/github\.com\/[\w.-]+\/[\w.-]+\/?$/

export default function RepoUrlForm({ onSubmit, disabled }) {
  const inputId = useId()
  const [url, setUrl] = useState('')
  const [validationError, setValidationError] = useState(null)

  function handleSubmit(event) {
    event.preventDefault()
    const trimmed = url.trim()
    if (!GITHUB_REPO_URL_PATTERN.test(trimmed)) {
      setValidationError(
        'Isso não parece um link de repositório GitHub. Use o formato https://github.com/owner/repo.',
      )
      return
    }
    setValidationError(null)
    onSubmit(trimmed)
  }

  return (
    <form className="repo-form" onSubmit={handleSubmit}>
      <label className="repo-form-label" htmlFor={inputId}>
        URL do repositório
      </label>
      <div className="repo-form-row">
        <div className="repo-input-wrap">
          <input
            id={inputId}
            type="text"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://github.com/owner/repo"
            disabled={disabled}
            autoComplete="off"
            spellCheck="false"
          />
        </div>
        <button type="submit" disabled={disabled}>
          {disabled ? 'Analisando…' : 'Analisar'}
        </button>
      </div>
      {validationError && (
        <p className="form-error" role="alert">
          {validationError}
        </p>
      )}
    </form>
  )
}
