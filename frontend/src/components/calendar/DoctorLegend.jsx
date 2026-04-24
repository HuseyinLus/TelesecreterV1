import { getDoctorColor } from '../../utils/constants'

const DOT_BG = { teal: 'var(--color-teal)', sage: 'var(--color-sage)', amber: 'var(--color-amber)', indigo: 'var(--color-indigo)', rose: 'var(--color-rose)' }

export default function DoctorLegend({ doctors }) {
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 14, padding: '14px 2px', marginTop: 8, borderTop: '1px solid var(--color-border)', fontSize: 11.5 }}>
      {doctors.map((d, i) => (
        <div key={d.id} style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'var(--color-ink-3)' }}>
          <span style={{ width: 9, height: 9, borderRadius: '50%', flexShrink: 0, background: DOT_BG[getDoctorColor(i)] }} />
          <span style={{ fontWeight: 500, color: 'var(--color-ink-2)' }}>{(d.full_name ?? d.name ?? '').replace('Dr. ', '')}</span>
          <span style={{ color: 'var(--color-ink-4)' }}>{d.specialty}</span>
        </div>
      ))}
    </div>
  )
}
