export default function EmptyState({ icon: Icon, title, subtitle }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10, padding: 48, color: 'var(--color-ink-4)' }}>
      {Icon && <Icon size={40} strokeWidth={1.2} />}
      <p style={{ margin: 0, fontSize: 13, fontWeight: 500, color: 'var(--color-ink-3)', textAlign: 'center' }}>{title}</p>
      {subtitle && <p style={{ margin: 0, fontSize: 12, color: 'var(--color-ink-4)', textAlign: 'center', lineHeight: 1.5 }}>{subtitle}</p>}
    </div>
  )
}
