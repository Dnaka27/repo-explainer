import { useState } from 'react'
import RepoUrlForm from './components/RepoUrlForm.jsx'
import LoadingState from './components/LoadingState.jsx'
import ErrorState from './components/ErrorState.jsx'
import ResultTabs from './components/ResultTabs.jsx'
import GraphMotif from './components/GraphMotif.jsx'
import { analyzeRepo, ApiError } from './api/analyzeRepo.js'
import './App.css'

export default function App() {
  const [status, setStatus] = useState('idle') // idle | loading | success | error
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [lastUrl, setLastUrl] = useState(null)

  async function handleSubmit(repoUrl) {
    setStatus('loading')
    setError(null)
    setLastUrl(repoUrl)
    try {
      const data = await analyzeRepo(repoUrl)
      setResult(data)
      setStatus('success')
    } catch (err) {
      const code = err instanceof ApiError ? err.code : 'INTERNAL_ERROR'
      setError({ code, message: err.message })
      setStatus('error')
    }
  }

  function handleRetry() {
    if (lastUrl) handleSubmit(lastUrl)
  }

  return (
    <div className="app">
      <header className="hero">
        <GraphMotif className="hero-motif" />
        <div className="hero-content">
          <span className="eyebrow">Cartografia de repositórios</span>
          <h1>Graph View</h1>
          <p>
            Cole o link de um repositório público do GitHub. A IA lê o código e traça o mapa:
            fluxograma, arquitetura e um resumo em duas camadas.
          </p>
        </div>
      </header>

      <main className="app-main">
        <RepoUrlForm onSubmit={handleSubmit} disabled={status === 'loading'} />

        {status === 'loading' && <LoadingState />}
        {status === 'error' && error && (
          <ErrorState code={error.code} message={error.message} onRetry={handleRetry} />
        )}
        {status === 'success' && result && (
          <>
            {result.meta?.partial_analysis && (
              <p className="partial-warning">
                <strong>Amostra parcial —</strong> este repositório é grande demais para ler
                por completo; a análise usou uma seleção dos arquivos mais relevantes.
              </p>
            )}
            <ResultTabs result={result} />
          </>
        )}
      </main>
    </div>
  )
}
