import { Terminal, Trash2 } from 'lucide-react'
import { useLogStore } from '../../store/logStore'

const FILTERS = ['ALL', 'WEBHOOK', 'ERROR', 'SUCCESS']

export default function LogFilterBar() {
  const { activeFilter, setFilter, clearLogs, logs } = useLogStore()

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '8px 14px', borderBottom: '1px solid var(--color-border)', flexShrink: 0 }}>
      <Terminal size={13} color="var(--color-ink-3)" />
      <span style={{ fontSize: 11, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-ink-3)', marginRight: 4 }}>Logic Trace</span>
      <div style={{ display: 'flex', gap: 4 }}>
        {FILTERS.map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            style={{
              padding: '3px 9px', borderRadius: 5, fontSize: 10.5, fontWeight: 500, border: '1px solid var(--color-border)',
              background: activeFilter === f ? 'var(--color-accent-soft)' : 'transparent',
              color: activeFilter === f ? 'var(--color-accent-ink)' : 'var(--color-ink-3)',
              cursor: 'pointer',
            }}
          >
            {f}
            {f === 'ERROR' && logs.filter(l => l.statusCode >= 400).length > 0 && (
              <span style={{ marginLeft: 4, background: 'var(--color-rose)', color: 'white', fontSize: 9, padding: '0 4px', borderRadius: 4 }}>
                {logs.filter(l => l.statusCode >= 400).length}
              </span>
            )}
          </button>
        ))}
      </div>
      <button
        onClick={clearLogs}
        style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 5, padding: '3px 9px', borderRadius: 5, fontSize: 10.5, color: 'var(--color-ink-3)', border: '1px solid var(--color-border)', cursor: 'pointer' }}
      >
        <Trash2 size={11} />
        Clear
      </button>
    </div>
  )
}
