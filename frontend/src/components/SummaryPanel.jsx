import ReactMarkdown from 'react-markdown'

export default function SummaryPanel({ content }) {
  return (
    <div className="summary-panel">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  )
}
