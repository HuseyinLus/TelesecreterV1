import { formatTime, toMinutes, isToday } from '../../utils/formatters'
import { getDoctorColor } from '../../utils/constants'

const RAIL_BG = { teal: 'var(--color-teal)', sage: 'var(--color-sage)', amber: 'var(--color-amber)', indigo: 'var(--color-indigo)', rose: 'var(--color-rose)' }

export default function TodayAgenda({ appointments, doctors, selectedId, onSelect }) {
  const doctorById = Object.fromEntries(doctors.map((d, i) => [d.id, { ...d, color: getDoctorColor(i) }]))
  const now = new Date()
  const nowMins = now.getHours() * 60 + now.getMinutes()

  const today = appointments
    .filter((a) => isToday(a.date))
    .sort((a, b) => a.start_time.localeCompare(b.start_time))

  const aiBookedCount = today.filter((a) => a.status !== 'cancelled').length

  return (
    <div style={{ background: 'var(--color-surface)', border: '1px solid var(--color-border)', borderRadius: 14, padding: 14, boxShadow: '0 1px 2px oklch(20% 0.04 240 / 0.05)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
        <div>
          <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--color-ink)', letterSpacing: '-0.005em' }}>Today</div>
          <div style={{ fontSize: 11, color: 'var(--color-ink-3)', marginTop: 2 }}>
            {today.length} appointments · {aiBookedCount} active
          </div>
        </div>
        <button style={{ fontSize: 11, color: 'var(--color-ink-3)', padding: '3px 8px', borderRadius: 6, fontWeight: 500, border: 'none', background: 'none', cursor: 'pointer' }}>View all</button>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 1, margin: '0 -6px' }}>
        {today.length === 0 && (
          <div style={{ padding: '16px 8px', textAlign: 'center', color: 'var(--color-ink-4)', fontSize: 12 }}>No appointments today</div>
        )}
        {today.map((a) => {
          const doc = doctorById[a.doctor_id]
          const startMins = toMinutes(a.start_time)
          const endMins   = toMinutes(a.end_time)
          const isPast = endMins < nowMins
          const isNow  = startMins <= nowMins && endMins > nowMins
          const docName = (doc?.full_name ?? doc?.name ?? '—').replace('Dr. ', '')

          return (
            <button
              key={a.id}
              onClick={() => onSelect(a)}
              style={{
                display: 'grid', gridTemplateColumns: '48px 3px 1fr', gap: 10,
                padding: '9px 8px', borderRadius: 8, textAlign: 'left', alignItems: 'start',
                opacity: isPast ? 0.5 : 1,
                background: isNow ? 'linear-gradient(90deg, oklch(66% 0.11 20 / 0.08), transparent 80%)' : selectedId === a.id ? 'var(--color-accent-soft)' : 'transparent',
                transition: 'background 0.12s',
                position: 'relative',
                border: 'none', cursor: 'pointer', width: '100%',
              }}
            >
              <div style={{ textAlign: 'right', paddingTop: 1 }}>
                <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--color-ink)', fontVariantNumeric: 'tabular-nums' }}>{formatTime(a.start_time)}</div>
                <div style={{ fontSize: 10, color: 'var(--color-ink-4)' }}>{Math.round(endMins - startMins)}m</div>
              </div>

              <div style={{ width: 3, borderRadius: 2, height: 28, marginTop: 2, background: doc ? RAIL_BG[doc.color] : 'var(--color-border)' }} />

              <div style={{ minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <span style={{ fontSize: 12.5, fontWeight: 600, color: 'var(--color-ink)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {a.user_id?.slice(0, 8)}…
                  </span>
                  {a.status === 'pending' && <span style={{ background: 'var(--color-amber-soft)', color: 'var(--color-amber)', fontSize: 9, fontWeight: 600, padding: '1px 5px', borderRadius: 4 }}>Pending</span>}
                </div>
                <div style={{ fontSize: 11, color: 'var(--color-ink-3)', marginTop: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {docName} · {doc?.specialty ?? ''}
                </div>
              </div>

              {isNow && (
                <div style={{ position: 'absolute', top: 12, right: 10, width: 6, height: 6, background: 'var(--color-rose)', borderRadius: '50%', boxShadow: '0 0 0 4px oklch(66% 0.11 20 / 0.2)' }} />
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
