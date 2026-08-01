import { useEffect, useRef, useState } from 'react'
import SummaryPanel from './SummaryPanel.jsx'
import MermaidDiagram from './MermaidDiagram.jsx'

const TABS = [
  { id: 'overview', index: '01', label: 'Visão geral' },
  { id: 'detailed', index: '02', label: 'Visão detalhada' },
  { id: 'flowchart', index: '03', label: 'Fluxograma' },
  { id: 'diagram', index: '04', label: 'Arquitetura' },
]

export default function ResultTabs({ result }) {
  const [activeTab, setActiveTab] = useState(TABS[0].id)
  const [indicator, setIndicator] = useState(null)
  const tabRefs = useRef({})

  useEffect(() => {
    function updateIndicator() {
      const el = tabRefs.current[activeTab]
      if (!el) return
      setIndicator({ left: el.offsetLeft, width: el.offsetWidth })
    }

    updateIndicator()
    window.addEventListener('resize', updateIndicator)
    return () => window.removeEventListener('resize', updateIndicator)
  }, [activeTab])

  return (
    <div className="result-tabs">
      <div className="tab-list" role="tablist">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            ref={(el) => {
              tabRefs.current[tab.id] = el
            }}
            type="button"
            role="tab"
            aria-selected={activeTab === tab.id}
            className={activeTab === tab.id ? 'tab active' : 'tab'}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-index">{tab.index}</span>
            {tab.label}
          </button>
        ))}
        {indicator && (
          <span
            className="tab-indicator"
            style={{ transform: `translateX(${indicator.left}px)`, width: indicator.width }}
          />
        )}
      </div>

      <div className="tab-panel" key={activeTab}>
        {activeTab === 'overview' && <SummaryPanel content={result.summary_overview} />}
        {activeTab === 'detailed' && <SummaryPanel content={result.summary_detailed} />}
        {activeTab === 'flowchart' && (
          <MermaidDiagram chart={result.flowchart} caption="Fig. 01 — Fluxo de execução" />
        )}
        {activeTab === 'diagram' && (
          <MermaidDiagram chart={result.diagram} caption="Fig. 02 — Arquitetura de módulos" />
        )}
      </div>
    </div>
  )
}
