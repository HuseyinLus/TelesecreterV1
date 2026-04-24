import PulsePanel from '../components/pulse/PulsePanel'
import RegistryPanel from '../components/registry/RegistryPanel'
import LogTracePanel from '../components/logtrace/LogTracePanel'

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
      <div style={{ gridRow: 1, gridColumn: 1, overflow: 'hidden', borderRight: '1px solid var(--color-border)', borderBottom: '1px solid var(--color-border)' }}>
        <RegistryPanel />
      </div>

      {/* Zone 1 — Pulse (right rail, 360px) */}
      <div style={{ gridRow: 1, gridColumn: 2, overflow: 'hidden' }}>
        <PulsePanel />
      </div>

      {/* Zone 3 — Logic Trace (full width bottom, 256px) */}
      <div style={{ gridRow: 2, gridColumn: '1 / -1', overflow: 'hidden', borderTop: '1px solid var(--color-border)' }}>
        <LogTracePanel />
      </div>
    </div>
  )
}
