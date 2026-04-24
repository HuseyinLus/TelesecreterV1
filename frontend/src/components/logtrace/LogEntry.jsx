import JsonViewer from './JsonViewer'

const METHOD_COLORS = {
  GET:    { bg: 'oklch(56% 0.09 210 / 0.15)', color: 'var(--color-accent-ink)' },
  POST:   { bg: 'oklch(62% 0.07 160 / 0.15)', color: 'var(--color-sage-ink)' },
  PATCH:  { bg: 'oklch(72% 0.11 70 / 0.15)',  color: 'var(--color-amber)' },
  DELETE: { bg: 'oklch(66% 0.11 20 / 0.15)',  color: 'var(--color-rose)' },
}

const statusColor = (code) => {
  if (!code || code === 0) return 'var(--color-ink-4)'
  if (code < 300) return 'var(--color-sage-ink)'
  if (code < 400) return 'var(--color-amber)'
  return 'var(--color-rose)'
}

export default function LogEntry({ entry }) {
  const m = METHOD_COLORS[entry.method] ?? { bg: 'var(--color-bg-subtle)', color: 'var(--color-ink-3)' }
  const ts = new Date(entry.timestamp)
  const timeStr = `${ts.getHours().toString().padStart(2,'0')}:${ts.getMinutes().toString().padStart(2,'0')}:${ts.getSeconds().toString().padStart(2,'0')}.${ts.getMilliseconds().toString().padStart(3,'0')}`
  const isError = entry.statusCode >= 400

  return (
    <div style={{
      padding: '5px 14px',
      borderLeft: isError ? '3px solid var(--color-rose)' : '3px solid transparent',
      borderBottom: '1px solid var(--color-border)',
      fontFamily: 'var(--font-mono)',
      fontSize: 11,
    }}>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, flexWrap: 'wrap' }}>
        <span style={{ color: 'var(--color-ink-4)', flexShrink: 0 }}>{timeStr}</span>
        <span style={{ padding: '1px 5px', borderRadius: 4, fontSize: 9.5, fontWeight: 700, background: m.bg, color: m.color, flexShrink: 0 }}>{entry.method}</span>
        <span style={{ color: 'var(--color-ink-2)', flex: 1, minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{entry.path}</span>
        <span style={{ color: statusColor(entry.statusCode), fontWeight: 600, flexShrink: 0 }}>{entry.statusCode}</span>
        <span style={{ color: 'var(--color-ink-4)', flexShrink: 0 }}>{entry.durationMs}ms</span>
      </div>
      <JsonViewer label="request"  data={entry.requestBody} />
      <JsonViewer label="response" data={entry.responseBody} />
    </div>
  )
}
