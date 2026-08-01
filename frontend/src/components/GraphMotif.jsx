const EDGES = ['M40 170 L130 70', 'M130 70 L214 132', 'M214 132 L300 56', 'M214 132 L268 188', 'M40 170 L214 132']

const STARS = [
  { cx: 40, cy: 170, r: 2.4, primary: false },
  { cx: 130, cy: 70, r: 2.4, primary: false },
  { cx: 214, cy: 132, r: 3.4, primary: true },
  { cx: 300, cy: 56, r: 2.4, primary: false },
  { cx: 268, cy: 188, r: 3.4, primary: true },
]

export default function GraphMotif({ className }) {
  return (
    <svg className={className} viewBox="0 0 340 220" fill="none" aria-hidden="true">
      <g className="constellation-lines" stroke="var(--gold)" strokeWidth="1">
        {EDGES.map((d, i) => (
          <path key={d} d={d} style={{ '--edge-index': i }} />
        ))}
      </g>
      <g className="constellation-stars">
        {STARS.map((star, i) => (
          <circle
            key={`${star.cx}-${star.cy}`}
            cx={star.cx}
            cy={star.cy}
            r={star.r}
            fill={star.primary ? 'var(--gold)' : 'currentColor'}
            style={{ '--star-index': i }}
          />
        ))}
      </g>
    </svg>
  )
}
