import { useAppointments } from '../../hooks/useAppointments'

export default function AIStatsCard() {
  const { data: appointments = [] } = useAppointments()

  const total     = appointments.length
  const confirmed = appointments.filter((a) => a.status === 'confirmed').length
  const pending   = appointments.filter((a) => a.status === 'pending').length
  const pct       = total > 0 ? Math.round((confirmed / total) * 100) : 0

  return (
    <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, padding: 14, boxShadow: '0 1px 2px oklch(20% 0.04 240 / 0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--color-ink)' }}>AI activity</div>
        <button style={{ fontSize: 11, color: 'var(--color-ink-3)', padding: '3px 8px', borderRadius: 6, fontWeight: 500, border: 'none', background: 'none', cursor: 'pointer' }}>Details</button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10 }}>
        {[
          { num: total,     label: 'Total booked'  },
          { num: confirmed, label: 'Confirmed'      },
          { num: `${pct}%`, label: 'Confirmed rate' },
        ].map(({ num, label }) => (
          <div key={label} style={{ padding: '10px 10px 8px', borderRadius: 9, background: 'var(--color-bg-subtle)', border: '1px solid var(--color-border)' }}>
            <div style={{ fontFamily: 'var(--font-serif)', fontSize: 24, color: 'var(--color-ink)', lineHeight: 1.1, fontVariantNumeric: 'tabular-nums' }}>{num}</div>
            <div style={{ fontSize: 10, color: 'var(--color-ink-3)', marginTop: 2, lineHeight: 1.2 }}>{label}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
