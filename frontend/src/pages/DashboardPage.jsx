import PulsePanel from '../components/pulse/PulsePanel'

export default function DashboardPage() {
  return (
    <div style={{
      display: 'grid',
      gridTemplateRows: '1fr 256px',
      gridTemplateColumns: '1fr 360px',
      height: '100%',
      overflow: 'hidden',
      gap: 0,
    }}>
      {/* Zone 2 — Registry (left, flex-grow) */}
      <div style={{
        gridRow: 1,
        gridColumn: 1,
        overflow: 'auto',
        padding: 24,
        borderRight: '1px solid var(--color-border)',
        borderBottom: '1px solid var(--color-border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--color-ink-3)',
        fontSize: 13,
      }}>
        Zone 2 — Registry
      </div>

      {/* Zone 1 — Pulse (right rail, 360px) */}
      <div style={{ gridRow: 1, gridColumn: 2, overflow: 'hidden' }}>
        <PulsePanel />
      </div>

      {/* Zone 3 — Logic Trace (full width bottom, 256px) */}
      <div style={{
        gridRow: 2,
        gridColumn: '1 / -1',
        overflow: 'hidden',
        borderTop: '1px solid var(--color-border)',
        background: 'var(--color-surface-2)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--color-ink-3)',
        fontSize: 13,
      }}>
        Zone 3 — Logic Trace
      </div>
    </div>
  )
}
