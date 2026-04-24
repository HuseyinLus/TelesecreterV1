import { Bell, HelpCircle } from 'lucide-react'

export default function Header() {
  const today = new Date().toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

  return (
    <header style={{
      display: 'flex',
      justifyContent: 'space-between',
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

      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <button style={{ width: 34, height: 34, borderRadius: 9, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', border: '1px solid var(--color-border)', background: 'var(--color-surface)' }}>
          <Bell size={18} strokeWidth={1.6} />
        </button>
        <button style={{ width: 34, height: 34, borderRadius: 9, display: 'grid', placeItems: 'center', color: 'var(--color-ink-2)', border: '1px solid var(--color-border)', background: 'var(--color-surface)' }}>
          <HelpCircle size={18} strokeWidth={1.6} />
        </button>
      </div>
    </header>
  )
}
