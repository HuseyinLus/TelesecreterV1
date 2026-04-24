import { ChevronLeft, ChevronRight } from 'lucide-react'

export default function CalendarToolbar({ view, onView, label, onPrev, onNext }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', alignItems: 'center', padding: '14px 0', gap: 12 }}>
      {/* Left: nav */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 2, background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 9, padding: 2 }}>
          <button onClick={onPrev} style={{ width: 28, height: 28, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', borderRadius: 7, border: 'none', background: 'none', cursor: 'pointer' }}><ChevronLeft size={14} /></button>
          <button onClick={onNext} style={{ width: 28, height: 28, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', borderRadius: 7, border: 'none', background: 'none', cursor: 'pointer' }}><ChevronRight size={14} /></button>
        </div>
        <span style={{ fontFamily: 'var(--font-serif)', fontSize: 20, color: 'var(--color-ink)', letterSpacing: '-0.005em', whiteSpace: 'nowrap' }}>{label}</span>
      </div>

      {/* Right: view switcher */}
      <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
        <div style={{ display: 'flex', background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 9, padding: 3 }}>
          {['week', 'day', 'list'].map((v) => (
            <button key={v} onClick={() => onView(v)} style={{ padding: '5px 12px', fontSize: 12, fontWeight: 500, borderRadius: 6, border: 'none', background: view === v ? 'var(--color-bg-subtle)' : 'transparent', color: view === v ? 'var(--color-ink)' : 'var(--color-ink-3)', boxShadow: view === v ? '0 1px 2px oklch(20% 0.04 240 / 0.05)' : 'none', transition: 'all 0.15s', cursor: 'pointer' }}>
              {v[0].toUpperCase() + v.slice(1)}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
