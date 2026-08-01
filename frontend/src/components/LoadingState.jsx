import GraphMotif from './GraphMotif.jsx'

export default function LoadingState() {
  return (
    <div className="loading-state" role="status" aria-live="polite">
      <GraphMotif className="loading-motif" />
      <p>Conectando os pontos do repositório — de 10 a 30 segundos.</p>
    </div>
  )
}
