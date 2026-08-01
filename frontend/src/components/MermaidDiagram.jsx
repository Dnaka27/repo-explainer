import { useEffect, useId, useRef, useState } from 'react'
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
      // Keep the diagram at its natural size instead of shrinking it to fit
      // the column width — the sheet scrolls/zooms instead of squishing text.
      useMaxWidth: false,
    },
  })
  initialized = true
}

const MIN_ZOOM = 0.25
const MAX_ZOOM = 3
const ZOOM_STEP = 0.2

export default function MermaidDiagram({ chart, caption }) {
  const renderId = useId().replace(/:/g, '-')
  const [svg, setSvg] = useState(null)
  const [error, setError] = useState(null)
  const [zoom, setZoom] = useState(1)
  const [naturalSize, setNaturalSize] = useState(null)

  const sheetRef = useRef(null)
  const renderRef = useRef(null)

  useEffect(() => {
    let cancelled = false
    initializeMermaid()
    setNaturalSize(null)
    setZoom(1)

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

  // After the SVG lands in the DOM, read its natural size and auto-fit it to
  // the available width so it starts fully legible instead of squeezed.
  useEffect(() => {
    if (!svg || !renderRef.current) return
    const svgEl = renderRef.current.querySelector('svg')
    if (!svgEl) return

    const width = parseFloat(svgEl.getAttribute('width'))
    const height = parseFloat(svgEl.getAttribute('height'))
    if (!width || !height) return

    setNaturalSize({ width, height })

    const available = sheetRef.current ? sheetRef.current.clientWidth - 48 : width
    const fitZoom = available > 0 && width > available ? available / width : 1
    setZoom(Math.max(MIN_ZOOM, Math.min(1, fitZoom)))
  }, [svg])

  // Apply the current zoom directly to the SVG's pixel size so the sheet can
  // scroll to the full diagram rather than scaling everything down uniformly.
  useEffect(() => {
    if (!naturalSize || !renderRef.current) return
    const svgEl = renderRef.current.querySelector('svg')
    if (!svgEl) return
    svgEl.style.width = `${naturalSize.width * zoom}px`
    svgEl.style.height = `${naturalSize.height * zoom}px`
  }, [zoom, naturalSize])

  function handleZoomOut() {
    setZoom((z) => Math.max(MIN_ZOOM, +(z - ZOOM_STEP).toFixed(2)))
  }

  function handleZoomIn() {
    setZoom((z) => Math.min(MAX_ZOOM, +(z + ZOOM_STEP).toFixed(2)))
  }

  function handleFit() {
    if (!naturalSize || !sheetRef.current) return
    const available = sheetRef.current.clientWidth - 48
    const fitZoom = available > 0 && naturalSize.width > available ? available / naturalSize.width : 1
    setZoom(Math.max(MIN_ZOOM, Math.min(1, fitZoom)))
  }

  function handleReset() {
    setZoom(1)
  }

  return (
    <div className="mermaid-diagram">
      <div className="mermaid-header">
        {caption && <p className="mermaid-caption">{caption}</p>}
        {!error && svg && naturalSize && (
          <div className="mermaid-zoom-controls">
            <button type="button" onClick={handleZoomOut} disabled={zoom <= MIN_ZOOM} aria-label="Diminuir zoom">
              −
            </button>
            <button type="button" className="mermaid-zoom-value" onClick={handleReset} title="Redefinir para 100%">
              {Math.round(zoom * 100)}%
            </button>
            <button type="button" onClick={handleZoomIn} disabled={zoom >= MAX_ZOOM} aria-label="Aumentar zoom">
              +
            </button>
            <button type="button" onClick={handleFit} className="mermaid-fit-button">
              Ajustar
            </button>
          </div>
        )}
      </div>
      <div className="mermaid-sheet" ref={sheetRef}>
        {error && (
          <div className="mermaid-error">
            <p>{error}</p>
            <pre>{chart}</pre>
          </div>
        )}
        {!error && svg && (
          // eslint-disable-next-line react/no-danger
          <div className="mermaid-render" ref={renderRef} dangerouslySetInnerHTML={{ __html: svg }} />
        )}
      </div>
    </div>
  )
}
