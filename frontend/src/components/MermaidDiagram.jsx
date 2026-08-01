import { useEffect, useId, useState } from 'react'
import mermaid from 'mermaid'

let initialized = false

function initializeMermaid() {
  if (initialized) return
  const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
  mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    themeVariables: {
      fontFamily: "'Work Sans', system-ui, sans-serif",
      fontSize: '15px',
      primaryColor: isDark ? '#171b3d' : '#f7f8fc',
      primaryTextColor: isDark ? '#f3eee0' : '#1c1f3d',
      primaryBorderColor: isDark ? '#d9a441' : '#9c6f1b',
      lineColor: isDark ? '#8d93b8' : '#5b6089',
      secondaryColor: isDark ? '#0e1128' : '#edeff7',
      tertiaryColor: isDark ? '#0e1128' : '#edeff7',
      noteBkgColor: isDark ? '#3a2a10' : '#faf1dc',
      noteBorderColor: isDark ? '#d9a441' : '#9c6f1b',
      edgeLabelBackground: isDark ? '#0e1128' : '#edeff7',
    },
    flowchart: {
      curve: 'basis',
      nodeSpacing: 45,
      rankSpacing: 65,
      padding: 12,
    },
  })
  initialized = true
}

export default function MermaidDiagram({ chart, caption }) {
  const renderId = useId().replace(/:/g, '-')
  const [svg, setSvg] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    initializeMermaid()

    async function render() {
      if (!chart || !chart.trim()) {
        setError('Nenhum diagrama foi gerado.')
        return
      }
      try {
        const { svg: renderedSvg } = await mermaid.render(`mermaid-${renderId}`, chart.trim())
        if (!cancelled) {
          setSvg(renderedSvg)
          setError(null)
        }
      } catch {
        if (!cancelled) {
          setError('Não foi possível renderizar este diagrama.')
          setSvg(null)
        }
      }
    }

    render()
    return () => {
      cancelled = true
    }
  }, [chart, renderId])

  return (
    <div className="mermaid-diagram">
      {caption && <p className="mermaid-caption">{caption}</p>}
      <div className="mermaid-sheet">
        {error && (
          <div className="mermaid-error">
            <p>{error}</p>
            <pre>{chart}</pre>
          </div>
        )}
        {!error && svg && (
          // eslint-disable-next-line react/no-danger
          <div className="mermaid-render" dangerouslySetInnerHTML={{ __html: svg }} />
        )}
      </div>
    </div>
  )
}
