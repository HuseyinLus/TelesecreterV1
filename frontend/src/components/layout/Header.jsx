import { Search, Bell, HelpCircle, Plus } from 'lucide-react'

export default function Header() {
  const today = new Date().toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

  return (
    <header style={{
      display: 'grid',
      gridTemplateColumns: '1fr auto 1fr',
      alignItems: 'center',
      padding: '18px 24px 16px',
      gap: 24,
      borderBottom: '1px solid var(--color-border)',
      background: 'var(--color-bg)',
      flexShrink: 0,
    }}>
      <div>
        <div style={{ fontSize: 11, color: 'var(--color-ink-3)', textTransform: 'uppercase', letterSpacing: '0.08em', fontWeight: 500, marginBottom: 4 }}>{today}</div>
        <h1 style={{ margin: 0, fontFamily: 'var(--font-serif)', fontSize: 26, fontWeight: 400, color: 'var(--color-ink)', letterSpacing: '-0.01em' }}>Good morning, Elif</h1>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 8, background: 'var(--color-surface)', border: '1px solid var(--color-border)', padding: '8px 12px', borderRadius: 10, width: 360 }}>
        <Search size={16} color="var(--color-ink-3)" />
        <input placeholder="Search patients, doctors, appointments…" style={{ border: 'none', outline: 'none', background: 'transparent', flex: 1, fontSize: 13, color: 'var(--color-ink)', fontFamily: 'var(--font-sans)' }} />
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'flex-end' }}>
        <button style={{ width: 34, height: 34, borderRadius: 9, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', border: '1px solid var(--color-border)', background: 'var(--color-surface)' }}>
          <Bell size={18} strokeWidth={1.6} />
        </button>
        <button style={{ width: 34, height: 34, borderRadius: 9, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', border: '1px solid var(--color-border)', background: 'var(--color-surface)' }}>
          <HelpCircle size={18} strokeWidth={1.6} />
        </button>
        <div style={{ width: 1, height: 22, background: 'var(--color-border)', margin: '0 4px' }} />
        <button style={{ display: 'flex', alignItems: 'center', gap: 6, padding: '8px 14px', background: 'var(--color-ink)', color: 'var(--color-bg)', borderRadius: 9, fontSize: 12.5, fontWeight: 500, border: 'none', cursor: 'pointer' }}>
          <Plus size={14} strokeWidth={2} />
          New appointment
        </button>
      </div>
    </header>
  )
}
