const STYLES = {
  pending:   { bg: 'var(--color-amber-soft)',  color: 'var(--color-amber)',    label: 'Pending' },
  confirmed: { bg: 'var(--color-sage-soft)',   color: 'var(--color-sage-ink)', label: 'Confirmed' },
  cancelled: { bg: 'var(--color-bg-subtle)',   color: 'var(--color-ink-4)',    label: 'Cancelled' },
}

export default function StatusPill({ status }) {
  const s = STYLES[status] ?? STYLES.pending
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: '2px 8px', borderRadius: 5, fontSize: 11, fontWeight: 500, background: s.bg, color: s.color }}>
      {s.label}
    </span>
  )
}
